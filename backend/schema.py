
from pydantic import BaseModel, FilePath

# Define the schema for the mapping

class Mapping(BaseModel):
    '''
    Model for mapping data
    '''
    external_variable: str
    internal_variable: str
    source: str
    

class Variable(BaseModel):
    '''
    Model for variable data
    '''
    name: str
    var_description: str
    

class ExternalVariable(BaseModel):
    '''
    Model for incoming variables that need to be mapped
    '''
    var: str
    var_description: str

class AIMapperOutputModel(BaseModel):
    '''
    Model for mapper response
    '''

    class_props: dict = {}
    winner: list = []

class AIMapperOutputModelCSV(BaseModel):


    file: str = ""
