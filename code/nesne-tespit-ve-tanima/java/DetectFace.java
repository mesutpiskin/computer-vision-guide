import java.awt.FlowLayout;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.InputStream;
import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.core.MatOfByte;
import org.opencv.core.MatOfRect;
import org.opencv.core.Point;
import org.opencv.core.Rect;
import org.opencv.core.Scalar;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;
import org.opencv.objdetect.CascadeClassifier;
import org.opencv.videoio.VideoCapture;
/*
 * OpenCV version 3.1
 Cascade modelleri https://github.com/opencv/opencv/tree/master/data/haarcascades
*/
public class DetectFace {
 
	static JFrame frame;
	static JLabel lbl;
	static ImageIcon icon;
 
	public static void main(String[] args) {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);

		CascadeClassifier cascadeFaceClassifier = new CascadeClassifier(
				"D:/Programlar/Opencv/3.1.0/opencv/build/etc/haarcascades/haarcascade_frontalface_default.xml");
		CascadeClassifier cascadeEyeClassifier = new CascadeClassifier(
				"D:/Programlar/Opencv/3.1.0/opencv/build/etc/haarcascades/haarcascade_eye.xml");
		
		CascadeClassifier cascadeNoseClassifier = new CascadeClassifier(
				"D:/Programlar/Opencv/3.1.0/opencv/build/etc/haarcascades/haarcascade_mcs_nose.xml");
	    //CascadeClassifier cascadeMouthClassifier = new CascadeClassifier("OpenCV/haarcascades/haarcascade_mcs_mouth.xml"); haarcascade_mcs_mouth on 2.4.11
		//Varsayylan kamera aygytyny ba?lat
		VideoCapture videoDevice = new VideoCapture();
		videoDevice.open(0);
		if (videoDevice.isOpened()) {
		//Sonsuz bir döngü ile sürekli olarak görüntü aky?y sa?lanyr 	
			while (true) {		
				Mat frameCapture = new Mat();
				videoDevice.read(frameCapture);
				
				//Yakalanan görüntüyü önce dönü?tür ve frame içerisine yükle
				MatOfRect faces = new MatOfRect();
				cascadeFaceClassifier.detectMultiScale(frameCapture, faces);								
				//Yakalanan çerçeve varsa içerisinde dön ve yüzün boyutlary ölçüsünde bir kare çiz
				for (Rect rect : faces.toArray()) {
					//Sol üst kö?esine metin yaz
					Imgproc.putText(frameCapture, "Face", new Point(rect.x,rect.y-5), 1, 2, new Scalar(0,0,255));								
					Imgproc.rectangle(frameCapture, new Point(rect.x, rect.y), new Point(rect.x + rect.width, rect.y + rect.height),
							new Scalar(0, 100, 0),3);
				}
				
				//Gözleri bul ve bulunan array içerisinde dönerek kare çiz
				MatOfRect eyes = new MatOfRect();
				cascadeEyeClassifier.detectMultiScale(frameCapture, eyes);
				for (Rect rect : eyes.toArray()) {
					//Sol üst kö?esine metin yaz
					Imgproc.putText(frameCapture, "Eye", new Point(rect.x,rect.y-5), 1, 2, new Scalar(0,0,255));				
					//Kare çiz
					Imgproc.rectangle(frameCapture, new Point(rect.x, rect.y), new Point(rect.x + rect.width, rect.y + rect.height),
							new Scalar(200, 200, 100),2);
				}
				
				//Burunlary bul ve bulunan array içerisinde dönerek kare çiz
				MatOfRect nose = new MatOfRect();
				cascadeNoseClassifier.detectMultiScale(frameCapture, nose);
				for (Rect rect : nose.toArray()) {
					//Sol üst kö?esine metin yaz
					Imgproc.putText(frameCapture, "Nose", new Point(rect.x,rect.y-5), 1, 2, new Scalar(0,0,255));				
					//Kare çiz
					Imgproc.rectangle(frameCapture, new Point(rect.x, rect.y), new Point(rect.x + rect.width, rect.y + rect.height),
							new Scalar(50, 255, 50),2);
				}
				
				//A?yz bul ve bulunan array içerisinde dönerek kare çiz
			   /*MatOfRect mouth = new MatOfRect();
				cascadeMouthClassifier.detectMultiScale(frameCapture, mouth);
				for (Rect rect : mouth.toArray()) {
					
					Imgproc.rectangle(frameCapture, new Point(rect.x, rect.y), new Point(rect.x + rect.width, rect.y + rect.height),
							new Scalar(129, 90, 50),2);
				}
				
				*/
				
				//Resmi swing nesnesinde gösterebilmek için önce image haline çevir ve ekrana bas
				PushImage(ConvertMat2Image(frameCapture));
				System.out.println(String.format("%s yüz(FACES) %s göz(EYE) %s burun(NOSE) detected.", faces.toArray().length,eyes.toArray().length,nose.toArray().length));
			}
		} else {
			System.out.println("Video aygytyna ba?lanylamady.");
			return;
		}
	}
	//Mat nesnesini image tipine dönü?tür
	private static BufferedImage ConvertMat2Image(Mat kameraVerisi) {
	
		
		MatOfByte byteMatVerisi = new MatOfByte();
		//Ara belle?e verilen formatta görüntü kodlar
		Imgcodecs.imencode(".jpg", kameraVerisi, byteMatVerisi);
		//Mat nesnesinin toArray() metodu elemanlary byte dizisine çevirir
		byte[] byteArray = byteMatVerisi.toArray();
		BufferedImage goruntu = null;
		try {
			InputStream in = new ByteArrayInputStream(byteArray);
			goruntu = ImageIO.read(in);
		} catch (Exception e) {
			e.printStackTrace();
			return null;
		}
		return goruntu;
	}
  	
//Bir frame (çerçeve) olu?turur
	public static void PencereHazirla() {
		frame = new JFrame();
		frame.setLayout(new FlowLayout());
		frame.setSize(700, 600);
		frame.setVisible(true);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	}
	//Resmi gösterecek label olu?turur
	public static void PushImage(Image img2) {
		//Pencere olu?turulmamy? ise hazyrlanyr
		if (frame == null)
			PencereHazirla();
		//Daha önceden bir görüntü yüklenmi? ise yenisi için kaldyryr
		if (lbl != null)
			frame.remove(lbl);
		icon = new ImageIcon(img2);
		lbl = new JLabel();
		lbl.setIcon(icon);
		frame.add(lbl);
		//Frame nesnesini yeniler
		frame.revalidate();
	}
}