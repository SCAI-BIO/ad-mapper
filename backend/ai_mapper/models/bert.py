# %%
from typing import Optional, Tuple, Union
import torch
from transformers import BertForSequenceClassification, BertTokenizer
import pandas as pd
from torch.utils.data import DataLoader
import pytorch_lightning as pl
from torch import cuda
import torch.functional as F
from torch.optim import AdamW
from torch import Tensor, softmax, argmax
import transformers
from torchmetrics import Precision, Recall, F1Score
from sklearn.metrics import f1_score, precision_score, recall_score, classification_report, accuracy_score
from torch.nn import BCEWithLogitsLoss, CrossEntropyLoss, MSELoss
from transformers.modeling_outputs import SequenceClassifierOutput

# %%
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def prepare_data(data : pd.DataFrame):
    data_to_be_tokenized = []
    raw_labels = []
    tokenizer = BertTokenizer.from_pretrained('dmis-lab/biobert-v1.1')
    max_length = 0
    for i, row in data.iterrows():
        sentence_a = (row['var_1'] if str(row['var_1']).lower() !='nan' else "") + " " + (row['description_1'] if str(row['description_1']).lower() !='nan' else "")
        sentence_b = (row['var_2'] if str(row['var_2']).lower() !='nan' else "") + " " + (row['description_2'] if str(row['description_2']).lower() !='nan' else "")
        label = row['label']
        raw_labels.append(label)
        l_tokenizer = len(tokenizer.encode(sentence_a, sentence_b))
        if l_tokenizer > max_length:
            max_length = l_tokenizer
        data_to_be_tokenized.append((sentence_a, sentence_b))

    
    return [[tokenizer(data_to_be_tokenized[i][0], data_to_be_tokenized[i][1], padding="max_length", max_length=max_length, return_tensors='pt'), raw_labels[i]] for i in range(len(data_to_be_tokenized))]

    

class MyBertForSequenceClassification(BertForSequenceClassification):
    def __init__(self, config):
        super().__init__(config)

    def forward(
        self,
        input_ids: Optional[torch.Tensor] = None,
        attention_mask: Optional[torch.Tensor] = None,
        token_type_ids: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.Tensor] = None,
        head_mask: Optional[torch.Tensor] = None,
        inputs_embeds: Optional[torch.Tensor] = None,
        labels: Optional[torch.Tensor] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
    ) -> Union[Tuple[torch.Tensor], SequenceClassifierOutput]:
        r"""
        labels (`torch.LongTensor` of shape `(batch_size,)`, *optional*):
            Labels for computing the sequence classification/regression loss. Indices should be in `[0, ...,
            config.num_labels - 1]`. If `config.num_labels == 1` a regression loss is computed (Mean-Square loss), If
            `config.num_labels > 1` a classification loss is computed (Cross-Entropy).
        """
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        outputs = self.bert(
            input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            position_ids=position_ids,
            head_mask=head_mask,
            inputs_embeds=inputs_embeds,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )

        pooled_output = outputs[1]

        pooled_output = self.dropout(pooled_output)
        logits = self.classifier(pooled_output)

        loss = None
        if labels is not None:
            if self.config.problem_type is None:
                if self.num_labels == 1:
                    self.config.problem_type = "regression"
                elif self.num_labels > 1 and (labels.dtype == torch.long or labels.dtype == torch.int):
                    self.config.problem_type = "single_label_classification"
                else:
                    self.config.problem_type = "multi_label_classification"

            if self.config.problem_type == "regression":
                loss_fct = MSELoss()
                if self.num_labels == 1:
                    loss = loss_fct(logits.squeeze(), labels.squeeze())
                else:
                    loss = loss_fct(logits, labels)
            elif self.config.problem_type == "single_label_classification":
                loss_fct = CrossEntropyLoss(weight=torch.tensor([0.1,0.9], device=device))
                loss = loss_fct(logits.view(-1, self.num_labels), labels.view(-1))
            elif self.config.problem_type == "multi_label_classification":
                loss_fct = BCEWithLogitsLoss()
                loss = loss_fct(logits, labels)
        if not return_dict:
            output = (logits,) + outputs[2:]
            return ((loss,) + output) if loss is not None else output

        return SequenceClassifierOutput(
            loss=loss,
            logits=logits,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
        )






