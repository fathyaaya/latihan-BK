# -*- coding: utf-8 -*-
"""latihan1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1L7_fwc-0RpNs4xPwxoK8adxEuOX6S9Kr

**2.menelaah data**

pilih dan memasukkan ke library untuk menelaah data
"""

import pandas as pd
import re
import numpy as np
import itertools

"""Load Data

memasukkan dataset yang dibutuhkan dengan alamat penyimpanan yang tepat dan simoan kedalam sebuah variabel
"""

dir = 'hungarian.data'

"""membuat iterasi untuk membaca data set"""

with open(dir, encoding='Latin1') as file:
  lines = [line.strip() for line in file]
lines[0:10]

"""setelah membaca dataset maka dilajutkan dengan melakukan iterasi sesuai jumlah kolom dan baris yang ada pada dataset"""

data = itertools.takewhile(
  lambda x: len(x) == 76,
  (' '.join(lines[i:(i + 10)]).split() for i in range(0, len(lines), 10))
)

df = pd.DataFrame.from_records(data)

df.head()

"""menampilan informasi dari file dataset yang sudah dimasukkan kedlama dataframe"""

df.info()

"""pada kondisi dataset yang dimiliki terdapat kondisi khusus yang dimana sebelum tahap validasi data untuk tipe data object atau
string perlu dilakukan penghapusan fitur dikarenakan pada dataset ini nilai null disimbolkan dengan angka -9.0
"""

df = df.iloc[:,:-1]
df = df.drop(df.columns[0], axis=1)

"""mengubah tipe data file dataset menjadi tipe data float sesuai dengan nilai null yaitu -9.0"""

df = df.astype(float)
df.info()

"""**3.Validasi Data **

Pada tahap ini bertujuan untuk mengetahui dan memahami isi dari dataset agar dapat dilakukan penanganan sesuai dengan kondisinya mengubah nilai -9.0 menjadi nilai null value sesuai dengan deskripsi dataset
"""

df.replace(-9.0, np.nan, inplace=True)

"""menghitung jumlah nilai null value"""

df.isnull().sum()

df.head()

df.info()

"""**4.menentukan object data**

memilih 14 fitur yang akan digunakan sesuai dengan deskripsi dataset
"""

df_selected = df.iloc[:, [1, 2, 7,8,10,14,17,30,36,38,39,42,49,56]]

df_selected.head()

df_selected.info()

"""mengganti nama kolom sesuai dengan 14 nama kolom yang ada pada deskripsi dataset"""

column_mapping = {
    2: 'age',
    3: 'sex',
    8: 'cp',
    9: 'trestbps',
    11: 'chol',
    15: 'fbs',
    18: 'restecg',
    31: 'thalach',
    37: 'exang',
    39: 'oldpeak',
    40: 'slope',
    43: 'ca',
    50: 'thal',
    57: 'target'
}

df_selected.rename(columns=column_mapping, inplace=True)

df_selected.info()

"""menghitung jumlah fitur pada dataset"""

df_selected.value_counts()

"""**5.membersihkan data**

Sebelum melakukan pemodelan dilakukan pembersihan data agar model yang dihasilkan lebih akurat
menghitung jumlah null values yang ada diddalam dataset
"""

df_selected.isnull().sum()

"""Berdasarkan output kode program diatas ada beberapa fitur yang hampir 90% datanya memiliki nilai null sehingga perlu dilakukan
penghapusan fitur menggunakan fungsi drop
"""

columns_to_drop = ['ca', 'slope','thal']
df_selected = df_selected.drop(columns_to_drop, axis=1)
df_selected.isnull().sum()

"""Dikarenakan masih ada nilai null dibeberapa kolom fitur maka akan dilakukan pengisian nilai null menggunakan nilai mean di setiap kolomnya"""

meanTBPS = df_selected['trestbps'].dropna()
meanChol = df_selected['chol'].dropna()
meanfbs = df_selected['fbs'].dropna()
meanRestCG = df_selected['restecg'].dropna()
meanthalach = df_selected['thalach'].dropna()
meanexang = df_selected['exang'].dropna()

