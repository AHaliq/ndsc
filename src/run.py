import csv
import numpy as np
import xgboost as xgb
from xgboost import XGBClassifier
import datetime
import pandas as pd
from random import randint
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold

features = ['title','group','english',"f5","blush","ram","neck","year","loose","cream","winner","maxi","hot","xperia","white","soft","control","bb","7a","foundation","face","setting","gel","wedding","spf","etude","water","cc","tablet","prime","aquos","limited","primer","vandroid","b81","moto","z5","tam","motorola","sh","plus","powder","lipstick","samsung","size","max","maxtron","2051d","matte","galaxy","warranty","sim","p12","c1","cover","7","vibe","liner","oppo","color","pernikahan","short","stick","s3","mate","lip","1054d","woman","prince","highlighter","house","lace","bronzer","nyx","dress","note","105","cushion","without","6","big","v9","1","android","party","balm","4","blouse","polos","buy","oil","brocade","tint","palette","mini","4g","andromax","concealer","ingredients","pencil","m1","32gb","64gb","bioaqua","mi","skin","long","spray","z3","arm","dual","smartfren","acne","contour","pro","duo","shirt","lte","gloss","9i","liquid","sexy","black","mist","2","aurora","model"]
# train_df = pd.read_csv("../data/clean/train_translated_numeric.csv")
# test_df = pd.read_csv('../data/clean/test_englishfeature.csv')

train_df = pd.read_csv("train.csv")
test_df = pd.read_csv('test.csv')


# drop image_path
del train_df['image_path']
del train_df['itemid']

# convert text to npfloat
labelencoder = LabelEncoder()
train_df['title'] = labelencoder.fit_transform(train_df['title'])
test_df['title'] = labelencoder.fit_transform(test_df['title'])

y = train_df['Category']
X = train_df[features]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

print('------ training model ------')
# grid search
# model = XGBClassifier()
# n_estimators = range(50, 400, 50)
# param_grid = dict(n_estimators=n_estimators)
# print('------ training model : k-fold ------')
# kfold = StratifiedKFold(n_splits=2, shuffle=True, random_state=7)
# print('------ training model : grid search ------')
# grid_search = GridSearchCV(model, param_grid, scoring="neg_log_loss", n_jobs=-1, cv=kfold)
# grid_result = grid_search.fit(X_train, y_train)

# print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
# means = grid_result.cv_results_['mean_test_score']
# stds = grid_result.cv_results_['std_test_score']
# params = grid_result.cv_results_['params']

model = xgb.XGBClassifier(max_depth=2, n_estimators=4, learning_rate=0.05)

# model = XGBClassifier()
print('------ fitting model ------')
model.fit(X_train, y_train)


# make predictions for test data
print('------ predicting test ------')
y_pred = model.predict(X_test)
predictions = [round(value) for value in y_pred]

# evaluate predictions
print('------ acc score ------')
accuracy = accuracy_score(y_test, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100.0))

# make predictions on test data
print('------ predicting ../data/clean/test_englishfeature.csv ------')
y_pred = model.predict(test_df[features])
data_info_val_sample_submission  = pd.DataFrame(columns = ['itemid','Category'])
data_info_val_sample_submission['itemid'] = test_df['itemid']
data_info_val_sample_submission['Category'] = y_pred
data_info_val_sample_submission.to_csv('data_info_val_sample_submission.csv',mode = 'w', index=False)

