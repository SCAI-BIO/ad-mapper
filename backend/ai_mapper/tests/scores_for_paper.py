# %%
import pandas as pd
import requests
from joblib import Parallel, delayed, wrap_non_picklable_objects

df = pd.read_csv("../data/test_v3_old.csv")
# %%
df = df[df.label == 1]
k = 5 
false_predictions = []
# %%
total = len(df)


def outer(k):
    Parallel(n_jobs=2)(delayed(inner)(w,k) for w in [0.0,0.1,0.3,0.5])




def inner(w, k):
    correct = 0
    

    for i, row in df.iterrows():
        var_1 = row["var_1"]
        #description_1 = row["description_1"]
        
        var_2 = row["var_2"]
        description_2 = row["description_2"] if str(row["description_2"]).lower() != "nan" else ""

        response = requests.get(f"http://localhost:8000/v2/ai-mapper?variable_name={var_2}&variable_description={description_2}&k={k}&w_1={1-w}&w_2={w}&class_prob_threshold=0.2&usePriorMappings=true")
        response_json = response.json()
        prediction = response_json["winner"][0]
        
        if prediction == "No suitable variable found." and description_2 != "":
            response = requests.get(f"http://localhost:8000/v2/ai-mapper?variable_name=&variable_description={description_2}&k={k}&w_1={1-w}&w_2={w}&class_prob_threshold=0.2&usePriorMappings=true")
            response_json = response.json()
            prediction = response_json["winner"][0]
        if prediction == "No suitable variable found.":
            response = requests.get(f"http://localhost:8000/v2/ai-mapper?variable_name={var_2}&variable_description=&k={k}&w_1={1-w}&w_2={w}&class_prob_threshold=0.2&usePriorMappings=true")
            response_json = response.json()
            prediction = response_json["winner"][0]
        
        if prediction.strip() == var_1.lower().strip():
            correct += 1
        
            #print(var_1 + " ----:---- ", prediction)
            #print(var_2 + " ----:---- ", description_2)
            #print("########################")
            #false_predictions.append(f"{var_1};{prediction};{var_2};{description_2}")
    '''
    with open(f"false_predictions_{k}.csv", "w") as f:
        f.write("True;prediction;input;description")
        for line in false_predictions:
            f.write("\n")
            f.write(line)
    '''
    print(f"Performance for k={k} and w_1={1-w}, w_2={w}:")
    print(correct / total)

# %%

# for k in [1,5,10]:
#     for w in [0.0,0.1,0.3,0.5]:
#         inner(w,k)


#Parallel(n_jobs=3)(delayed(outer)(k) for k in [1,5,10])


inner(0.0, 10)

# %%
