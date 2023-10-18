# %%
import sys
sys.path.append("models")
import torch 

from sklearn.metrics import classification_report

import pandas as pd 



train_data = pd.read_csv("data/train_v3.csv")
validation_data = pd.read_csv("data/dev_v3.csv")
train_data.label.value_counts()

# %%

test_set = pd.read_csv("data/test.csv")

# %%

from models import BertMapper

from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained("dmis-lab/biobert-v1.1")

config = config = {
    "version": "dmis-lab/biobert-v1.1", 
    "dropout": 0.3, 
    "lr": 2e-5, 
    "weight_decay": 5e-3
}

model = BertMapper(config)

model.load_state_dict(torch.load("bioBERT_ai_mapper.pth"))

# %%


sentence_a = "Gender The patients sex"
sentence_b = "The gender of study participant"


sentence_b2 = "Left Hippocampus Volume"



tokenized_1 = tokenizer(sentence_a, sentence_b, return_tensors = 'pt')

tokenized_2 = tokenizer(sentence_a, sentence_b2, return_tensors = 'pt')

# %%
torch.argmax(model(tokenized_1).logits)
# %%
torch.argmax(model(tokenized_2).logits)

# %%

total_true = []
total_pred = []

for i ,row in test_set.iterrows():
    print(f"\r {i}")
    sentence_a = (row['var_1'] if str(row['var_1']).lower() !='nan' else "") + " " + (row['description_1'] if str(row['description_1']).lower() !='nan' else "")
    sentence_b = (row['var_2'] if str(row['var_2']).lower() !='nan' else "") + " " + (row['description_2'] if str(row['description_2']).lower() !='nan' else "")
    tokenized = tokenizer(sentence_a, sentence_b, return_tensors = 'pt')
    label = row['label']
    pred = torch.argmax(model(tokenized).logits)
    total_true.append(label)
    total_pred.append(pred)


print(classification_report(total_true, total_pred))




# %%
