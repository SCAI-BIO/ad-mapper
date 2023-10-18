# %%
import sys
sys.path.append("./models")
from models import BertMapper
from models import prepare_data_for_BERT as prepare_data
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



BATCH_SIZE = 16
train_loader = DataLoader(train_data, batch_size=BATCH_SIZE)
validation_loader = DataLoader(validation_data, batch_size=BATCH_SIZE)


config = {
    "version": "dmis-lab/biobert-v1.1", 
    "dropout": 0.3, 
    "lr": 2e-5, 
    "weight_decay": 5e-3
}

device = "gpu" if cuda.is_available() else "cpu"
logger = TensorBoardLogger(save_dir="tb-logs/", name="BaseTrainLogs")
#logger = WandbLogger(project="MappingAssistent", name="bioBERT_V3_dataset")
trainer = Trainer(logger=logger, max_epochs=8,accelerator=device, gpus=1, callbacks=[EarlyStopping('val_loss'), ])

# %%
model = BertMapper(config)
trainer.fit(model, train_dataloaders=train_loader, val_dataloaders=validation_loader)


save(model.state_dict(), "bioBERT_ai_mapper_v4_dataset.pth")
   


    


# %%
