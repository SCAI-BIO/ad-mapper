# %%
from Levenshtein import distance
import pandas as pd 


cdm = pd.read_excel("/Users/philippwegner/Desktop/Fraunhofer/cdm-ndd/datamodels/Datamodel_6_5_22.xlsx", sheet_name="Attributes")

cdm

def find_matching_substrings(sentence_a, sentence_b, substring_length):
    matching_substrings = set()
    sentence_a_length = len(sentence_a)
    sentence_b_length = len(sentence_b)

    if substring_length > sentence_a_length or substring_length > sentence_b_length:
        raise ValueError("Substring length cannot be greater than the length of either sentence.")

    for i in range(sentence_a_length - substring_length + 1):
        substring_a = sentence_a[i:i + substring_length]
        if substring_a in sentence_b:
            matching_substrings.add(substring_a)

    return len(matching_substrings)
# %%

df = pd.read_csv("../data/test_v3.csv")

brace = pd.read_csv("ad-mapper_data.csv")


df = df[df.label == 1]

# %%

correct = 0
total = len(df)
for i, row in df.iterrows():
    print(i/total*100, "%")
    winner = cdm.Attribute.tolist()[0]
    dist = distance(row['var_2'], cdm.Attribute.tolist()[0])
    for attr in cdm.Attribute.tolist():
        d = distance(row['var_2'], attr)
        if d < dist:
            dist = d
            winner = attr
    if winner.lower() == row['var_1'].lower():
        correct += 1


print(correct/total)


# %%
df = brace[~brace.BRACE.isna()]
df.reset_index(inplace=True)
correct = 0
total = len(df)
for i, row in df.iterrows():
    print(i/total*100, "%")
    winner = cdm.Attribute.tolist()[0]
    dist = distance(row['BRACE'], cdm.Attribute.tolist()[0])
    for attr in cdm.Attribute.tolist():
        d = distance(row['BRACE'], attr)
        if d < dist:
            dist = d
            winner = attr
    if winner.lower() == row['Feature'].lower():
        correct += 1


print(correct/total)



# %%
df_unseen = pd.read_csv("/Users/philippwegner/Downloads/new_variables_adni.csv")

correct = 0
total = 0 

for i, row in df_unseen.iterrows():
    target = row['Feature']
    candidates = df_unseen['ADNI'].tolist()

    winner = None

    dist = 1e15

    for j, candidate in enumerate(candidates):
        if str(candidate).lower() == "nan":
            continue

        if len(candidate) > len(target):
            longer_word = candidate
            shorter_word = target
        else:
            longer_word = target
            shorter_word = candidate
        substirng_val = find_matching_substrings(longer_word, shorter_word, 3)/(len(shorter_word)-2)

        d = distance(target, candidate) / max(len(target), len(candidate))

        #d = 0.5 * d + 0.5 * substirng_val

    
        if d < dist:
            dist = d
            winner = j
    total +=1

    print(candidates[winner], target)

    if winner == i:
        correct += 1


print(correct/total)

# %%

# %%
df = brace[~brace.AMED.isna()]
df.reset_index(inplace=True)
correct = 0
total = len(df)
for i, row in df.iterrows():
    print(i/total*100, "%")
    winner = cdm.Attribute.tolist()[0]
    dist = distance(row['AMED'], cdm.Attribute.tolist()[0])
    for attr in cdm.Attribute.tolist():
        d = distance(row['AMED'], attr)
        if d < dist:
            dist = d
            winner = attr
    if winner.lower() == row['Feature'].lower():
        correct += 1


print(correct/total)

# %%

df = brace[~brace.ALFA.isna()]
df.reset_index(inplace=True)
correct = 0
total = len(df)
for i, row in df.iterrows():
    print(i/total*100, "%")
    winner = cdm.Attribute.tolist()[0]
    dist = distance(row['ALFA'], cdm.Attribute.tolist()[0])
    for attr in cdm.Attribute.tolist():
        d = distance(row['ALFA'], attr)
        if d < dist:
            dist = d
            winner = attr
    if winner.lower() == row['Feature'].lower():
        correct += 1


print(correct/total)
