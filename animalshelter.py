__author__ = 'Stella'
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder, LabelBinarizer, Imputer, OneHotEncoder

'''OutcomeSubtype AnimalType SexuponOutcome AgeuponOutcome
AnimalID        Name             DateTime      OutcomeType '''


def prepareData(train):
    train['Sex'] = train.SexuponOutcome.apply(get_sex)
    train['Neutered'] = train.SexuponOutcome.apply(get_neutered)
    train['Mix'] = train.Breed.apply(get_mix)
    train['AgeuponOutcome'] = train.AgeuponOutcome.apply(calc_age_in_years)
    return train

def loadData():
    train = pd.read_csv('train.csv')
    test = pd.read_csv('test.csv')
    train = prepareData(train)
    test = prepareData(test)

    y = train.OutcomeType
    train.drop(["Name", "OutcomeType","SexuponOutcome","DateTime","AnimalID"], axis=1, inplace=True)
    test.drop(["Name", "SexuponOutcome","DateTime","ID"], axis=1, inplace=True)

    for var in ['AnimalType', 'Neutered','Mix','Breed','Sex']: # color is bad
        le = LabelEncoder().fit(train[var])
        train[var] = le.transform(train[var])
        test[var] = le.transform(test[var])

    yFit = LabelEncoder().fit(y)
    y = yFit.transform(y)

    clf = GridSearchCV(DecisionTreeClassifier(), param_grid={'max_depth':[4,5,6,7,8,9,10,12],
         'min_samples_split':[2, 5, 10, 15, 20, 25],'min_samples_leaf':[1, 2, 5, 8, 12, 15, 20]},
                       scoring='log_loss',n_jobs=-1)

    clf.fit(train, y)

def get_sex(x):
    x = str(x)
    if x.find('Male') >= 0: return 'male'
    if x.find('Female') >= 0: return 'female'
    return 'unknown'

def get_neutered(x):
    x = str(x)
    if x.find('Spayed') >= 0: return 'neutered'
    if x.find('Neutered') >= 0: return 'neutered'
    if x.find('Intact') >= 0: return 'intact'
    return 'unknown'


def get_mix(x):
    x = str(x)
    if x.find('Mix') >=0 :
        return 'mix'
    return 'not'




def calc_age_in_years(x):
    x = str(x)
    if x == 'nan': return 0
    age = int(x.split()[0]) # split with space, get number
    if x.find('year')> -1: return age
    if x.find('month')> -1: return age/12
    if x.find('week') > -1 : return age/52
    if x.find('day') > -1 : return age/365
    else : return 0



