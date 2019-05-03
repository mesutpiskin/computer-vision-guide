English | [Türkçe](./README.md)

# Face Recognition with FaceNet

**What is FaceNet?**

https://github.com/davidsandberg/facenet


**Dependence:**


```bash
pip install -r requirements.txt
```

**How to run:**

First, you need to copy the faces you want to train into the following directory.
***./dataset/train/name/name_id.jpg***

Example: ./dataset/train/mesut/mesut_1.png 

To do the training process with the added faces;

```bash
python classifier.py TRAIN datasets/train models/20180408-102900/20180408-102900.pb models/datasets_classifier.pkl --batch_size 1000
```

When the training is complete, the output model will be created under the model directory dataset classifier. To test the trained model;

```bash
python face_recognition_webcam.py --model models/20180408-102900 --classifier models/datasets_classifier.pkl
```