from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
import numpy as np
import pandas as pd
import joblib

def train_decision_tree(X_train, y_train, params):
    dt = DecisionTreeClassifier(**params)
    dt.fit(X_train, y_train)
    return dt

def train_random_forest(X_train, y_train, params):
    rf = RandomForestClassifier(**params)
    rf.fit(X_train, y_train)
    return rf

def tune_hyperparameters(X_train, y_train):
    dt_params = {
        'max_depth': [None, 10, 20, 30, 40, 50],
        'min_samples_split': [2, 5, 10]
    }
    
    rf_params = {
        'n_estimators': [10, 50, 100],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10]
    }
    
    dt_grid = GridSearchCV(DecisionTreeClassifier(), dt_params, cv=5)
    rf_grid = GridSearchCV(RandomForestClassifier(), rf_params, cv=5)
    
    dt_grid.fit(X_train, y_train)
    rf_grid.fit(X_train, y_train)
    
    return dt_grid.best_estimator_, rf_grid.best_estimator_

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred)
    return report

def save_model(model, filename):
    joblib.dump(model, filename)