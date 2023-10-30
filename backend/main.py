import os
from uuid import uuid4
os.environ['KMP_DUPLICATE_LIB_OK']='True' ## don't know why :(
import torch
import requests

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000/")

BACKEND_URL="https://ad-mapper.scai.fraunhofer.de/api/"


from fastapi import FastAPI, File, HTTPException, UploadFile

from fastapi.responses import FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
import io, threading

from schema import Mapping, Variable, ExternalVariable, AIMapperOutputModel, AIMapperOutputModelCSV

from settings import BASEDIR

from Levenshtein import ratio
from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained("dmis-lab/biobert-v1.1")

print("Load models...")

from ai_mapper.models.bert import MappingModel as mapping_model

from ai_mapper.models.classifier_bert import MappingModelCl as mapper_classifier
from ai_mapper.models.classifier_bert import find_nearest_k

import pandas as pd

mapper_data = pd.read_csv(os.path.join(BASEDIR, "ai_mapper/embedding_spaces/CDM/ad-mapper_data.csv"))#.drop(columns=['AMED'])


mapper_data2 = pd.read_csv(os.path.join(BASEDIR, "ad-mapper_data.csv"))#.drop(columns=['AMED'])

#from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware

## Supertokens initialization
print("Loading FASTAPI...")


version="0.2.9"


app = FastAPI(
    version=version,
)



origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("loading done")




# initial datamodel 

# CDM_PATH = "/Users/philippwegner/Desktop/Fraunhofer/cdm-ndd/datamodels/Datamodel_6_5_22.xlsx"

# attribute_sheet = pd.read_excel(CDM_PATH, sheet_name='Attributes')



def load_model_files():
    if not os.path.exists(os.path.join(BASEDIR, "ai_mapper","bioBERT_ai_mapper_v3_dataset.pth" )):
        print("Downloading model files...")
        r = requests.get("https://huggingface.co/phwegn/ad-mapper/resolve/main/bioBERT_ai_mapper_v3_dataset.pth")
        with open(os.path.join(BASEDIR, "ai_mapper","bioBERT_ai_mapper_v3_dataset.pth" ), 'wb') as f:
            f.write(r.content)
    if not os.path.exists(os.path.join(BASEDIR, "ai_mapper","bioBERT_classifier_v3_optimized_dataset_60_epochs.pth" )):
        print("Downloading model files...")
        r = requests.get("https://huggingface.co/phwegn/ad-mapper/resolve/main/bioBERT_classifier_v3_optimized_dataset_60_epochs.pth")
        with open(os.path.join(BASEDIR, "ai_mapper","bioBERT_classifier_v3_optimized_dataset_60_epochs.pth" ), 'wb') as f:
            f.write(r.content)




load_model_files()
## initialte ai-model 

config = {
    "version": "dmis-lab/biobert-v1.1", 
    "dropout": 0.3, 
    "lr": 2e-5, 
    "weight_decay": 5e-3, 
    "emb_path": os.path.join(BASEDIR, "ai_mapper/embedding_spaces/embedding_space_filtered.pkl")
}

mapping_model = mapping_model(config)

mapping_model.load_state_dict(torch.load(os.path.join(BASEDIR, "ai_mapper/bioBERT_ai_mapper_v3_dataset.pth")))
mapping_model.eval()

mapper_classifier = mapper_classifier(config)
mapper_classifier.load_state_dict(torch.load(os.path.join(BASEDIR, "ai_mapper/bioBERT_classifier_v3_optimized_dataset_60_epochs.pth")))
mapper_classifier.eval()




##
#  Endpoints
##
@app.get("/")
def read_root():
    return {"Message": "Welcome to the Mapping Assistant"}



##
# Main mappings function
##


