"""
Module for training and saving the model.
"""
# pylint: disable=E1101, E0401
import os
import sys
import warnings
import pandas as pd
import numpy as np
from loguru import logger
from pycaret.classification import setup, create_model, tune_model, finalize_model, save_model
from scipy.stats import randint as sp_randint
from scipy.stats import uniform as sp_uniform

warnings.filterwarnings("ignore")


# ignore warnings : https://github.com/pycaret/pycaret/discussions/1951
if not sys.warnoptions:
    warnings.simplefilter("ignore")
    os.environ["PYTHONWARNINGS"] = "ignore"

# read the data
mhr_data = pd.read_csv("./data/Maternal Health Risk Data Set.csv")
# convert the index to int
mhr_data.index = mhr_data.index.astype("int64")

logger.info("Data read successfully")
logger.info(
    f"Data read successfully: shape={mhr_data.shape}, columns={mhr_data.columns}")
logger.info(f"Data head: {mhr_data.head()}")
logger.info(f"Data info: {mhr_data.info()}")


setup_params = {
    "data": mhr_data.head(100),
    "target": "RiskLevel",
    "fix_imbalance": True,
    "train_size": 0.8,
    "normalize": True,
    "numeric_features": [
        "Age",
        "SystolicBP",
        "DiastolicBP",
        "BS",
        "BodyTemp",
        "HeartRate",
    ],
    "feature_interaction": True,
    "feature_ratio": True,
    "polynomial_features": True,
    "group_features": ["SystolicBP", "DiastolicBP"],
    "bin_numeric_features": [
        "Age",
        "SystolicBP",
        "DiastolicBP",
        "BS",
        "BodyTemp",
        "HeartRate",
    ],
    "fold": 5,
    "log_experiment": True,
    "experiment_name": "Mental Health Risk",
    "silent": True
}

logger.info("Setting up")
setup_ret = setup(**setup_params)
logger.info("Setup completed successfully")


logger.info("Creating model")
lightgbm = create_model("lightgbm")
logger.info("Model created successfully")

grid = {"num_leaves": sp_randint(6, 50),
        "min_child_samples": sp_randint(100, 500),
        "min_child_weight": [1e-5, 1e-3, 1e-2, 1e-1, 1, 1e1, 1e2, 1e3, 1e4],
        "subsample": sp_uniform(loc=0.2, scale=0.8),
        "colsample_bytree": sp_uniform(loc=0.4, scale=0.6),
        "reg_alpha": [0, 1e-1, 1, 2, 5, 7, 10, 50, 100],
        "reg_lambda": [0, 1e-1, 1, 5, 10, 20, 50, 100]}


lgbm_params = {"num_leaves": np.arange(10, 200, 10),
               "max_depth": [int(x) for x in np.linspace(10, 110, num=11)],
               "learning_rate": np.arange(0.1, 1, 0.1)
               }

logger.info("Tuning model")
tuned_lightgbm = tune_model(lightgbm,
                            custom_grid=grid,
                            optimize="f1",
                            choose_better=True,
                            fold=5,
                            n_iter=100)
logger.info("Model tuned successfully")


logger.info("Finalizing model")
final_lightgbm = finalize_model(tuned_lightgbm)
logger.info("Model finalized successfully")

logger.info("Saving model")
save_model(final_lightgbm, "model")
logger.info("Model saved successfully")
