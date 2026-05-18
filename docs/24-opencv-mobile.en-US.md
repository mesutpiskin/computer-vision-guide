[Türkçe](./24-opencv-mobil.md) | English

# OpenCV Mobile (Android and iOS)

OpenCV officially supports both Android and iOS platforms. This chapter covers installation and basic usage for each platform.

## Android

### Installation

1. Download the "Android" package from [opencv.org/releases](https://opencv.org/releases/)
2. Extract the zip file (e.g., `OpenCV-4.9.0-android-sdk/`)
3. In Android Studio: `File → New → Import Module`
4. Select the `OpenCV-4.9.0-android-sdk/sdk/` folder
5. Add dependency to `app/build.gradle`:

```groovy
dependencies {
    implementation project(':sdk')
}
```

### Initialize OpenCV

Load OpenCV asynchronously in `MainActivity.java`:

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
            Log.i(TAG, "OpenCV loaded successfully.");
        } else {
            Log.e(TAG, "Failed to load OpenCV!");
        }
    }
}
```

### Process Camera Frame (CameraBridgeViewBase)

```java
import org.opencv.android.CameraBridgeViewBase;
import org.opencv.core.Mat;

public class MainActivity extends AppCompatActivity
        implements CameraBridgeViewBase.CvCameraViewListener2 {

    private CameraBridgeViewBase mCameraView;

    @Override
    public Mat onCameraFrame(CameraBridgeViewBase.CvCameraViewFrame inputFrame) {
        Mat rgba = inputFrame.rgba();
        // Convert to grayscale
        Imgproc.cvtColor(rgba, rgba, Imgproc.COLOR_RGBA2GRAY);
        Imgproc.cvtColor(rgba, rgba, Imgproc.COLOR_GRAY2RGBA);
        return rgba;
    }

    @Override public void onCameraViewStarted(int width, int height) {}
    @Override public void onCameraViewStopped() {}
}
```

Camera view in `activity_main.xml`:

```xml
<org.opencv.android.JavaCameraView
    android:id="@+id/camera_view"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    app:camera_id="back"
    app:show_fps="true" />
```

### Real-time Detection with TFLite Model (Android)

```java
import org.tensorflow.lite.Interpreter;

// Place model.tflite in assets/ folder
Interpreter tflite = new Interpreter(loadModelFile("model.tflite"));

float[][][][] input = new float[1][224][224][3];
// ... populate input array with image

float[][] output = new float[1][1000];
tflite.run(input, output);

int predClass = argmax(output[0]);
```

### AndroidManifest Permissions

```xml
<uses-permission android:name="android.permission.CAMERA" />
<uses-feature android:name="android.hardware.camera" />
```

---

## iOS

### Installation (CocoaPods)

```ruby
# Podfile
platform :ios, '12.0'

target 'MyApp' do
  pod 'OpenCV', '~> 4.9.0'
end
```

```bash
pod install
# Open the .xcworkspace file
```

### Installation (Swift Package Manager)

In Xcode: `File → Add Package Dependencies` → Enter URL `https://github.com/opencv/opencv`.

### Basic Usage (Swift + Objective-C Bridge)

To use OpenCV in a Swift project, you need an Objective-C bridge header.

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

Call from Swift:

```swift
let grayImage = OpenCVWrapper.toGrayscale(originalImage)
imageView.image = grayImage
```

### Real-time Camera Processing (iOS)

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

        // OpenCV operation
        let processed = OpenCVWrapper.toGrayscale(uiImage)
        DispatchQueue.main.async {
            self.previewImageView.image = processed
        }
    }
}
```

---

## Performance Tips

* On mobile devices, `opencv-contrib` modules consume unnecessary space; compile only required modules
* Camera frame processing should be done outside the main thread
* `BGR` format is faster on CPU than `RGBA`; `RGBA2GRAY` can be done in one step
* On Android, `NativeCamera` (C++ JNI) is ~2x faster than Java camera
