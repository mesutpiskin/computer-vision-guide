**face_recognition Kütüphanesi ile Yüz Tanıma** 
-----------------------------------------------


**Çalıştırmak için:**

```bash
python facerec_with_gui.py
```
Çalıştığında bu dizinde yer alan faces klasörü içerisindeki yüzler train eder, etiket olarak ise fotoğrafın adını kullanır.

Örneğin;

- mesut.png
- ahmet.jpg
- ayse.jpeg
- mehmet.jpg

şekkinde bir yüz listeniz olursa train için etiketlerde mesut, ahmet, ayşe ve mehmet olacaktır. Bir kişi için birden fazla yüz kullanarak eğitim yapmak isterseniz de aşağıdaki şekilde yüzleri numaralandırabilirsiniz ;

- mesut_1.png
- mesut_2.png
- mesut_3.jpg


**Bağımlılıklar:**

* Python 3.x
* face_recognition 
```bash
pip install face_recognition
```

* OpenCV 
```bash
pip install opencv-python
```
