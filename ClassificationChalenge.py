"""
Created on Mon Aug  6 13:51:08 2018
@author: Ruslan Mamedov
"""
#Classification Challenge

#Importing the libraries
import pandas as pd
import numpy as np

# Suppress warnings from pandas
import warnings
warnings.filterwarnings('ignore')

#importing the dataset
dataset_train=pd.read_csv('application_train.csv')
dataset_test =pd.read_csv('application_test.csv')
dataset_train.head()

#replacing nonumeric binary columns with numeric values
dataset_train['FLAG_OWN_REALTY'].replace(('Y', 'N'), (1, 0), inplace=True)
dataset_train['FLAG_OWN_CAR'].replace(('Y', 'N'), (1, 0), inplace=True)
dataset_train['EMERGENCYSTATE_MODE'].replace(('No', 'Yes'), (1, 0), inplace=True)
dataset_train['CODE_GENDER'].replace(('M', 'F'), (0, 1), inplace=True)

dataset_test['FLAG_OWN_REALTY'].replace(('Y', 'N'), (1, 0), inplace=True)
dataset_test['FLAG_OWN_CAR'].replace(('Y', 'N'), (1, 0), inplace=True)
dataset_test['EMERGENCYSTATE_MODE'].replace(('No', 'Yes'), (1, 0), inplace=True)
dataset_test['CODE_GENDER'].replace(('M', 'F'), (0, 1), inplace=True)

#there are 13 nonnumeric columns; will have to convert them with one hot encoder. Then we'll take care of the missing values
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
labelencoder=LabelEncoder()
onehotencoder=OneHotEncoder()
for column in range(0-121):
    if dataset_train[column].type=='object':
        dataset_train[column]=labelencoder.fit_transform[dataset_test[column]]
    if dataset_test[column].type=='object':
        dataset_test[column]=labelencoder.fit_transform[dataset_test[column]]
        
dataset_train=pd.get_dummies(dataset_train)
dataset_test=pd.get_dummies(dataset_test)

#imputing missing values with a mean
dataset_train=dataset_train.fillna(dataset_train.mean())
dataset_test=dataset_test.fillna(dataset_test.mean())

# Dimension Reduction - dropping the features with less than 2% correllation
correlations = dataset_train.corr()['TARGET'].sort_values()
correlations = correlations.reset_index().values
print(dataset_train.shape)
for column in range (0,len(correlations)-1):
    if correlations[column,1]>-0.02 and correlations[column,1]<0.02 and correlations[column,0]!='SK_ID_CURR':
        dataset_train=dataset_train.drop ([correlations[column,0]], axis=1)
print(dataset_train.shape)
correlations = dataset_train.corr()['TARGET'].sort_values()
print('Most Positive Correlations:\n', correlations.tail(15))
print('\nMost Negative Correlations:\n', correlations.head(15))

# Align the training and testing data, keep only columns present in both dataframes
train_labels = dataset_train['TARGET']
dataset_train, dataset_test = dataset_train.align(dataset_test, join = 'inner', axis = 1)
# Add the target back in
dataset_train['TARGET'] = train_labels

#Splitting train dataset, training the model
y=dataset_train.iloc[:,dataset_train.columns.get_loc('TARGET')].values
X=dataset_train.drop(['TARGET'], axis=1).values

# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Fitting Random Forest Classification to the Training set
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)
'''# Applying Grid Search to tune up the model - if needed
from sklearn.model_selection import GridSearchCV
cv_params = {'max_depth': [1,2,3,4,5,6], 'min_child_weight': [1,2,3,4]}    # parameters to be tries in the grid search
fix_params = {'learning_rate': 0.2, 'n_estimators': 100, 'objective': 'binary:logistic'}   #other parameters, fixed for the moment 
csv = GridSearchCV(XGBClassifier(**fix_params), cv_params, scoring = 'roc_auc', cv = 5)
csv.fit(X_train, y_train)
print(csv.best_params_)
cv_params = {'subsample': [0.8,0.9,1], 'max_delta_step': [0,1,2,4]}
fix_params = {**csv.best_params_, **fix_params}
csv.fit(X_train, y_train)
fix_params.pop('learning_rate', None)
cv_params = {'learning_rate': [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]}
fix_params = {**csv.best_params_, **fix_params}
csv.fit(X_train, y_train)
#applying best parameters from the grid search
print ('csv.best_params_')
classifier = XGBClassifier(**csv.best_params_)'''

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Confusion Matrix - to determine if the model is a good fit -true positives/fp/tn/fn
from sklearn.metrics import confusion_matrix
print (dataset_train.shape)
cm = confusion_matrix(y_test,y_pred)
print(cm)     


'''
#For the competition: realligning two datasets
dataset_train, dataset_test = dataset_train.align(dataset_test, join = 'inner', axis = 1)
X=dataset_train.values
classifier.fit(X, y)
X_test=dataset_test.values
y_pred = classifier.predict_proba(X_test)[:, 1]
# Submission dataframe
submit = dataset_test[['SK_ID_CURR']]
submit['TARGET'] = y_pred
submit.head()
# Save the submission to a csv file
submit.to_csv('XGBoostClassification.csv', index = False)
'''
