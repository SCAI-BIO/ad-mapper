# Mapping Assistent 




## Set up 
Download the model files from here: https://drive.google.com/file/d/14AdB9NUEVGESfck-GDScFqwQld1G-5_s/view?usp=sharing and https://drive.google.com/file/d/1E2XkUM7i1oXnRvXT5OjL1l-CXjeTzCuS/view?usp=sharing and place then in backend/ai_mapper. 
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



