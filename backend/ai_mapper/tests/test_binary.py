# %%
import sys
import pandas as pd
sys.path.append("..")
sys.path.append("../models/")
#sys.path.append("models")
import torch 

from pytorch_lightning.loggers import WandbLogger, TensorBoardLogger
from pytorch_lightning import Trainer
from torch.utils.data import DataLoader


from models import BertMapperCl, BertMapper
from models import prepare_data_fro_BERT_classifier, prepare_data_for_BERT

config = {
    "version": "dmis-lab/biobert-v1.1", 
    "dropout": 0.3, 
    "lr": 2e-5, 
    "weight_decay": 5e-3, 
    "emb_path": "../embedding_spaces/embedding_space.pkl"
}

model = BertMapper(config)

model.load_state_dict(torch.load("../bioBERT_ai_mapper_v3_dataset.pth"))


# %%

test_data = prepare_data_for_BERT(pd.read_csv("../data/test_v3.csv"))

# %%

device = "gpu" if torch.cuda.is_available() else "cpu"
logger = TensorBoardLogger(save_dir="tb_logs", name="test_binary_metrics")
trainer = Trainer(logger=logger, max_epochs=150,accelerator=device, gpus=1)

trainer.test(model, DataLoader(test_data, batch_size=16))

# %%