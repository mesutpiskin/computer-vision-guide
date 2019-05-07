[English](./README.en-US.md) | Türkçe

**FaceNet ile Yüz Tanıma** 
-----------------------------------------------


**FaceNet Nedir?**

https://github.com/davidsandberg/facenet



**Bağımlılıklar:**


```bash
pip install -r requirements.txt
```

paket kurulumlarının ardından modeli aşağıdaki bağlantıdan indirerek proje altındaki models dizinine çıkartın.

https://drive.google.com/open?id=1n9GZ_Uw9aJWfuAoPt6_4riNW8OpZVXK4

**Çalıştırmak için:**

Öncelikli olarak eğitmek istediğiniz yüzleri kırpılmış olarak aşağıdaki dizine atmalısınız
***./dataset/train/isim/isim_id.jpg***

Örnek: ./dataset/train/mesut/mesut_1.png 

Eklenmiş olan yüzler ile eğitim işlemi yapmak için;

```bash
python classifier.py TRAIN datasets/train models/20180408-102900/20180408-102900.pb models/datasets_classifier.pkl --batch_size 1000
```

Eğitim işlemi tamamlandığında çıktı model, models dizini altında datasets_classifier adıyla oluşturulacaktır. Eğitilmiş modeli test etmek için ise 

```bash
python face_recognition_webcam.py --model models/20180408-102900 --classifier models/datasets_classifier.pkl
```
