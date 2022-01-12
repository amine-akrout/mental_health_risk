import uvicorn
from fastapi import FastAPI
from fastapi import Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import pandas as pd
from pycaret.classification import *

model=load_model('model')


app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates/")
app.mount("/templates", StaticFiles(directory="templates", html=True), name="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
def app_post(request: Request, 
                age: float= Form(...),
                sbp: float= Form(...),
                dbp: float= Form(...),
                bs: float= Form(...),
                bt: float= Form(...),
                hr: float= Form(...)):
    data = [[age, sbp,	dbp, bs, bt, hr]]
    cols = ['Age', 'SystolicBP', 'DiastolicBP', 'BS', 'BodyTemp', 'HeartRate']

    data_unseen = pd.DataFrame(data, columns = cols)
    prediction= predict_model(model, data=data_unseen, round = 0)
    preds= prediction.Label[0]
    print(preds)
    
    print('Python module executed successfully')
    message = 'Risk Level : {} !'.format(preds.split(' ', 1)[0].title())

    return templates.TemplateResponse('index.html', context={'request': request, 'message': message})