class MappingModel(pl.LightningModule):

    def __init__(self, config, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.classifier_dropout = config['dropout'] or None
        self.lr = config['lr'] or None
        self.weight_decay = config['weight_decay'] or None
        self.transformer = MyBertForSequenceClassification.from_pretrained(config["version"], num_labels = 2, classifier_dropout=self.classifier_dropout)


    def forward(self, x, **kwargs):
        if "output_hidden_states" in kwargs:
            return self.transformer(**x, output_hidden_states=kwargs['output_hidden_states'])
        else:
            return self.transformer(**x)


    def training_step(self, batch):
        x, y = batch 
        x['input_ids'] = x['input_ids'].squeeze(1)
        x['attention_mask'] = x['attention_mask'].squeeze(1)
        x['token_type_ids'] = x['token_type_ids'].squeeze(1)
        loss = self.transformer(**x ,labels=y).loss
        self.log("train_loss", loss.item())
        return loss



    def validation_step(self, batch, batch_idx):
        x, y = batch 
        x['input_ids'] = x['input_ids'].squeeze(1)
        x['attention_mask'] = x['attention_mask'].squeeze(1)
        x['token_type_ids'] = x['token_type_ids'].squeeze(1)
        output = self.transformer(**x ,labels=y)
        self.log("val_loss", output.loss.item())
        
        logits = output.logits
        class_probabilities = softmax(logits, dim=1)
        predictions = argmax(logits, dim=1)
        return {'predictions': predictions, 'true': y,  'class_probs': class_probabilities}
        
        


    def validation_epoch_end(self, outputs,**kwargs):
        total_predictions = []
        total_class_probabilities = []
        total_true = []
        print(outputs)
        for output in outputs:
            total_predictions.extend([int(val.item()) for val in output['predictions'].to("cpu")])
            total_class_probabilities.extend([(int(val[0].item()), int(val[1].item())) for val in output['class_probs'].to("cpu")])
            total_true.extend([int(l.item()) for l in output['true'].to("cpu")])
        self.log('precision', precision_score(total_true, total_predictions), on_epoch=True)
        self.log('recall', recall_score(total_true, total_predictions), on_epoch=True)
        self.log('f1-score', f1_score(total_true, total_predictions), prog_bar=True, on_epoch=True)
        print(classification_report(total_true, total_predictions))


    def test_step(self, batch, batch_idx):
        x, y = batch 
        x['input_ids'] = x['input_ids'].squeeze(1)
        x['attention_mask'] = x['attention_mask'].squeeze(1)
        x['token_type_ids'] = x['token_type_ids'].squeeze(1)
        output = self.transformer(**x,labels=y)
        self.log("test_loss", output.loss.item())
        
        logits = output.logits
        class_probabilities = softmax(logits, dim=1)
        predictions = argmax(logits, dim=1)
        return {'predictions': predictions, 'true': y,  'class_probs': class_probabilities}
    
    def test_epoch_end(self, outputs, **kwargs):
        total_predictions = []
        total_class_probabilities = []
        total_true = []
        
        for output in outputs:
            total_predictions.extend([int(val.item()) for val in output['predictions'].to("cpu")])
            total_class_probabilities.extend([(int(val[0].item()), int(val[1].item())) for val in output['class_probs'].to("cpu")])
            total_true.extend([int(l.item()) for l in output['true'].to("cpu")])
        self.log('precision', precision_score(total_true, total_predictions), on_epoch=True)
        self.log('recall', recall_score(total_true, total_predictions), on_epoch=True)
        self.log('f1-score', f1_score(total_true, total_predictions), on_epoch=True)
        self.log('accuracy', accuracy_score(total_true, total_predictions), on_epoch=True)
        


    def configure_optimizers(self):
        return AdamW(self.parameters(), lr=self.lr, weight_decay=self.weight_decay)
# %%