@app.get("/v1/ai-mapper", response_model = AIMapperOutputModel)
async def ai_mapping(variable_name : str = None, variable_description : str = None):
    return {
        "Message": "Deprecated. Please use /v2/ai-mapper"
    }
    # w_1, w_2 = 0.5, 0.5 # maybe learnable
    # CHUNK_SIZE = 128
    # if not (variable_name or variable_description):
    #     return {
    #         'class_props': {},
    #         'winner': []
    #     }
    # sentence_a = variable_name if variable_name else "" + " " + variable_description if variable_description else ""
    
    # class_propabilities = {}
    # total = len(attribute_sheet)


    # sentence_b_chunk = {}


    # for i,row in attribute_sheet.iterrows():
        
    #     sentence_b = row['Attribute'] if str(row['Attribute']).lower() != 'nan' else "" + " " + row['Attribute_Description'] if str(row['Attribute_Description']).lower() != 'nan' else ""
    #     sentence_b_chunk[row['Attribute']] = sentence_b
    #     if i >0 and (i+1) % CHUNK_SIZE == 0 or (i == (len(attribute_sheet) - 1)):
    #         sentence_a_chunk = [sentence_a]*len(sentence_b_chunk)
            
    #         tokenized_chunk = tokenizer(sentence_a_chunk, list(sentence_b_chunk.values()),padding=True, return_tensors='pt')
    #         logits = mapping_model(tokenized_chunk).logits

    #         for k, logit in enumerate(logits):
    #             if torch.argmax(logit, dim=0).item() == 1:
    #                 class_propabilities[list(sentence_b_chunk.keys())[k]] = w_1*torch.squeeze(torch.softmax(logit, dim=0))[1].item() + w_2*ratio(sentence_a, list(sentence_b_chunk.values())[k])
    #         print(f"Compared {i+1}/{total} Variables...")
    #         sentence_b_chunk = {}

    # return {
    #     'class_props': class_propabilities,
    #     'winner': sorted(class_propabilities.items(), key=lambda x: x[1])[-1]
    # }

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


def map_variables_v2(variable_name : str = None, variable_description : str = None, k: int = 10, w_1: float = 1.0, w_2 : float = 0.0, bypass_binary: bool = False, class_prob_threshold: float = 0.5, usePriorMappings: bool = False, useDefinitions: bool =True, useSubstringMetric: bool = False):
    if not (variable_name or variable_description):
        return {
            'class_props': {},
            'winner': []
        }
    k = int(k)
    sentence_a = (variable_name.lower() if variable_name else "") + " " + (variable_description.lower() if variable_description else "")
    variable_tokenized = tokenizer(sentence_a, return_tensors='pt')
    result = mapper_classifier(variable_tokenized)
    predictions = find_nearest_k(mapper_classifier.embedding_CDM, result, k=k)
    
    predictions = [mapper_classifier.labels[l[0]] for l in predictions.tolist()]

    #print(predictions)
    if usePriorMappings:

        pre_known_variables = [mapper_data[mapper_data["Feature"].str.lower() == p] for p in predictions]

        cols = mapper_data.columns[2:]

        extra_vars = []
        extra_vars_no_definitions = []
        extra_vars_dict = {}
        for p in pre_known_variables:
            for c in cols:
                if len(p)>0:
                    if str(p[c].values[0]).lower() != "nan":
                        extra_info_no_definitions = str(p[c].values[0]).lower()
                        extra_info = str(p[c].values[0]).lower() + " " + str(p["Definition"].values[0]).lower()
                        extra_vars.append(extra_info)
                        extra_vars_no_definitions.append(extra_info_no_definitions)
                        extra_vars_dict[extra_info] = p["Feature"].values[0].lower()
                        extra_vars_dict[extra_info_no_definitions] = p["Feature"].values[0].lower()


        definitions = [str(p["Definition"].values[0]).replace("\n", "") if len(p) > 0 else "" for p in pre_known_variables]
    #definitions = [mapper_data['Feature'].str.lower() == p for p in predictions]
    definitions = [mapper_data[mapper_data['Feature'].str.lower() == p]['Definition'].values[0] if len(mapper_data[mapper_data['Feature'].str.lower() == p]) > 0 else "" for p in predictions]




    #print(predictions)
    if bypass_binary:
        
        return {
                'class_props': {p: 1/len(predictions) for p in predictions},
                'winner': [predictions[0]]
            }
    
    ## concat definitions to predictions
    predictions_with_definitions = [f"{p} {d}" for p,d in zip(predictions, definitions)]
    if usePriorMappings:
        
        predictions_with_definitions_and_extra_knowledge = predictions_with_definitions + extra_vars

    #print(predictions_with_definitions)

        predictions_to_use = predictions_with_definitions_and_extra_knowledge
    else:
        predictions_to_use = predictions_with_definitions


    if not useDefinitions:
        if usePriorMappings:
            predictions_to_use = predictions + extra_vars_no_definitions
        else:
            predictions_to_use = predictions

    
    tokenized_chunk = dict(tokenizer([sentence_a]*len(predictions_to_use), predictions_to_use ,padding=True, return_tensors='pt'))
    logits = mapping_model(tokenized_chunk).logits
    class_propabilities = {}
    for i, logit in enumerate(logits):
        class_prob = torch.softmax(logit, dim=0)[1].item()
        if class_prob > class_prob_threshold:
            if i < len(predictions):
                if useSubstringMetric:
                    if len(predictions[i]) == len(sentence_a):
                        shorter_word = predictions[i]
                        longer_word = sentence_a
                    else:
                        shorter_word = predictions[i] if len(predictions[i]) < len(sentence_a) else sentence_a
                        longer_word = predictions[i] if len(predictions[i]) > len(sentence_a) else sentence_a
                    valSubstringMetric = find_matching_substrings(longer_word, shorter_word, 3)/(len(shorter_word)-2)
                    class_propabilities[str(predictions[i])] = w_1*torch.squeeze(torch.softmax(logit, dim=0))[1].item() + w_2*valSubstringMetric
                else:
                    class_propabilities[str(predictions[i])] = w_1*torch.squeeze(torch.softmax(logit, dim=0))[1].item() + w_2*ratio(sentence_a,predictions_to_use[i])
            else:
                class_propabilities[extra_vars_dict[predictions_with_definitions_and_extra_knowledge[i]]] = w_1*torch.squeeze(torch.softmax(logit, dim=0))[1].item() + w_2*ratio(sentence_a,predictions_to_use[i])
        
 

    if len(class_propabilities)> 0:
        return {
                'class_props': class_propabilities,
                'winner': sorted(class_propabilities.items(), key=lambda x: x[1])[-1] 
            }
    else:
        return {
                'class_props': class_propabilities,
                'winner': ["No suitable variable found."]
            }



