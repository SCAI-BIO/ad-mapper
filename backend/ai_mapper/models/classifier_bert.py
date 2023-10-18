# %%
from transformers import BertForSequenceClassification, BertTokenizer, BertModel
import pandas as pd
import numpy as np
import pickle
from torch.utils.data import DataLoader
import pytorch_lightning as pl
from torch import cuda
import torch.functional as F
from torch.optim import AdamW
from torch import Tensor, softmax, argmax, from_numpy, squeeze, sub, abs, argmin, cdist, topk
import torch.nn as nn
import transformers
from torchmetrics import Precision, Recall, F1Score, Accuracy
from sklearn.metrics import f1_score, precision_score, r2_score, recall_score, classification_report, accuracy_score
from collections import Counter

# %%
# K = 1
# try:
#     attributes = pd.read_excel("data/Datamodel_6_5_22.xlsx", sheet_name="Attributes")['Attribute'].to_list()
#     attributes = [a.lower().strip() for a in attributes]
# except FileNotFoundError as e:
#     print("File not found... Try other location")
#     try:
#         attributes = pd.read_excel("../data/Datamodel_6_5_22.xlsx", sheet_name="Attributes")['Attribute'].to_list()
#         attributes = [a.lower().strip() for a in attributes]
#     except:
#         print("File not found... Try other location")
#         attributes = pd.read_excel("../ai_mapper/data/Datamodel_6_5_22.xlsx", sheet_name="Attributes")['Attribute'].to_list()
#         attributes = [a.lower().strip() for a in attributes]


# %%
device = "cuda" if cuda.is_available() else "cpu"
def prepare_data(data : pd.DataFrame):
    try:
        with open("embedding_spaces/embedding_space_13_5.pkl", "rb") as f:
            obj = pickle.load(f)
            labels = np.char.strip(np.char.lower(np.array(list(obj.keys()))))
    except FileNotFoundError as e: 
        with open("../embedding_spaces/embedding_space_13_5.pkl", "rb") as f:
            obj = pickle.load(f)
            labels = np.char.strip(np.char.lower(np.array(list(obj.keys()))))

            


    data_to_be_tokenized = []
    raw_labels = []
    tokenizer = BertTokenizer.from_pretrained('dmis-lab/biobert-v1.1')
    max_length = 0
    for i, row in data.iterrows():
        if row['label'] == 0:
            continue
        label = row['var_1'].strip().lower()
        if label not in labels:
            print(label)
            continue
        sentence_b = (row['var_2'] if str(row['var_2']).lower() !='nan' else "") + " " + (row['description_2'] if str(row['description_2']).lower() !='nan' else "")
        #label = row['label']
        raw_labels.append(label)
        l_tokenizer = len(tokenizer.encode(sentence_b))
        if l_tokenizer > max_length:
            max_length = l_tokenizer
        data_to_be_tokenized.append(sentence_b)

    
    return [[tokenizer(data_to_be_tokenized[i], padding="max_length", max_length=max_length, return_tensors='pt'), raw_labels[i]] for i in range(len(data_to_be_tokenized))]



def find_nearest(array, value):
    array = from_numpy(array).to(device)
    dist = cdist(array, value)
    idx = argmin(dist, dim=0)
    return idx

def find_nearest_k(array,value, k):
    array = from_numpy(array).to(device)
    dist = cdist(array, value)
    smallest_k = topk(dist, k, 0, False)
    return smallest_k[1]




