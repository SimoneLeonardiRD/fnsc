from sklearn.model_selection import train_test_split, KFold
from sklearn.ensemble import  RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn import preprocessing
import pandas as pd


dy = pd.read_csv("output_test/user_label_clean.csv")
y = dy['label'].values
dx = pd.read_csv("user_info.csv")
dx = dx.fillna("")
#print(dx.head)
le = preprocessing.LabelEncoder()
dx['location'] = le.fit_transform(dx['location'])
dx['created_at'] = le.fit_transform(dx['created_at'])
#print(dx.head())

X = dx.values
print(X.shape)
print(y.shape)
'''
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
model = RandomForestClassifier(random_state=1)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
prfs = precision_recall_fscore_support(y_test, y_pred)
print(acc)
print(prfs)
'''
n_splits=10
tot_acc = 0.0
prec = 0.0
recall = 0.0
f1 = 0.0
kf = KFold(n_splits=n_splits)
for train_index, test_index in kf.split(X):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    model = RandomForestClassifier(random_state=1)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prfs = precision_recall_fscore_support(y_test, y_pred)
    #print(acc)
    tot_acc += acc
    prec += prfs[0][0]
    recall += prfs[1][0]
    f1 += prfs[2][0]
    print(prfs)

print(str(tot_acc/n_splits))
print(str(prec/n_splits))
print(str(recall/n_splits))
print(str(f1/n_splits))