@app.get("/v2/ai-mapper", response_model = AIMapperOutputModel)
def ai_mapping_2(variable_name : str = None, variable_description : str = None, k: int = 10, w_1: float = 1.0, w_2 : float = 0.0, bypass_binary: bool = False, class_prob_threshold: float = 0.5, usePriorMappings: bool = False, useDefinitions: bool =True, useSubstringMetric: bool = False):
    return map_variables_v2(variable_name, variable_description, k, w_1, w_2, bypass_binary, class_prob_threshold, usePriorMappings, useDefinitions, useSubstringMetric)

# method to read csv and load it with pandas

def process_csv(df, variableColumnName, definitionColumnName, k, w_1, w_2, bypass_binary, class_prob_threshold, usePriorMappings, useDefinitions, useSubstringMetric, uuid):
    data = []
    columns = df.columns.tolist() + ['target', 'OMOP']
    total = len(df)
    with open(f"tmp/{uuid}.txt", "w") as f:
        f.write(f"Mapping {total} Variables...\n")
        f.write(f"This can take a couple of minutes")
    for i, row in df.iterrows():
        print(f"Mapping {i+1}/{total} Variables...")
        with open(f"tmp/{uuid}.txt", "a") as f:
            f.write(f"Mapping {i+1}/{total} Variables...\n")
        variable_name = row[variableColumnName] if str(row[variableColumnName]).lower() != "nan" else ""
        variable_description = row[definitionColumnName] if str(row[definitionColumnName]).lower() != "nan" else ""
        response = map_variables_v2(variable_name, variable_description, k, w_1, w_2, bypass_binary, class_prob_threshold, usePriorMappings, useDefinitions, useSubstringMetric)
        winner = response['winner'][0]
        omop = mapper_data[mapper_data['Feature'].str.lower() == winner]['OMOP'].values[0] if len(mapper_data[mapper_data['Feature'].str.lower() == winner]) > 0 else ""
        row_to_add = list(row) + [winner, omop]
        data.append(row_to_add)
    pd.DataFrame(data, columns=columns)
    pd.DataFrame(data, columns=columns).to_csv(f'tmp/{uuid}.csv')
    os.remove(f"tmp/{uuid}.txt")

@app.get("/running-processes", response_model = list)
def running_processes():
    return list([txt.replace(".txt", "") for txt in filter(lambda x: x.endswith(".txt"), os.listdir("tmp"))])