class MappingModelCl(pl.LightningModule):

    def __init__(self, config, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.classifier_dropout = config['dropout'] or None
        self.lr = config['lr'] or None
        self.weight_decay = config['weight_decay'] or None
        self.transformer = BertModel.from_pretrained(config['version'])
        self.dropout = nn.Dropout(config['dropout'])
        with open(config['emb_path'], "rb") as f:
            obj = pickle.load(f)
            self.labels = np.char.strip(np.char.lower(np.array(list(obj.keys()))))

            label_dublicates = [item for item, count in Counter(self.labels).items() if count > 1]
            dublicates_indeces = [int(np.where(self.labels == l)[0][1:]) for l in label_dublicates]

            self.labels = np.delete(self.labels, dublicates_indeces)

            self.embedding_CDM = np.delete(np.array(list(obj.values())), dublicates_indeces, axis=0)
        self.linear = nn.Linear(768, 768)
        self.loss = nn.MSELoss()
        

    def forward(self, x):
        out = self.transformer(**x).last_hidden_state[:,0,:]
        out = self.dropout(out)
        return self.linear(out)


    def training_step(self, batch, *args, **kwargs):
        x, y = batch 

        index = np.array([np.where(self.labels == y_val)[0] for y_val in y])
        #print(index)
        label = from_numpy(self.embedding_CDM[index]).to(device)
        x['input_ids'] = x['input_ids'].squeeze(1)
        x['attention_mask'] = x['attention_mask'].squeeze(1)
        x['token_type_ids'] = x['token_type_ids'].squeeze(1)
        out = self(x)
        
        label = squeeze(label, dim=1)
        
        loss = self.loss(out, label)
        self.log("train_loss", loss.item())
        return loss

    def validation_step(self, batch, *args, **kwargs):
        x, y = batch 
        
        index = np.array([np.where(self.labels == y_val)[0] for y_val in y])
        #print(index)

        #index = np.argwhere(np.isin(self.labels, y))
        label = from_numpy(self.embedding_CDM[index]).to(device)
        x['input_ids'] = x['input_ids'].squeeze(1)
        x['attention_mask'] = x['attention_mask'].squeeze(1)
        x['token_type_ids'] = x['token_type_ids'].squeeze(1)
        out = self(x)
        label = squeeze(label, dim=1)
        loss = self.loss(out, label)
        self.log("val_loss", loss.item())        
        predictions = find_nearest(self.embedding_CDM, out)
        index = squeeze(from_numpy(index))
        return {'predictions': predictions, 'true': index}

    def test_step(self, batch, *args, **kwargs):
        x, y = batch 
        index = np.array([np.where(self.labels == y_val)[0] for y_val in y])
        label = from_numpy(self.embedding_CDM[index]).to(device)
        x['input_ids'] = x['input_ids'].squeeze(1)
        x['attention_mask'] = x['attention_mask'].squeeze(1)
        x['token_type_ids'] = x['token_type_ids'].squeeze(1)
        out = self(x)
        label = squeeze(label, dim=1)      
        predictions = find_nearest_k(self.embedding_CDM, out, K)

        index = squeeze(from_numpy(index))
        predictions_ = []
        for i, l in enumerate(index):
            if l in predictions[:, i]:
                predictions_.append(l.item())
            else:
                predictions_.append(predictions[0, i].item())
        return {'predictions': Tensor(predictions_), 'true': index}

    def test_epoch_end(self, outputs):
        total_predictions = []
        total_true = []
        for output in outputs:
            total_predictions.extend([int(val.item()) for val in output['predictions'].to("cpu")])
            total_true.extend([int(l.item()) for l in output['true'].to("cpu")])
        self.log("accuracy",accuracy_score(total_true, total_predictions))
        
           
    def validation_epoch_end(self, outputs):
        total_predictions = []
        total_true = []
        for output in outputs:
            if output['predictions'].dim() == 0:
                total_predictions.append(int(output['predictions'].to("cpu").item()))
            else:
                total_predictions.extend([int(val.item()) for val in output['predictions'].to("cpu")])
            if output['true'].dim() == 0:
                total_true.append(int(output['true'].to("cpu").item()))
            else:
                total_true.extend([int(l.item()) for l in output['true'].to("cpu")])
        self.log("accuracy",accuracy_score(total_true, total_predictions))



    def configure_optimizers(self):
        return AdamW(self.parameters(), lr=self.lr, weight_decay=self.weight_decay)
# %%
