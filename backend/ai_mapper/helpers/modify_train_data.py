# %%
import pandas as pd

PATH = "../data/"



for dataset in ["../data/dev_v3.csv", "../data/test_v3.csv", "../data/train_v3.csv"]:
    df = pd.read_csv(dataset)
    df = df.drop(df.columns[0], axis=1)
    n_rows = []
    for i, row in df.iterrows():
        descript_1 = str(row['description_1']).lower()
        descript_2 = str(row['description_2']).lower()
        if descript_1 != "nan":
            n_rows.append([row['var_1'], "", row['var_2'], row['description_2'], row['label']])
        if descript_2 != "nan":
            n_rows.append([row['var_1'], row['description_1'], row['var_2'], "", row['label']])
    n_df = pd.DataFrame(columns=df.columns, data=n_rows)
    num_ones = len(n_df[n_df['label']== 1])
    num_zeros = len(n_df[n_df['label'] == 0])

    m = min(num_ones, num_zeros)

    new_df = pd.concat([df,n_df[n_df['label']== 1].sample(n=m),n_df[n_df['label'] == 0].sample(n=m)])
    new_df = new_df.sample(frac=1).reset_index(drop=True)
    #new_df.to_csv(dataset, index=False)
# %%

import pandas as pd

PATH = "../data/"

dataframes = []

for dataset in ["../data/dev_v3.csv", "../data/test_v3.csv", "../data/train_v3.csv"]:
    dataframes.append(pd.read_csv(dataset))

# %%
df = pd.concat(dataframes)
# %%
df[df['label'] == 1].shape
# %%
