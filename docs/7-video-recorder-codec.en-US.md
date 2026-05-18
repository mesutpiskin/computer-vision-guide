[Türkçe](./7-video-kaydediciler-codec.md) | English

**Video Recorders and Codecs** 
-------------------------------

To create video with OpenCV — that is, to save arrays of images — the VideoWriter class is used. Before using it, it's helpful to understand some concepts: codec (code-decoder) and FourCC (Four character code).

Codec (Code-Decoder):

Raw audio and video file sizes are quite large. The solution to this problem is to compress this data. Many different algorithms have been developed to compress image and audio files. These algorithms use different methods for compression. To decompress the compressed data, a decoder that understands and displays the data according to this compression algorithm is needed. These decoders are called codecs. Some common codecs you're probably familiar with include H261, MJPEG, MPEG, etc.

FourCC:

"Four character code" is the term used for a four-character code. The purpose of FourCC is to identify codecs in media data with four characters — creating a standard identification format. ASCII characters must be used when defining FourCC codes. The most well-known are DIVX, XVID, H264, etc. You can check the current list here. To download codecs, you can use this link.

The FourCC format is as follows:

__ – __ – __ – __

8   –  8   –   8   –   8      = 4byte – 32bit

In OpenCV, we'll use FourCC to define or use codecs.

 
VideoWriter

To write video, 5 parameters are needed: the directory where the video will be saved, the codec, frame size (width, height), fps value, and a boolean flag that determines whether the video will be recorded in color or grayscale.

*Java:*

```Java
VideoWriter videoWriter;
videoWriter = new VideoWriter(outputFile, VideoWriter.fourcc('X', 'V','I','D'),
                fps, frameSize, isRGB);
//We specified with fourcc that we'll use x264 as the codec
//For the write operation, we added the following method to write the image we passed as parameter
 public void Write(Mat frame) {
        if(videoWriter.isOpened()==false){
            videoWriter.release();
            throw new IllegalArgumentException("Video Writer Exception: VideoWriter could not be opened,"
                    + "check parameters.");        
        }
        //Write
        videoWriter.write(frame);
    }

//For the example, let's read images from the camera with VideoCapture and write the same video

VideoCapture videoCapture = new VideoCapture(0);
Size frameSize = new Size((int) videoCapture.get(Videoio.CAP_PROP_FRAME_WIDTH), (int) videoCapture.get(Videoio.CAP_PROP_FRAME_HEIGHT));
VideoWriter videoWriter = new VideoWriter("test.avi", VideoWriter.fourcc('X', 'V','I','D'),
                videoCapture.get(Videoio.CAP_PROP_FPS), frameSize, true);
while (videoCapture.read(mat)) {
            videoWriter.write(mat);         
        }
        videoCapture.release();
        videoWriter.release();
```

*Python:*

```Python
import cv2

cap = cv2.VideoCapture(0)

# Create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('recording.avi', fourcc, 10.0, (1024, 768))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.flip(frame, 0)

        # Write current frame
        out.write(frame)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()

```

One of the potential problems you might encounter from this process is that the written video won't open or the write operation fails. This is likely due to a missing codec package on your system. To solve this, you can download ffmpeg from https://ffmpeg.org/download.html and see how to install it at http://www.wikihow.com/Install-FFmpeg-on-Windows.
