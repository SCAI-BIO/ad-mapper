# %%
import pandas as pd
import requests
df = pd.read_csv("ad-mapper_data.csv")

xlsx = pd.read_csv("Data_dictionary_AMED-pre.tsv", sep="\t")

df = df[~df.AMED.isna()]


xlsx
# %%
k = 10

w=0.0

for k in [5,10]:

    for w in [0.1]:

        allready_predicted = []
        correct = 0
        total = 0

        for i, row in df.iterrows():
            
            var_1 = row["Feature"]
            var_2 = row["AMED"]

            if var_2 in allready_predicted:
                continue
            total += 1
            allready_predicted.append(var_2)
            #description_1 = row["description_1"]
            df_matching_external = df[df['AMED'] == var_2]
            var_1_all = [str(s).lower().strip() for s in df_matching_external["Feature"].tolist()]
            
            
            desc = xlsx.query("fldname == @var_2")
            if desc.shape[0] == 0:
                #print(var_2)
                description_2 = ""
            else:
                description_2 = desc.iloc[0]['desc_en']
            response = requests.get(f"http://localhost:8000/v2/ai-mapper?variable_name={var_2}&variable_description={description_2}&k={k}&w_1={1-w}&w_2={w}&bypass_binary=false&class_prob_threshold=0.2&usePriorMappings=true&useSubstringMetric=true")
            response_json = response.json()
            prediction = response_json["winner"][0]
            if prediction == "No suitable variable found." and description_2 != "":
                response = requests.get(f"http://localhost:8000/v2/ai-mapper?variable_name=&variable_description={description_2}&k={k}&w_1={1-w}&w_2={w}&bypass_binary=false&class_prob_threshold=0.2&usePriorMappings=true&useSubstringMetric=true")
                response_json = response.json()
                prediction = response_json["winner"][0]
            if prediction == "No suitable variable found.":
                response = requests.get(f"http://localhost:8000/v2/ai-mapper?variable_name={var_2}&variable_description=&k={k}&w_1={1-w}&w_2={w}&bypass_binary=false&class_prob_threshold=0.2&usePriorMappings=true&useSubstringMetric=true")
                response_json = response.json()
                prediction = response_json["winner"][0]
            
            if prediction.strip() in var_1_all:
                correct += 1
            else:
                pass
                #print(str(var_1_all) + " ----:---- ", prediction)
                #print(var_2 + " ----:---- ", description_2)
                #print("########################")

        print("k: ", k, "w: ", w)
        print(correct / total)
        print("########################")



# %%
