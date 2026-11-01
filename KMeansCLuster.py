import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans 
# from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import linkage,dendrogram


df = pd.read_csv("sales_data_sample.csv",encoding="latin1")
df.info();
print(df.isnull().sum())

X = df[["QUANTITYORDERED","SALES"]]
X_Scaled = StandardScaler().fit_transform(X)

wcss=[]

for i in range(1,11):
    kmeans = KMeans(n_clusters=i,n_init=10,random_state=42)
    kmeans.fit(X_Scaled)
    wcss.append(kmeans.inertia_)
plt.plot(range(1,11),wcss)
plt.title("Elbow method")
plt.xlabel("no of clusters")
plt.ylabel("wcss")
plt.savefig("elbow_method.png")
plt.show()

df["kmeans_cluster"] = KMeans(n_clusters =3,random_state=42,n_init=10).fit_predict(X_Scaled)
plt.scatter(x=df['QUANTITYORDERED'],y=df['SALES'],c=df["kmeans_cluster"])
plt.title("KMeans Clustering")
plt.xlabel("QUANTITYORDERED")
plt.ylabel("SALES")
plt.show()

Z = linkage(X_Scaled,method="ward")
plt.figure()
dendrogram(Z,p=30)
plt.title("Hierarchical Clustering Dendrogram")
plt.xlabel("Data Points")
plt.ylabel("Distance")
plt.show()





