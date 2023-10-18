# %%
from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained("dmis-lab/biobert-v1.1")
sequence_a = "(G_and_S_paracentral)ThickAvg"

encoded_dict = tokenizer(sequence_a)
decoded = tokenizer.decode(encoded_dict["input_ids"])

# %%
encoded_dict
# %%

