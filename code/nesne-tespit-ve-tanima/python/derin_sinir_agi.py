import cv2
import numpy as np

model_class = { 0: 'background',
				1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat',
				5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair',
				10: 'cow', 11: 'diningtable', 12: 'dog', 13: 'horse',
				14: 'motorbike', 15: 'person', 16: 'pottedplant',
				17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tvmonitor' }
		
model_proto = "MobileNetSSD_deploy.prototxt"
model_weight = "MobileNetSSD_deploy.caffemodel"
net = cv2.dnn.readNetFromCaffe(model_proto, model_weight)
video_capture= cv2.VideoCapture(0)

while(video_capture.isOpened()):
	
	ret, frame = video_capture.read()
	
	rows, cols = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(frame, 0.007843, 
								(640, 480), 
								(127.5, 127.5, 127.5), False)
	net.setInput(blob)
	detections = net.forward()	

	for i in range(detections.shape[2]):
		confidence = detections[0, 0, i, 2]
		if confidence > 0.4:
			class_id = int(detections[0, 0, i, 1])
			xLeftBottom = int(detections[0, 0, i, 3] * cols)
			yLeftBottom = int(detections[0, 0, i, 4] * rows)
			xRightTop   = int(detections[0, 0, i, 5] * cols)
			yRightTop   = int(detections[0, 0, i, 6] * rows)
			cv2.rectangle(frame, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop),
							(0,0,0), 2)

			if model_id in model_class:
				label = "Nesne: "+model_class[model_id] + " Tahmin Orani: " + "%0.1f"%confidence
				labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
				yLeftBottom = max(yLeftBottom, labelSize[1])
				cv2.putText(frame, label, (xLeftBottom, yLeftBottom),
					cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)	
	cv2.imshow("",frame)
	key = cv2.waitKey(2)
	if key == 27:
		break


video_capture.release()
cv2.destroyAllWindows()
