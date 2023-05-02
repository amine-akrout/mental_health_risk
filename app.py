"""
Module to run the app
"""
# pylint: disable=E0401,E0611,R0903
import warnings
from fastapi import FastAPI, Request, Body
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from loguru import logger
import pandas as pd
from pycaret.classification import predict_model, load_model
from pydantic import BaseModel

warnings.filterwarnings("ignore")
app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates/")
app.mount("/templates", StaticFiles(directory="templates",
          html=True), name="templates")


class InputData(BaseModel):
    """
    Class to define the input data
    """
    age: float
    sbp: float
    dbp: float
    bs: float
    bt: float
    hr: float


models = {}


@app.on_event("startup")
def start_load_model():
    """ Function to load the model on startup """
    logger.info("Loading the model...")
    models['model'] = load_model('model')


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """ Function to serve the home page """
    logger.info("Serving the home page...")
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict")
async def app_post(request: Request, input_data: InputData = Body(...)) -> dict:
    """
    Function to make the prediction using the model trained in training.py
    """
    # Get the input data from the Pydantic model
    data = [[input_data.age, input_data.sbp, input_data.dbp,
             input_data.bs, input_data.bt, input_data.hr]]
    cols = ['Age', 'SystolicBP', 'DiastolicBP', 'BS', 'BodyTemp', 'HeartRate']
    data_unseen = pd.DataFrame(data, columns=cols)
    # Make the prediction using the PyCaret model
    prediction = predict_model(models['model'], data=data_unseen, round=0)
    preds = prediction.Label[0]
    logger.info(f"Prediction: {preds}")
    # Prepare the response message
    message = 'Risk Level : {} !'.format(preds.split(' ', 1)[0].title())

    return templates.TemplateResponse('index.html',
                                      context={'request': request, 'message': message})
