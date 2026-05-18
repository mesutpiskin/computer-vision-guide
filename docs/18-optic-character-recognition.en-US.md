[Türkçe](./18-optik-karakter-tanima.md) | English

# Optical Character Recognition (OCR)

The accounting department manually enters hundreds of invoice images into the system every day. A parking automation system can't read vehicle plates from camera footage. Handwritten notes in archives need to become searchable. All three are different looks at the same fundamental problem: automatically read text from an image. In this chapter, you'll learn every step of the OCR pipeline, how to use Tesseract and EasyOCR, and how to combine text detection with recognition.

## The OCR Pipeline

"Read text in an image" is not a single step. A good OCR system has three stages:

1. **Image preprocessing:** Remove noise, boost contrast, straighten the text.
2. **Text detection:** Find where text is in the image.
3. **Text recognition:** Read what's written in that region.

Each step determines the success of the next. Running OCR directly on a torn, faded, or skewed image can mean 40% lower accuracy.

> **⚠️ Warning:** Poor preprocessing can reduce OCR accuracy by 40%. Try improving preprocessing before switching models.

## Image Preprocessing

```python
import cv2
import numpy as np

def prepare_for_ocr(img_path: str) -> np.ndarray:
    img = cv2.imread(img_path)
    if img is None:
        raise FileNotFoundError(f"{img_path} not found")

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Otsu thresholding — automatically picks threshold between two peaks
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Noise reduction — clean small spots
    denoised = cv2.medianBlur(binary, 3)

    # Deskewing — straighten text if tilted
    coords = np.column_stack(np.where(denoised < 127))  # Black pixel coordinates
    if len(coords) > 0:
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle += 90
        if abs(angle) > 0.5:  # If tilt > 0.5 degrees, straighten
            h, w = denoised.shape
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            denoised = cv2.warpAffine(denoised, M, (w, h),
                                       flags=cv2.INTER_CUBIC,
                                       borderMode=cv2.BORDER_REPLICATE)

    return denoised

prepared = prepare_for_ocr("invoice.jpg")
cv2.imshow("Preprocessed", prepared)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Black text on a white background (or vice versa) is the standard OCR engines expect. Otsu thresholding automatically picks the correct threshold for both handwriting and printed text.

## Tesseract

Developed and open-sourced by Google, Tesseract supports over 100 languages, including Turkish. First install the Tesseract binary on your system (`brew install tesseract` or `sudo apt install tesseract-ocr`), then `pip install pytesseract`.

```python
import cv2
import pytesseract

# For Windows, set the binary path:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = cv2.imread("document.jpg")
if img is None:
    raise FileNotFoundError("document.jpg not found")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Extract plain text — lang: tur for Turkish, eng for English
text = pytesseract.image_to_string(binary, lang="tur")
print("Recognized text:\n", text)

# Bounding box + confidence score
data = pytesseract.image_to_data(binary, lang="tur", output_type=pytesseract.Output.DICT)

