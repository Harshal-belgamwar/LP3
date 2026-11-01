import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

df = pd.read_csv("Downloads/emails.csv/emails.csv")

print(df.isnull().sum())
df.head()

x = df.drop(["Email No.","Prediction"],axis=1)
y = df["Prediction"]

X_train,X_test,Y_train,Y_test = train_test_split(
    x,y,test_size=0.2,random_state=42
)

knn = make_pipeline(
    StandardScaler(),
    KNeighborsClassifier(n_neighbors = 5)
)
knn.fit(X_train,Y_train)
knn_pred = knn.predict(X_test)

svm = make_pipeline(
    StandardScaler(),
    SVC(kernel="linear")
)
svm.fit(X_train,Y_train)
svm_pred = knn.predict(X_test)

from sklearn.metrics import f1_score,accuracy_score,recall_score,precision_score,classification_report,confusion_matrix

print("KNeighbors classification model\n")
print("Accuracy: ",accuracy_score(Y_test,knn_pred))
print("Recall: ",recall_score(Y_test,knn_pred))
print("precision: ",precision_score(Y_test,knn_pred))
print("f1 score: ",f1_score(Y_test,knn_pred))
print("Classification report: \n",classification_report(
    Y_test,knn_pred,target_names=["Spam","Not Spam"]
))

print("SVM classification model\n")
print("Accuracy: ",accuracy_score(Y_test,svm_pred))
print("Recall: ",recall_score(Y_test,svm_pred))
print("precision: ",precision_score(Y_test,svm_pred))
print("f1 score: ",f1_score(Y_test,svm_pred))
print("Classification report: \n",classification_report(
    Y_test,svm_pred,target_names=["Spam","Not Spam"]
))

import seaborn as sns
cm = confusion_matrix(Y_test,knn_pred)

sns.heatmap(
    cm,annot=True,fmt="d",
    xticklabels = ["Spam","Not Spam"],
    yticklabels = ["Spam","Not Spam"]
)
plt.title("KNeighbors classifier")
plt.xlabel("Predicted")
plt.ylabel("Actual")


cm1 = confusion_matrix(Y_test,svm_pred)

sns.heatmap(
    cm1,annot=True,fmt="d",
    xticklabels = ["Spam","Not Spam"],
    yticklabels = ["Spam","Not Spam"]
)
plt.title("SVM classifier")
plt.xlabel("Predicted")
plt.ylabel("Actual")
