import pandas as pd
from pycaret.classification import *


df = pd.read_csv('./data/Maternal Health Risk Data Set.csv')
df.head()

df.info()

setup = setup(data = df,
            target = 'RiskLevel', 
            fix_imbalance = True,
            train_size = 0.8,
            normalize = True,
            numeric_features= ['Age','SystolicBP','DiastolicBP','BS','BodyTemp','HeartRate'],
            feature_interaction = True, 
            feature_ratio = True,
            polynomial_features = True,
            group_features = ['SystolicBP', 'DiastolicBP'],
            bin_numeric_features = ['Age','SystolicBP','DiastolicBP','BS','BodyTemp','HeartRate'],
            fold = 5,
            log_experiment = True, 
            experiment_name = 'Mental Health Risk')

lightgbm = create_model('lightgbm')

from scipy.stats import randint as sp_randint
from scipy.stats import uniform as sp_uniform
grid ={'num_leaves': sp_randint(6, 50), 
             'min_child_samples': sp_randint(100, 500), 
             'min_child_weight': [1e-5, 1e-3, 1e-2, 1e-1, 1, 1e1, 1e2, 1e3, 1e4],
             'subsample': sp_uniform(loc=0.2, scale=0.8), 
             'colsample_bytree': sp_uniform(loc=0.4, scale=0.6),
             'reg_alpha': [0, 1e-1, 1, 2, 5, 7, 10, 50, 100],
             'reg_lambda': [0, 1e-1, 1, 5, 10, 20, 50, 100]}


import numpy as np
lgbm_params = {'num_leaves': np.arange(10,200,10),
                'max_depth': [int(x) for x in np.linspace(10, 110, num = 11)],
                'learning_rate': np.arange(0.1,1,0.1)
                }


tuned_lightgbm = tune_model(lightgbm, 
                        custom_grid=grid, 
                        optimize='f1',
                        choose_better= True, 
                        fold = 5,
                        n_iter = 5000)

final_lightgbm = finalize_model(tuned_lightgbm)

save_model(final_lightgbm, 'model')
