# %%

import pandas as pd
import pickle
import requests


from tqdm import tqdm 
#df_unseen = pd.read_csv("/Users/philippwegner/Downloads/AD Cohorts Mappings - new_variables (1).csv")
df_unseen = pd.read_csv("/Users/philippwegner/Downloads/new_variables_adni.csv")
df_unseen

# %%

# # join embedding spaces 

# space1 = "/Users/philippwegner/Desktop/Fraunhofer/SEM-Group/git/mapping-assistent/ai_mapper/embedding_spaces/embedding_space_unseen.pkl"
# space2 = "/Users/philippwegner/Desktop/Fraunhofer/SEM-Group/git/mapping-assistent/ai_mapper/embedding_spaces/embedding_space_13_5.pkl"


# with open(space1, "rb") as f:
#     space1 = pickle.load(f)

# with open(space2, "rb") as f:
#     space2 = pickle.load(f)

# ## combine spaces

# space1.update(space2)

# with open("embedding_space_unseen_combined.pkl", "wb") as f:
#     pickle.dump(space1, f, protocol=pickle.HIGHEST_PROTOCOL)

# # %%


cols = df_unseen.columns[4:]

total = 0
correct = 0

k = len(df_unseen)

w = 1.0

with tqdm(total=df_unseen.shape[0]) as pbar:
    for i, row in df_unseen.iterrows():
        var_1 = row["Feature"]


        description_2 = row["ADNI_Definition"]

        no_description = False

        if str(description_2).lower().strip() == "nan":
            no_description = True

        if not no_description:

            if description_2.startswith("Score "):
                description_2 = ""
            else:
                description_2 = description_2.split(".")[1]
        
        
        var_2 = row["ADNI"]

        if str(var_2).lower().strip() == "nan":
            continue
        
        total +=1

        response = requests.get(f"http://localhost:8000/v2/ai-mapper?variable_name={var_2}&variable_description={description_2}&k={k}&w_1={1-w}&w_2={w}&class_prob_threshold=0.0&usePriorMappings=false")
        response_json = response.json()
        prediction = response_json["winner"][0]


        if prediction == "No suitable variable found." and description_2 != "":
            response = requests.get(f"http://localhost:8000/v2/ai-mapper?variable_name=&variable_description={description_2}&k={k}&w_1={1-w}&w_2={w}&class_prob_threshold=0.0&usePriorMappings=false")
            response_json = response.json()
            prediction = response_json["winner"][0]
        if prediction == "No suitable variable found.":
            response = requests.get(f"http://localhost:8000/v2/ai-mapper?variable_name={var_2}&variable_description=&k={k}&w_1={1-w}&w_2={w}&class_prob_threshold=0.0&usePriorMappings=false")
            response_json = response.json()
            prediction = response_json["winner"][0]
        
        
        if prediction.strip() == var_1.lower().strip():
            correct += 1
        else:
            print(var_2)

            print(prediction)
            print("########################")
        pbar.update(1)
    

# %%
print(correct / total)

# %%

