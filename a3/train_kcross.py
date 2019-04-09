# scikit-learn k-fold cross-validation
import numpy as np 
import pandas as pd
from sklearn.model_selection import KFold
# data sample
# data = array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
df = pd.read_csv("sample_data_comp4106_SAVED.csv")
df = df.drop(df.columns[0], axis=1)
data = df.values.tolist()

# prepare cross validation
kfold = KFold(3, True, 1)
# enumerate splits
for train, test in kfold.split(data):
	print('train: %s, test: %s' % (data[train], data[test]))