for i, word in enumerate(data["text"]):
    if word.strip() and int(data["conf"][i]) > 60:  # Confidence threshold
        x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
        cv2.putText(img, word, (x, y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

cv2.imshow("Tesseract Results", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Tesseract's PSM (Page Segmentation Mode) parameter describes text layout:

- `--psm 6`: Single uniform text block (invoice, book page)
- `--psm 7`: Single line of text (license plate, heading)
- `--psm 11`: Sparse text, scattered locations (form fields, labels)

```python
custom_config = r"--psm 6 --oem 3"  # OEM 3: LSTM + legacy engine combined
text = pytesseract.image_to_string(binary, lang="tur", config=custom_config)
```

> **💡 Tip:** For mixed Turkish + English documents, use `lang="tur+eng"`. Check which languages are installed with `tesseract --list-langs`.

## EasyOCR

EasyOCR supports over 80 languages, accelerates with GPU, and installs as easily as `pip install easyocr`. Each detection returns a `[bounding_box, text, confidence]` triple.

```python
import cv2
import easyocr
import numpy as np

img = cv2.imread("mixed_language_document.jpg")
if img is None:
    raise FileNotFoundError("mixed_language_document.jpg not found")

# On first run, model files (~500MB) are downloaded
reader = easyocr.Reader(["tr", "en"], gpu=False)  # Set gpu=True if CUDA available
results = reader.readtext(img)

overlay = img.copy()

for (bbox, text, confidence) in results:
    if confidence < 0.4:
        continue

    # bbox: [[x1,y1],[x2,y1],[x2,y2],[x1,y2]] quadrilateral corners
    pts = np.array(bbox, dtype=np.int32).reshape((-1, 1, 2))
    cv2.polylines(overlay, [pts], isClosed=True, color=(0, 200, 255), thickness=2)

    # Text label at top-left corner
    x, y = int(bbox[0][0]), int(bbox[0][1])
    label = f"{text} ({confidence:.2f})"
    cv2.putText(overlay, label, (x, max(y - 6, 10)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 255), 1)
    print(f"'{text}' — confidence: {confidence:.2f}")

cv2.imshow("EasyOCR Results", overlay)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

EasyOCR returns quadrilateral bounding boxes (Tesseract returns rectangles) — providing more accurate positioning on tilted text.

> **💡 Tip:** For mixed Turkish + English documents, pass the language list `["tr", "en"]`. The longer the list, the slower startup — add only the languages you need.

## EAST: Text Detection

Tesseract and EasyOCR do detection and recognition together. Sometimes it's better to first answer "where is text in this image?" and then pass those regions to a separate recognizer.

EAST (Efficient and Accurate Scene Text Detector) detects tilted and multi-oriented text even on street signs and billboards — it's powerful for scene text.

```python
import cv2
import numpy as np

net = cv2.dnn.readNet("frozen_east_text_detection.pb")

img = cv2.imread("street_sign.jpg")
if img is None:
    raise FileNotFoundError("street_sign.jpg not found")

orig_h, orig_w = img.shape[:2]

# EAST requires dimensions that are multiples of 32
new_w, new_h = (orig_w // 32) * 32, (orig_h // 32) * 32
blob = cv2.dnn.blobFromImage(
    cv2.resize(img, (new_w, new_h)), 1.0, (new_w, new_h),
    (123.68, 116.78, 103.94), swapRB=True, crop=False,
)

net.setInput(blob)
layer_names = ["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]
scores, geometry = net.forward(layer_names)

# Filter detected boxes
rows, cols = scores.shape[2], scores.shape[3]
boxes, confidences = [], []

for y in range(rows):
    for x in range(cols):
        score = float(scores[0, 0, y, x])
        if score < 0.5:
            continue

        offset_x = x * 4.0
        offset_y = y * 4.0
        angle = float(geometry[0, 4, y, x])
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)
        h_box = float(geometry[0, 0, y, x]) + float(geometry[0, 2, y, x])
        w_box = float(geometry[0, 1, y, x]) + float(geometry[0, 3, y, x])

        end_x = int(offset_x + cos_a * geometry[0, 1, y, x] + sin_a * geometry[0, 2, y, x])
        end_y = int(offset_y - sin_a * geometry[0, 1, y, x] + cos_a * geometry[0, 2, y, x])
        start_x = int(end_x - w_box)
        start_y = int(end_y - h_box)

        # Scale to original image dimensions
        sx = orig_w / new_w
        sy = orig_h / new_h
        boxes.append((int(start_x * sx), int(start_y * sy),
                       int(end_x * sx), int(end_y * sy)))
        confidences.append(score)

# NMS to clean overlapping boxes
indices = cv2.dnn.NMSBoxes(
    [(x, y, x2 - x, y2 - y) for x, y, x2, y2 in boxes],
    confidences, 0.5, 0.4,
)

for i in indices.flatten():
    x1, y1, x2, y2 = boxes[i]
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.imshow("EAST Text Detection", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

## Method Comparison

| Method | Language Support | Speed | Accuracy | Setup |
|--------|-----------------|-------|----------|--------|
| Tesseract | 100+ languages | Medium | Medium-high (clean documents) | pip + binary |
| EasyOCR | 80+ languages | Slow (CPU) / fast (GPU) | High | pip (downloads models) |
| PaddleOCR | 80+ languages | Fast | Very high | pip (heavy dependencies) |
| EAST (detection only) | — (detection only) | Fast | Strong on tilted text | .pb file required |

## Summary

- The OCR pipeline has three steps: preprocessing → detection → recognition. Each affects the next.
- Otsu thresholding, noise reduction, and deskewing are the core preprocessing steps.
- Tesseract adapts to different text layouts with PSM modes; it works in Turkish with `lang="tur"`.
- EasyOCR returns quadrilateral bounding boxes — better than Tesseract's rectangles for tilted text.
- EAST answers "where is text?" first; it excels at tilted and multi-directional scene text.
- Filtering low confidence (`conf < 0.5`) is the easiest way to clean up misreadings.
- GPU accelerates EasyOCR and PaddleOCR 5-10× faster than CPU.

## Further Reading

- Shi et al., "An End-to-End Trainable Neural Network for Image-based Sequence Recognition (CRNN)" (IEEE TPAMI 2017): https://arxiv.org/abs/1507.05717
- Zhou et al., "EAST: An Efficient and Accurate Scene Text Detector" (CVPR 2017): https://arxiv.org/abs/1704.03155
- Tesseract OCR Documentation: https://tesseract-ocr.github.io/tessdoc
- EasyOCR GitHub: https://github.com/JaidedAI/EasyOCR
