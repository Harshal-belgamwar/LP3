import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score,confusion_matrix,f1_score,recall_score,precision_score,r2_score,mean_absolute_error,mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv("path to/uber.csv")
df.info()
df.isnull().sum()

df.dropna(inplace=True)

df.isnull().sum()
# remove unnecessary column
df.drop(["Unnamed: 0","key"],axis=1,inplace=True)

# remove invalid data
df = df[df["fare_amount"]>0]

df.head()

import seaborn as sns
import matplotlib.pyplot as plt

sns.boxplot(x=df["fare_amount"])
plt.title("Box plot before removal")
plt.show()

q1 = df["fare_amount"].quantile(0.25)
q3 = df["fare_amount"].quantile(0.75)

IQR = q3 - q1
lower = max(0,q1 - 1.5*IQR)
upper = q3 + 1.5*IQR
print("Lower:",lower)
print("Upper:",upper)
df= df[(df["fare_amount"]>=lower) & (df["fare_amount"]<=upper)]

sns.boxplot(x=df["fare_amount"])
plt.title("Box plot after removal")
plt.show()

corr = df.corr(numeric_only=True)
sns.heatmap(corr,annot=True,fmt=".2f",cmap="coolwarm")
plt.title("Correlation between numeric columns")

from sklearn.model_selection import train_test_split

x = df[["pickup_longitude","pickup_latitude","dropoff_longitude","dropoff_latitude","passenger_count"]]
y = df["fare_amount"]

X_train,X_test,Y_train,Y_test = train_test_split(
    x,y,test_size=0.2,random_state=42
)

lr = LinearRegression()
lr.fit(X_train,Y_train)
y_pred_lr = lr.predict(X_test)

# rfc = RandomForestRegressor(n_estimators=100,random_state = 42,n_jobs=-1)
rfc = RandomForestRegressor()
rfc.fit(X_train,Y_train)
y_pred_rfc = rfc.predict(X_test)


print("Model Metrics\n")
print("LinearRegression Model:\n")
print("R2 score",r2_score(Y_test,y_pred_lr))
print("RMSE",np.sqrt(mean_squared_error(Y_test,y_pred_lr)))
print("MSE",mean_squared_error(Y_test,y_pred_lr))
print("MAE",mean_absolute_error(Y_test,y_pred_lr))

print("\nRandom Forest Model:")
print("R2 score",r2_score(Y_test,y_pred_rfc))
print("RMSE",np.sqrt(mean_squared_error(Y_test,y_pred_rfc)))
print("MSE",mean_squared_error(Y_test,y_pred_rfc))
print("MAE",mean_absolute_error(Y_test,y_pred_rfc))