meanTBPS = meanTBPS.astype(float)
meanChol = meanChol.astype(float)
meanfbs = meanfbs.astype(float)
meanthalach = meanthalach.astype(float)
meanexang = meanexang.astype(float)
meanRestCG = meanRestCG.astype(float)

meanTBPS = round(meanTBPS.mean())
meanChol = round(meanChol.mean())
meanfbs = round(meanfbs.mean())
meanthalach = round(meanthalach.mean())
meanexang = round(meanexang.mean())
meanRestCG = round(meanRestCG.mean())

"""mengubah nilai null menjadi nilai mean yang sudah ditentukan"""

fill_values = {'trestbps': meanTBPS, 'chol': meanChol, 'fbs': meanfbs,'thalach':meanthalach,'exang':meanexang,'restecg':meanRestCG}
dfClean = df_selected.fillna(value=fill_values)

dfClean.info()

dfClean.isnull().sum()

"""pengecekan terhadap duplikasi data"""

duplicate_rows = dfClean.duplicated()
dfClean[duplicate_rows]

print("All Duplicate Rows:")
dfClean[dfClean.duplicated(keep=False)]

"""menghapus data yang memiliki duplikat"""

dfClean = dfClean.drop_duplicates()
print("All Duplicate Rows:")
dfClean[dfClean.duplicated(keep=False)]

dfClean.head()

dfClean['target'].value_counts()

import seaborn as sns
import matplotlib.pyplot as plt

"""untuk mencari korelasi antar fitur"""

dfClean.corr()

cor_mat=dfClean.corr()
fig,ax=plt.subplots(figsize=(15,10))
sns.heatmap(cor_mat,annot=True,linewidths=0.5,fmt=".3f")

"""**6.kontruksi data**

tahap ini adalah salah satu tujuan untuk menyesuaikan semua tipe data yang ada di dalam dataset. tetapi tahap ini dataset sudah memiliki tipe data maka tidak perlu melakukan penyesuaian kembali
"""

dfClean.info()

dfClean.head(5)

"""setelah menyesuaikan, setelah itu memisahkan fitur dan taerget lalu simpan kedalam variabel"""

X = dfClean.drop("target",axis=1).values
y = dfClean.iloc[:,-1]

"""setekah pemisahan fitur da taerget, setelah itu melakukan pengecekan terhadap persebara jumlah target terlebih dahulu"""

dfClean['target'].value_counts().plot(kind='bar',figsize=(10,6),color=['green','blue'])
plt.title("Count of the target")
plt.xticks(rotation=0);

"""Pada Grafik diatas menunjukan bahwa persebaran jumlah target tidak seimbang oleh karena itu perlu diseimbangkan terlebih dahulu.
Menyeimbangkan target ada 2 cara yaitu oversampling dan undersampling. oversampling dilakukan jika jumlah dataset sedikit sedangkan
undersampling dilakukan jika jumlah data terlalu banyak.
Disini kita akan melakukan oversampling dikarenakan jumlah data kita tidak banyak. Salah satu metode yang Oversampling yang akan kita
gunakan adalah SMOTE
"""

from imblearn.over_sampling import SMOTE

# oversampling
smote = SMOTE(random_state=42)
X_smote_resampled, y_smote_resampled = smote.fit_resample(X, y)

plt.figure(figsize=(12, 4))

new_df1 = pd.DataFrame(data=y)

plt.subplot(1, 2, 1)
new_df1.value_counts().plot(kind='bar',figsize=(10,6),color=['green','blue','red','yellow'])
plt.title("target before over sampling with SMOTE ")
plt.xticks(rotation=0);

plt.subplot(1, 2, 2)
new_df2 = pd.DataFrame(data=y_smote_resampled)

new_df2.value_counts().plot(kind='bar',figsize=(10,6),color=['green','blue','red','yellow'])
plt.title("target after over sampling with SMOTE")
plt.xticks(rotation=0);

