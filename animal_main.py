import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder, LabelBinarizer, Imputer, OneHotEncoder

train = pd.read_csv("train.csv")
train = train.drop(["Name", "OutcomeSubtype"], axis=1)
test = pd.read_csv("test.csv")
test = test.drop(["Name"], axis=1)

# Split up information in SexuponOutcome

def split_sexuponoutcome(dataset):
    sex_split = [str(s).split() for s in dataset.SexuponOutcome]
    sterilizationStatus = [s[0] if len(s) == 2 else "Unknown" for s in sex_split]
    sex = [s[1] if len(s) == 2 else "Unknown" for s in sex_split]
    return sterilizationStatus, sex

def get_neutered(x):
    x = str(x)
    if x.find('Spayed') >= 0: return 'neutered'
    if x.find('Neutered') >= 0: return 'neutered'
    if x.find('Intact') >= 0: return 'intact'
    return 'unknown'

train['Neutered'] = train.SexuponOutcome.apply(get_neutered)
test['Neutered'] = train.SexuponOutcome.apply(get_neutered)

sterile_train, sex_train = split_sexuponoutcome(train)
sterile_test, sex_test = split_sexuponoutcome(test)

train['Sex'], train['SterilizationStatus'] = pd.Series(sex_train), pd.Series(sterile_train)
test['Sex'], test['SterilizationStatus'] = pd.Series(sex_test), pd.Series(sterile_test)
train = train.drop('SexuponOutcome', axis=1)
test = test.drop('SexuponOutcome', axis=1)


# Convert AgeuponOutcome to days


def convert_ages_to_days(dataset):
    ages = [str(a).split() for a in dataset.AgeuponOutcome]
    ages_in_days = []
    for a in ages:
        if len(a) != 2:
            ages_in_days.append(np.nan)
        else:
            value, unit = int(a[0]), a[1]
            if unit == 'year' or unit == 'years':
                ages_in_days.append(365 * value)
            elif unit == 'month' or unit == 'months':
                ages_in_days.append(30 * value)
            elif unit == 'week' or unit == 'weeks':
                ages_in_days.append(7 * value)
            elif unit == 'day' or unit == 'days':
                ages_in_days.append(value)
            else:
                raise Exception('Data is in inconsistent format.', 'value:', value, 'unit:', unit)
    return ages_in_days


ages_in_days_train = convert_ages_to_days(train)
ages_in_days_test = convert_ages_to_days(test)
# TODO: train random forest or nearest neighbors to predict age and impute NaN values

train_age_mean = np.nanmedian(ages_in_days_train)
test_age_mean = np.nanmedian(ages_in_days_test)
ages_in_days_train = [a if not np.isnan(a) else train_age_mean for a in ages_in_days_train]
ages_in_days_test = [a if not np.isnan(a) else test_age_mean for a in ages_in_days_test]
train['Age'] = pd.Series(ages_in_days_train)
test['Age'] = pd.Series(ages_in_days_test)
train = train.drop('AgeuponOutcome', axis=1)
test = test.drop('AgeuponOutcome', axis=1)

def format_datetime(dataset):
    times = [pd.Timestamp(t) for t in dataset.DateTime]
    years = [int(t.year) for t in times]
    months = [int(t.month) for t in times]
    days = [int(t.day) for t in times]
    hours = [int(t.hour) for t in times]
    minutes = [int(t.minute) for t in times]
    return years, months, days, hours, minutes

years_train, months_train, days_train, hours_train, minutes_train = format_datetime(train)
years_test, months_test, days_test, hours_test, minutes_test = format_datetime(test)
train['Year'], train['Month'], train['Day'], train['Hour'], train['Minute'] \
    = years_train, months_train, days_train, hours_train, minutes_train
test['Year'], test['Month'], test['Day'], test['Hour'], test['Minute'] \
    = years_test, months_test, days_test, hours_test, minutes_test
train = train.drop('DateTime', axis=1)
test = test.drop('DateTime', axis=1)
train.head()


def mix_encoder(dataset):
    breeds = [b.split() for b in dataset.Breed]
    is_mix = []
    for b in breeds:
        if 'mix' in b or 'Mix' in b:
            is_mix.append(1)
        else:
            is_mix.append(0)
    return is_mix

train_mix = mix_encoder(train)
test_mix = mix_encoder(test)
train['Mix'] = pd.Series(train_mix)
test['Mix'] = pd.Series(test_mix)
train.head()


train['OutcomeType'] = LabelEncoder().fit_transform(train['OutcomeType'])

for var in ['AnimalType', 'Sex']:
    train[var] = LabelBinarizer().fit_transform(train[var])
    test[var] = LabelBinarizer().fit_transform(test[var])

for var in ['SterilizationStatus', 'Breed', 'Color']:
    train[var] = LabelEncoder().fit_transform(train[var])
    test[var] = LabelEncoder().fit_transform(test[var])

train.head()

clf = GridSearchCV(DecisionTreeClassifier(), param_grid={'max_depth': [4, 5, 6, 7, 8, 9, 10, 12],
                                                         'min_samples_split': [2, 5, 10, 15, 20, 25],
                                                         'min_samples_leaf': [1, 2, 5, 8, 12, 15, 20]},
                   scoring='log_loss',
                   n_jobs=-1)
clf.fit(train[train.columns[2:]], train.OutcomeType)

clf.best_params_
clf.best_score_

class_probabilites = clf.predict_proba(test[test.columns[1:]])
submission = 'ID,Adoption,Died,Euthanasia,Return_to_owner,Transfer\n'
for i in range(len(test.ID)):
    submission += str(test.ID[i]) + ',' + ','.join([str(j) for j in class_probabilites[i]]) + '\n'
f = open("submission.csv", "w")
f.write(submission)
f.close()