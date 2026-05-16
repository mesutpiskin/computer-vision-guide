**OpenCV Mobil (Android ve iOS)**
----------------------------------

OpenCV, Android ve iOS platformlarını resmi olarak destekler. Bu bölümde her iki platform için kurulum ve temel kullanım anlatılmaktadır.

## Android

### Kurulum

1. [opencv.org/releases](https://opencv.org/releases/) adresinden "Android" paketini indir
2. Zip dosyasını çıkart (örneğin `OpenCV-4.9.0-android-sdk/`)
3. Android Studio'da: `File → New → Import Module`
4. `OpenCV-4.9.0-android-sdk/sdk/` klasörünü seç
5. `app/build.gradle` dosyasına bağımlılık ekle:

```groovy
dependencies {
    implementation project(':sdk')
}
```

### OpenCV'yi Başlat

`MainActivity.java` içinde OpenCV'yi asenkron yükle:

```java
import org.opencv.android.OpenCVLoader;
import android.util.Log;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "OpenCV";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        if (OpenCVLoader.initLocal()) {
            Log.i(TAG, "OpenCV başarıyla yüklendi.");
        } else {
            Log.e(TAG, "OpenCV yüklenemedi!");
        }
    }
}
```

### Kamera Görüntüsünü İşle (CameraBridgeViewBase)

```java
import org.opencv.android.CameraBridgeViewBase;
import org.opencv.core.Mat;

public class MainActivity extends AppCompatActivity
        implements CameraBridgeViewBase.CvCameraViewListener2 {

    private CameraBridgeViewBase mCameraView;

    @Override
    public Mat onCameraFrame(CameraBridgeViewBase.CvCameraViewFrame inputFrame) {
        Mat rgba = inputFrame.rgba();
        // Gri tonlamaya çevir
        Imgproc.cvtColor(rgba, rgba, Imgproc.COLOR_RGBA2GRAY);
        Imgproc.cvtColor(rgba, rgba, Imgproc.COLOR_GRAY2RGBA);
        return rgba;
    }

    @Override public void onCameraViewStarted(int width, int height) {}
    @Override public void onCameraViewStopped() {}
}
```

`activity_main.xml` içinde kamera görünümü:

```xml
<org.opencv.android.JavaCameraView
    android:id="@+id/camera_view"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    app:camera_id="back"
    app:show_fps="true" />
```

### TFLite Modeli ile Gerçek Zamanlı Tespit (Android)

```java
import org.tensorflow.lite.Interpreter;

// assets/ klasörüne model.tflite koy
Interpreter tflite = new Interpreter(loadModelFile("model.tflite"));

float[][][][] input = new float[1][224][224][3];
// ... görüntüyü input array'e doldur

float[][] output = new float[1][1000];
tflite.run(input, output);

int predClass = argmax(output[0]);
```

### AndroidManifest İzinleri

```xml
<uses-permission android:name="android.permission.CAMERA" />
<uses-feature android:name="android.hardware.camera" />
```

---

## iOS

### Kurulum (CocoaPods)

```ruby
# Podfile
platform :ios, '12.0'

target 'MyApp' do
  pod 'OpenCV', '~> 4.9.0'
end
```

```bash
pod install
# .xcworkspace dosyasını aç
```

### Kurulum (Swift Package Manager)

Xcode'da: `File → Add Package Dependencies` → `https://github.com/opencv/opencv` URL'sini gir.

### Temel Kullanım (Swift + Objective-C Bridge)

Swift projesinde OpenCV kullanmak için Objective-C bridge header gerekir.

`OpenCVWrapper.h`:

```objc
#import <Foundation/Foundation.h>
#import <UIKit/UIKit.h>

@interface OpenCVWrapper : NSObject
+ (UIImage *)toGrayscale:(UIImage *)image;
@end
```

`OpenCVWrapper.mm`:

```objc
#import "OpenCVWrapper.h"
#import <opencv2/opencv.hpp>
#import <opencv2/imgcodecs/ios.h>

@implementation OpenCVWrapper

+ (UIImage *)toGrayscale:(UIImage *)image {
    cv::Mat mat;
    UIImageToMat(image, mat);
    cv::cvtColor(mat, mat, cv::COLOR_BGR2GRAY);
    cv::cvtColor(mat, mat, cv::COLOR_GRAY2BGR);
    return MatToUIImage(mat);
}

@end
```

Swift'ten çağır:

```swift
let grayImage = OpenCVWrapper.toGrayscale(originalImage)
imageView.image = grayImage
```

### Kameradan Gerçek Zamanlı İşleme (iOS)

```swift
import AVFoundation
import UIKit

class CameraViewController: UIViewController, AVCaptureVideoDataOutputSampleBufferDelegate {

    func captureOutput(_ output: AVCaptureOutput,
                       didOutput sampleBuffer: CMSampleBuffer,
                       from connection: AVCaptureConnection) {
        guard let pixelBuffer = CMSampleBufferGetImageBuffer(sampleBuffer) else { return }
        let ciImage = CIImage(cvPixelBuffer: pixelBuffer)
        let uiImage = UIImage(ciImage: ciImage)

        // OpenCV işlemi
        let processed = OpenCVWrapper.toGrayscale(uiImage)
        DispatchQueue.main.async {
            self.previewImageView.image = processed
        }
    }
}
```

---

## Performans İpuçları

* Mobil cihazlarda `opencv-contrib` modülleri gereksiz yer kaplar; sadece gerekli modülleri derle
* Kamera karesi işlemesi `main thread` dışında yapılmalıdır
* `RGBA` yerine `BGR` formatı CPU'da daha hızlıdır; `RGBA2GRAY` tek adımda yapılabilir
* Android'de `NativeCamera` (C++ JNI) Java kamerasına göre ~2x daha hızlıdır
