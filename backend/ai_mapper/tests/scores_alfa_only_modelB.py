# %%
import pandas as pd
import requests
df = pd.read_csv("ad-mapper_data.csv")

xlsx = pd.read_excel("20221021_index_ALFA+.xlsx", sheet_name="root")

df = df[~df.ALFA.isna()]


xlsx
# %%
k = 5
correct = 0
total = 0
w=0.3

print(xlsx.columns)

allready_predicted = []

for i, row in df.iterrows():
    
    
    #description_1 = row["description_1"]
    
    var_2 = row["ALFA"]

    if var_2 in allready_predicted:
        continue
    total += 1
    allready_predicted.append(var_2)
    df_matching_external = df[df['ALFA'] == var_2]
    var_1_all = [str(s).lower().strip() for s in df_matching_external["Feature"].tolist()]

    desc = xlsx.query("Name == @var_2")
    if desc.shape[0] == 0:
        print(var_2)
        description_2 = ""
    else:
        description_2 = desc.iloc[0]['Description']
    response = requests.get(f"http://localhost:8000/v2/ai-mapper?variable_name={var_2}&variable_description={description_2}&k={k}&w_1={1-w}&w_2={w}&bypass_binary=false&class_prob_threshold=0.2&useSubstringMetric=true")
    response_json = response.json()
    prediction = list(response_json["class_props"].keys())
    print(prediction)
    if prediction == "No suitable variable found." and description_2 != "":
        response = requests.get(f"http://localhost:8000/v2/ai-mapper?variable_name=&variable_description={description_2}&k={k}&w_1={1-w}&w_2={w}&bypass_binary=false&class_prob_threshold=0.2&useSubstringMetric=true")
        response_json = response.json()
        prediction = list(response_json["class_props"].keys())
    if prediction == "No suitable variable found.":
        response = requests.get(f"http://localhost:8000/v2/ai-mapper?variable_name={var_2}&variable_description=&k={k}&w_1={1-w}&w_2={w}&bypass_binary=false&class_prob_threshold=0.2&useSubstringMetric=true")
        response_json = response.json()
        prediction = list(response_json["class_props"].keys())
    
    if bool(set(prediction) & set(var_1_all)):
        correct += 1
    else:
        print(f"Prediction: {prediction} predicted from {var_2}")
        print(f"True label: {var_1_all}")

        print("########################")



# %%
print(correct / total)

# %%
