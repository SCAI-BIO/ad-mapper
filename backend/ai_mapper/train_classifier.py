# %%
import sys
sys.path.append("./models")
from models import BertMapperCl
from models import prepare_data_fro_BERT_classifier as prepare_data
from torch import cuda
import pandas as pd
from torch.utils.data import DataLoader
from pytorch_lightning import Trainer
from pytorch_lightning.loggers import WandbLogger, TensorBoardLogger
from pytorch_lightning.callbacks import EarlyStopping
from torch import save



# %%


train_data = prepare_data(pd.read_csv("data/train_v3.csv"))
validation_data = prepare_data(pd.read_csv("data/dev_v3.csv"))


#if set(train_data) & set(validation_data):
    #raise Exception("Non-empty intersection")
# %%

BATCH_SIZE = 12
train_loader = DataLoader(train_data, batch_size=BATCH_SIZE)
validation_loader = DataLoader(validation_data, batch_size=BATCH_SIZE)


config = {
    "version": "dmis-lab/biobert-v1.1", 
    "dropout": 0.163, 
    "lr": 5.636e-5, 
    "weight_decay": 0.0669, 
    "emb_path": "embedding_spaces/embedding_space_13_5.pkl"
}

device = "gpu" if cuda.is_available() else "cpu"
logger = TensorBoardLogger(save_dir="tb-logs/", name="ClassifierTrainLogs")
#logger = WandbLogger(project="MappingAssistent", name="Classifier_bioBERT_V1_dataset")
trainer = Trainer(logger=logger, max_epochs=75,accelerator=device, gpus=1)#, callbacks=[EarlyStopping("accuracy", patience=30)])

# %%
model = BertMapperCl(config)
trainer.fit(model, train_dataloaders=train_loader, val_dataloaders=validation_loader)

save(model.state_dict(), "bioBERT_classifier_v4_optimized_dataset_75_epochs.pth")
   
# %%