@app.post("/v2/csv-mapper", response_model = AIMapperOutputModelCSV )
async def ai_mapping_2_csv(csvFile: UploadFile, variableColumnName: str = "Variable", definitionColumnName: str = "Definition", k: int = 10, w_1: float = 1.0, w_2 : float = 0.0, bypass_binary: bool = False, class_prob_threshold: float = 0.5, usePriorMappings: bool = False, useDefinitions: bool =True, useSubstringMetric: bool = False, return_all_mappings: bool = False, delimiter: str = ";"):
    
    file_content = csvFile.file.read()


    ## try different encodings
    encodings = ["utf-8", "unicode_escape", "cp1252", "ISO-8859-1", "", "ENDING"]

    for encoding in encodings:
        if encoding == "ENDING":
            return Response(status_code=500, content=f"Could not read csv file. Please Check encoding -->one of {encodings} required", media_type="text/plain")
        try:
            df = pd.read_csv(io.StringIO(file_content.decode('utf-8')), sep=delimiter, encoding=encoding)
            break
        except Exception as e:
            print(e)
            continue
            
    if len(df.columns.tolist()) < 2:
        return Response(status_code=500, content="CSV file does not contain enough columns. Maybe not ; as seperator?", media_type="text/plain")

    if variableColumnName not in df.columns.tolist():
        return Response(status_code=500, content="Variable column name not found in csv file.", media_type="text/plain")
    if definitionColumnName not in df.columns.tolist():
        return Response(status_code=500, content="Definition column name not found in csv file.", media_type="text/plain")

    uuid = str(uuid4())

    if len(df) > 15:
        print(f"Starting mapping process in background. You can download the file at {BACKEND_URL}download/{uuid}")
        thread = threading.Thread(target=process_csv, args=(df, variableColumnName, definitionColumnName, k, w_1, w_2, bypass_binary, class_prob_threshold, usePriorMappings, useDefinitions, useSubstringMetric, uuid, ) )
        thread.start()
        message = f"Found more than 15 rows. Starting mapping process in background. You can download the file in a few minutes at {BACKEND_URL}download/{uuid}"
    else:
        print(f"Starting mapping process. You can download the file at {BACKEND_URL}download/{uuid}")
        process_csv(df, variableColumnName, definitionColumnName, k, w_1, w_2, bypass_binary, class_prob_threshold, usePriorMappings, useDefinitions, useSubstringMetric, uuid)
        message = f"Mapping process finished. You can download the file at {BACKEND_URL}download/{uuid}"

    #print(BACKEND_URL)
    return {
        "file": BACKEND_URL + "download/" + uuid, 
        "message": message
    }


# download files

@app.get("/download/{uuid}")
def download(uuid: str):
    if os.path.exists(f"tmp/{uuid}.csv"):
        return FileResponse(f'tmp/{uuid}.csv')
    else:
        if os.path.exists(f"tmp/{uuid}.txt"):
            with open(f"tmp/{uuid}.txt", "r") as f:
                return Response(content=f.read(), media_type="text/plain")
        else:

            return Response(status_code=404, content="File not found. If you got this link as an output of a mapping process retry in a couple of minutes.", media_type="text/plain")

@app.get("/download-cdm")
def download_cdm():
    return FileResponse("ad-mapper_data.csv")


@app.get("/get-cdm-as-json")
def get_cdm_as_csv():
    
    return mapper_data2.fillna("").to_dict(orient="records")
    

# POST variable
@app.post("/variable")
def create_variable(variable: Variable):
    
    return {"Message": "Variable created", "variable": None}

# GET all variables
@app.get("/variables")
def get_variables():
    variables = mapper_data.Feature.tolist()
    return variables


# POST mapping
@app.post("/add-mapping/")
def add_mapping(mapping: Mapping, response_model: Mapping):
    
    return {"message": "Not yet implemented."}


# GET mappings
@app.get("/mappings/")
def get_mappings():
    mappings = mapper_data.to_dict(orient="records")
    
    return mappings

@app.get("/mappings/{internal_variable}")
def get_mappings(internal_variable: str):
    sub_df = mapper_data[mapper_data["Feature"].str.lower() == internal_variable.lower()]
    if len(sub_df) > 0:
        return sub_df.to_dict(orient="records")
    else:
        return {"message": "No mappings found."}
    

