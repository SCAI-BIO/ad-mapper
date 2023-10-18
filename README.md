# Mapping Assistent 




## Set up 

## Backend
In the base directory do: 
```bash
export PYTHONPATH=$(pwd):PYTHONPATH
```
In the backend directory do: 
```bash
export BASEDIR=$(pwd)
```


Install backend/requirements.txt using  
```bash
pip install -r backend/requirements.txt
```
## Frontend

In the frontend folder do:

```bash
npm i . 
```
And adjust the VUE_APP_API variable in .env.development(/production) if necessary. 

## Run everything 
_Backend_: In the backend folder: ```uvicorn main:app```
_Frontend_: ```npm run serve```