plt.tight_layout()
plt.show()

"""pada grafik diatas dapat dilihat ketika target belum di seimbangkan dan sudah diseimbangkan menggunakan oversampling."""

new_df1 = pd.DataFrame(data=y)
new_df1.value_counts()

# over
new_df2 = pd.DataFrame(data=y_smote_resampled)
new_df2.value_counts()

"""Setelah menyeimbangkan persebaran jumlah target kita akan melakukan mengecekan apakah perlu dilakukan normalisasi/standarisasi pada
datset kita.
"""

dfClean.describe()

"""deskripsi di atas terlihat bahwa terdapat rentang ilai yang cukuo jauh pada standart deviasi setiap viturdata set yang kita moiliki. karena itu perludilakukan normalisasi/standarisasi agar dapat memperkecil rentang antara standardeviasi setiap kolom"""

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
X_smote_resampled_normal = scaler.fit_transform(X_smote_resampled)
len(X_smote_resampled_normal)

dfcek1 = pd.DataFrame(X_smote_resampled_normal)
dfcek1.describe()

"""setelah normalisasi pada fiur, selnjutnya perlu membagi fitur dan target menjadi data train dan test"""

from sklearn.model_selection import train_test_split

# membagi fitur dan target menjadi data train dan test (untuk yang oversample saja)
X_train, X_test, y_train, y_test = train_test_split(X_smote_resampled, y_smote_resampled, test_size=0.2, random_state=42,stratify=y_smote_resampled)

# membagi fitur dan target menjadi data train dan test (untuk yang oversample + normalization)
X_train_normal, X_test_normal, y_train_normal, y_test_normal = train_test_split(X_smote_resampled_normal, y_smote_resampled, test_size=0.2, random_state=42,stratify = y_smote_resampled)

"""**7.model**

tahap ini untuk membangun model

fungsi untuk menampilkan hasilakurasi dan rata-ratadari recall, f1 dan precision scoresetiap model. dan fungsi ini nantinya akan di panggil di setiap model(membuat fubgsi ini bersifat opsional)
"""

from sklearn.metrics import accuracy_score,recall_score,f1_score,precision_score,roc_auc_score,confusion_matrix,precision_score

def evaluation(Y_test,Y_pred):
    acc = accuracy_score(Y_test,Y_pred)
    rcl = recall_score(Y_test,Y_pred,average = 'weighted')
    f1 = f1_score(Y_test,Y_pred,average = 'weighted')
    ps = precision_score(Y_test,Y_pred,average = 'weighted')

    metric_dict={'accuracy': round(acc,3),
                  'recall': round(rcl,3),
                  'F1 score': round(f1,3),
                  'Precision score': round(ps,3)
                }
    return print(metric_dict)

"""KNN

tahap ini memulai membangun model dengan menggunakan algoritma KNN dengan nilai neighbors yaitu 3.
"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report

knn_model = KNeighborsClassifier(n_neighbors = 3)
knn_model.fit(X_train, y_train)

"""kode program untuk menampilkan hasil akurasi dengan algoritma KNN"""

y_pred_knn = knn_model.predict(X_test)

# Evaluate the KNN model
print("K-Nearest Neighbors (KNN) Model:")
accuracy_knn_smote = round(accuracy_score(y_test,y_pred_knn),3)
print("Accuracy:", accuracy_knn_smote)
print("Classification Report:")
print(classification_report(y_test, y_pred_knn))

evaluation(y_test,y_pred_knn)
{'accuracy': 0.754, 'recall': 0.754, 'F1 score': 0.741, 'Precision score': 0.745}

"""pada visualisasi ini ditampilkan visualisasi confusioan matrix untuk membandingakn hasil prediksi model dengan nilai sebelumnya"""

cm = confusion_matrix(y_test, y_pred_knn)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title('Confusion Matrix')
plt.xlabel('True')
plt.ylabel('Predict')
plt.show()