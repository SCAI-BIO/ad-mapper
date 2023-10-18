# %%
import transformers, torch, sys
from tqdm import tqdm

sys.path.append("../../backend")
sys.path.append("../")
sys.path.append("../..")

from ai_mapper.models import BertMapper as mapping_model


from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained('dmis-lab/biobert-v1.1')


import pandas as pd
import pickle

import sys
#nlp = spacy.load("/Users/philippwegner/Desktop/Fraunhofer/SEM-Group/git/semantic-annotator/backend/annotators/ADO_nlp_2022_11_04_v1")



# %%
config = {
    "version": "dmis-lab/biobert-v1.1", 
    "dropout": 0.3, 
    "lr": 2e-5, 
    "weight_decay": 5e-3
}
model = mapping_model(config)
model.load_state_dict(torch.load("/Users/philippwegner/Desktop/Fraunhofer/SEM-Group/git/mapping-assistent/ai_mapper/bioBERT_ai_mapper_v3_dataset.pth"))
model.eval()


# %%
#cdm = pd.read_excel("/Users/philippwegner/Desktop/Fraunhofer/cdm-ndd/datamodels/Datamodel_6_5_22.xlsx", sheet_name="Attributes")
#cdm = pd.read_csv("CDM/ad-mapper_data.csv")
cdm = pd.read_csv("/Users/philippwegner/Downloads/AD Cohorts Mappings - new_variables (1).csv")
# %%
total_ents = []
padding=245
embedd_space = {}
all_sentences = []
for i, row in tqdm(cdm.iterrows(), total=len(list(cdm.iterrows()))):
    var = row['Feature']
    description = row['Definition']
    sentence = var + " " + (description if str(description).lower() != 'nan' else "")
    #doc = nlp(sentence)
    if not sentence:
        print(row)
    tokenized = tokenizer(sentence,padding='max_length', max_length=padding, return_tensors='pt')
    model_out = model(tokenized, output_hidden_states =True).hidden_states[-1][0,0,:]
    embedd_space[var] = torch.squeeze(model_out).detach().numpy() 
    
# %%

# with open("embedding_space_13_5.pkl", "wb") as f:
#     pickle.dump(embedd_space, f, protocol=pickle.HIGHEST_PROTOCOL)

with open("embedding_space_unseen.pkl", "wb") as f:
    pickle.dump(embedd_space, f, protocol=pickle.HIGHEST_PROTOCOL)

# %%
embedd_space

# %%
