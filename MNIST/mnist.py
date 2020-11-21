# -*- coding: utf-8 -*-
"""MNIST.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ehfZdkxrlFEjqndbSysiQIK03LGQ-FBB

# **MNIST Dataseti ile Deep Learning Uygulaması**

## Load Data
"""

from keras.datasets import mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()

print("ilk datanin shape'i:", x_train[0].shape) # (28, 28)
print("ilk datanin icerigi:", y_train[0]) # 5

"""## Normalization"""

x_train_norm = x_train.reshape((60000, 28*28)) #Goruntuyu vektore donusturur
x_train_norm = x_train_norm.astype('float32') / 255 #Normalize eder
x_test_norm = x_test.reshape((10000, 28*28)) 
x_test_norm = x_test_norm.astype('float32') / 255

print("Normalizasyon sonrasi shape:", x_train_norm.shape) # (60000, 784)

"""## Model

Devamında ağın yapısını tanımlamamız gerekiyor.
"""

from keras import models
from keras import layers

"""`from keras.models import Sequential` gibi de kullanabiliriz.

Modeli kullanmadan önce `models.Sequential()` gibi tanımlamalıyız.
"""

model = models.Sequential()

#Giris katmani
model.add(layers.Dense(32, 
                       activation='relu', 
                       input_shape=(28*28,)))

model.add(layers.Dense(32,
                       activation='relu'))

"""Çıkış katmanımızda 10 adet çıkış olmalı.  
0,1,2,3,4,5,6,7,8,9

Bu, **multi class classification** olarak geçer. Dolayısıyla çıkış katmanımızda activation function olarak **softmax** tercih ediyoruz.

**Binary Classification**'da ise genelde **sigmoid** tercih edilir.
"""

#Cikis katmani
model.add(layers.Dense(10, #cikis sayisina esit olmali
                       activation="softmax"))

"""`categorical_crossentropy` kullanabilmemiz için, çıkış datalarımız olan *y_train* ve *y_test* datalarını categorical'a dönüştürmemiz gerekiyor.

Örneğin, **5** olarak değil **[0,0,0,0,0,1,0,0,0,0]** olarak modele vermemiz gerekiyor.

`sparse_categorical_crossentropy` bu işlemi kendisi yapar. `to_categorical` yapmamıza gerek kalmaz.
"""

from keras.utils import to_categorical
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

y_train.shape

y_train[0,:] # 5 vardi

"""Optimizer olarak *Stochastic Gradient Descent (SGD)* kullanıyoruz.

Loss function olarak *Categorical Cross Entropy* kullanıyoruz.  
Problem tipi Regresyon ise genelde *mse, mae* gibi regresyon fonksiyonları kullanılır.  
Multi class classification'da ise *cross entropy* veya *sparse categorical cross entropy* kullanılır.

Metrics ise ekrana yazdıracağımız değeri belirtir.



"""

model.compile(optimizer="sgd", 
              loss="categorical_crossentropy",
              metrics=["accuracy"])

"""Modelin yapısını özet olarak görelim;"""

model.summary()

"""Birinci katmanın çıkışı 32 olarak gözüküyor.  

Neden 25120 parametre var?  
Girişimiz 784 elemanlı.  
Her bir hücreden 784x32 adet *weights* bağlantısı var demektir.  
*Bias*'lar da var; 32 adet. (her bir hücre için 1 adet.)  
`784x32+32 = 25120` değiştirilebilir parametreye denk gelir.

İkinci katman hidden layer'dır.(dense_1)  
Bu katmanın giriş sayısı önceki katmanın çıkış sayısı kadardır yani 16.  
32x32 adet weights var 32 adet de bias var. Yani toplam;  
`32x32+32 = 1056` değiştirilebilir parametreye denk gelir.

Son katman, çıkış katmanımızdır. 10 adet hücre var.  
32x10 = 320 adet weights var, 10 adet de bias var.  
`32x10+10 = 330` değiştirilebilir parametreye denk gelir.

---

### Train

Sıradaki adımımız modeli eğitmek.
"""

model.fit(x_train_norm, y_train, epochs=10, batch_size=16)

"""Eğitilmiş ağın performansını ölçelim.

Eğitim bittikten sonra eğitimde kullanılmamış görüntülerle ağın başarımı belli olur.
"""

test_loss, test_acc = model.evaluate(x_test_norm, y_test) #test_images, test_labels

print("test_acc=", test_acc)
print("test_loss=", test_loss)

"""Eğitilen ağırlıklarımız bize %96.2 doğruluk sağladı.

Bizim eğittiğimiz şey aslında modelin ağırlıklarıdır.
"""

W = model.get_weights()

W[0] #egitilmis katsayilar

W[0].shape

"""İlk başta random üretilen kat sayılar öyle değerler almış ki bize yukarıdaki başarıyı sağladılar.  
Bu ağırlıkları kaydedersek weights'leri daha sonra tekrar kullanabiliriz. Modeli ve ağırlıkları saklamam lazım.  

Modeli kaydederken uzantısı genelde *.h5* olur.
"""

# mnist_model.h5
model.save("/content/drive/Shareddrives/UnlimitedDrive/Works/Deep_Learning/ISE-DL/MNIST/mnist_model.h5")

"""Ağırlıkları da kaydedelim;"""

# mnist_weights.h5
model.save_weights("/content/drive/Shareddrives/UnlimitedDrive/Works/Deep_Learning/ISE-DL/MNIST/mnist_weights.h5")

"""Kaydettiğimiz modeli şu şekilde yeniden yükleyebiliriz;

```
from keras import models
model = models.load_model("mnist_model.h5")
```

---
### Predict

Şimdi eğittiğimiz modeli kullanacağız.  
Predict yapacağız.

Başlangıçta test verilerimize ve train verilerimize normalizasyon uygulamıştık;

```
x_test_norm = x_test.reshape((10000, 28*28)) 
x_test_norm = x_test_norm.astype('float32') / 255
```

Predict işlemine geçmeden önce dataları biraz inceleyelim.
"""

x_test[1]

#Gorsellestirme icin
import matplotlib.pyplot as plt
import numpy as np

inx = np.random.randint(0, 10000) #kullanmak istedigimiz test verisinin index'i

rakam = x_test[inx]
plt.imshow(rakam)

"""*rakam*'ın y_test'deki karşılığına bakalım;

`argmax()` fonksiyonu bize en büyük elemanın konumunu verir.
"""

y=np.argmax(y_test[inx])
y

"""Predict yaparken normalize edilmiş verileri kullanmamız gerekiyor.  
Yani doğrudan `x_test` değil `x_test`'in normalize edilmiş halini kullanacağız.
"""

rakam = x_test[inx]

pre = model.predict(rakam.reshape(1,784)/255)
pre

tahmin_sonucu = np.argmax(pre)
print("Beklenen deger:.....", y)
print("Tahmin edilen deger:", tahmin_sonucu)