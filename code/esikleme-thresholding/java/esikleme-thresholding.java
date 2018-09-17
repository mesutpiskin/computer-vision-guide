System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
		Mat kaynakGoruntu=new Mat();
kaynakGoruntu=Imgcodecs.imread("C:\\1.jpg");	
		Mat hedefGoruntu=new Mat();
		intthresh=150;
		intmaxDeger=255;
Imgproc.threshold(kaynakGoruntu, hedefGoruntu, thresh, maxDeger, Imgproc.THRESH_BINARY);
		Imgcodecs.imwrite("C:\\2.jpg", hedefGoruntu);
		System.out.println("Thresholding uygulandı.");