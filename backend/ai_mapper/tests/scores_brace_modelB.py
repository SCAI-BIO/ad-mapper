# %%
import pandas as pd
import requests
df = pd.read_csv("ad-mapper_data.csv")

xlsx = pd.read_excel("BRACE_2.xlsx", sheet_name=0)

df = df[~df.BRACE.isna()]


xlsx
# %%
k = 5
correct = 0
total = 0
w=0.2

allready_predicted = []

print(xlsx.columns)

for i, row in df.iterrows():

    var_2 = row["BRACE"]
    

    if var_2 in allready_predicted:
        continue
    total += 1
    allready_predicted.append(var_2)

    var_1 = row["Feature"]
    #description_1 = row["description_1"]

    df_matching_external = df[df['BRACE'] == var_2]
    var_1_all = [str(s).lower().strip() for s in df_matching_external["Feature"].tolist()]
    
    
    
    desc = xlsx.query("Field == @var_2")
    if desc.shape[0] == 0:
        print(var_2)
        raise
    else:
        description_2 = desc.iloc[0]['Description ']
    response = requests.get(f"http://localhost:8000/v2/ai-mapper?variable_name={var_2}&variable_description={description_2}&k={k}&w_1={1-w}&w_2={w}&bypass_binary=false&class_prob_threshold=0.2&useDefinitions=false")
    response_json = response.json()
    prediction = list(response_json["class_props"].keys())
    if len(prediction) == 0 and description_2 != "":
        response = requests.get(f"http://localhost:8000/v2/ai-mapper?variable_name=&variable_description={description_2}&k={k}&w_1={1-w}&w_2={w}&bypass_binary=false&class_prob_threshold=0.2&useDefinitions=false")
        response_json = response.json()
        prediction = list(response_json["class_props"].keys())
    if len(prediction) == 0:
        response = requests.get(f"http://localhost:8000/v2/ai-mapper?variable_name={var_2}&variable_description=&k={k}&w_1={1-w}&w_2={w}&bypass_binary=false&class_prob_threshold=0.2&useDefinitions=false")
        response_json = response.json()
        prediction = list(response_json["class_props"].keys())
    
    if bool(set(prediction) & set(var_1_all)):
        correct += 1
    else:
        print(str(var_1_all) + " ----:---- ", prediction)
        print(var_2 + " ----:---- ", description_2)
        print("########################")



# %%
print(correct / total)

# %%
