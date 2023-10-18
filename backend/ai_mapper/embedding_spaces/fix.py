# %%
import pickle 

import numpy as np
import pandas as pd


df = pd.read_csv("/Users/philippwegner/Desktop/Fraunhofer/SEM-Group/git/mapping-assistent/ai_mapper/tests/ad-mapper_data.csv")
with open("embedding_space.pkl", "rb") as f:
    obj = pickle.load(f)

# %%
new_dict = {}

for key in obj:
    if key in df.Feature.tolist():
        
        new_dict[key] = obj[key]



#%%
with open("embedding_space_filtered.pkl", "wb") as f:
    pickle.dump(new_dict, f, protocol=pickle.HIGHEST_PROTOCOL)
# %%
