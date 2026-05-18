[Türkçe](./22-segmentasyon.md) | English

# Segmentation

In a pathology lab, you want to detect tumor cells in a microscope image. Object detection might tell you "there's a tumor in this region," but it doesn't answer "which exact pixels belong to the tumor?" You need to draw the cell boundary at the pixel level: how many cells are there, what's their total area, are they adjacent? In this section, you'll learn segmentation methods that classify every pixel in an image to the correct object or class.

## Types of Segmentation

There are three different segmentation approaches — choose based on what question you're asking.

**Semantic segmentation:** Every pixel is assigned to a class. If there are five people in the image, they all fall into the "person" class — they're not distinguished from each other. It answers "where is road and where is building in this image?"

**Instance segmentation:** Each object is independent. Five people get separate masks: "person_1", "person_2", etc. It answers "how many cells are there and where is each one?"

**Panoptic segmentation:** It combines both. Countable objects (people, cars) use instance segmentation; background classes (sky, road, ground) use semantic segmentation.

| Type | Each object separate? | Background class? | Example Use |
|------|--------------------|--------------------|------------|
| Semantic | No | Yes | Lane detection for autonomous vehicles |
| Instance | Yes | No | Cell counting, crowd analysis |
| Panoptic | Yes | Yes | Scene understanding, autonomous navigation |

## Classical Method: Watershed

Think of an image like a terrain map: bright regions are mountain peaks, dark regions are valleys. Fill the valleys with water — the boundaries where waters meet before merging form object boundaries. This intuition is the Watershed algorithm, used to separate objects with known shapes (cells, mineral grains).

```python
import cv2
import numpy as np

def watershed_count_cells(image_path: str) -> int:
    """Use Watershed to count and separate bright objects (cells)."""
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"{image_path} not found")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Thresholding — bright cells become white
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    # Define certain background and foreground regions
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    dist = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist, 0.5 * dist.max(), 255, 0)
    sure_fg = sure_fg.astype(np.uint8)

    # Uncertain region
    unknown = cv2.subtract(sure_bg, sure_fg)

    # Marker matrix
    _, markers = cv2.connectedComponents(sure_fg)
    markers += 1
    markers[unknown == 255] = 0

    # Apply Watershed
    cv2.watershed(img, markers)
    img[markers == -1] = [0, 0, 255]   # Mark boundaries in red

    # Count regions
    cell_count = markers.max() - 1   # 1 = background
    print(f"Detected cell count: {cell_count}")

    cv2.imshow("Watershed Result", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return int(cell_count)

if __name__ == "__main__":
    count = watershed_count_cells("cells.jpg")
```

> **💡 Tip:** Watershed shines when objects are close or touching (cells, mineral grains) and simple thresholding fails. The distance transform computes each pixel's distance to the nearest background — its peaks mark each object's center.

## YOLOv8-seg: Real-Time Instance Segmentation

YOLOv8 adds pixel mask generation on top of the object detection pipeline. Alongside the detection head, a mask head runs — producing a binary pixel mask for each detected object.

```bash
pip install ultralytics opencv-python numpy
```

```python
import cv2
import numpy as np
from ultralytics import YOLO

def yolov8_segmentation_camera() -> None:
    """Real-time instance segmentation from camera with YOLOv8-seg."""
    model = YOLO("yolov8n-seg.pt")   # Nano model; speed-focused

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Camera could not be opened")

    # Color palette — fixed color per class
    np.random.seed(42)
    colors = np.random.randint(0, 255, size=(80, 3), dtype=np.uint8)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, verbose=False)
        overlay = frame.copy()

        if results[0].masks is not None:
            masks = results[0].masks.data.cpu().numpy()    # (N, H, W)
            boxes = results[0].boxes
            h, w = frame.shape[:2]

            for i, mask in enumerate(masks):
                # Resize mask to original dimensions
                mask_resized = cv2.resize(mask, (w, h))
                mask_bool = mask_resized > 0.5

                # Get class color
                cls_id = int(boxes.cls[i].item())
                color = colors[cls_id % len(colors)].tolist()

                # Semi-transparent color overlay
                overlay[mask_bool] = (
                    overlay[mask_bool] * 0.4 + np.array(color) * 0.6
                ).astype(np.uint8)

                # Label
                conf = float(boxes.conf[i].item())
                label = f"{model.names[cls_id]} {conf:.2f}"
                x1, y1 = int(boxes.xyxy[i][0]), int(boxes.xyxy[i][1])
                cv2.putText(overlay, label, (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        # Blend original and overlay
        result_frame = cv2.addWeighted(frame, 0.3, overlay, 0.7, 0)
        cv2.imshow("YOLOv8-seg", result_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    yolov8_segmentation_camera()
```

The `results[0].masks.data` tensor has shape `(N, H, W)` — N detections, with H and W being small mask dimensions. You must scale to the original image size with `cv2.resize`.

> **⚠️ Warning:** If the mask tensor is on CUDA, convert with `.cpu()` first, then `.numpy()`. Skipping either step causes an error.

## SAM: Universal Segmentation

Meta's Segment Anything Model (SAM) offers a segmentation paradigm that requires no training: click a point, get the mask of the object that point belongs to. Draw a box, segment the object inside. Trained on over 1 billion masked images, SAM generalizes to object types it's never seen.

```bash
pip install segment-anything
# Download model weights (vit_b ≈ 375 MB)
# wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth
```

```python
import cv2
import numpy as np
from segment_anything import sam_model_registry, SamPredictor

def sam_point_segmentation(image_path: str, point_x: int, point_y: int) -> None:
    """Segment an object by clicking a point with SAM."""
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"{image_path} not found")

    # SAM expects RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Load model (vit_b, vit_l, vit_h)
    sam = sam_model_registry["vit_b"](checkpoint="sam_vit_b_01ec64.pth")
    predictor = SamPredictor(sam)
    predictor.set_image(img_rgb)

    # Predict — point coordinate and label (1 = foreground, 0 = background)
    masks, scores, _ = predictor.predict(
        point_coords=np.array([[point_x, point_y]]),
        point_labels=np.array([1]),
        multimask_output=True   # Produce 3 alternative masks
    )

    # Choose the highest-scoring mask
    best = np.argmax(scores)
    mask = masks[best]

    print(f"Mask score    : {scores[best]:.3f}")
    print(f"Mask area     : {mask.sum()} pixels "
          f"({100 * mask.mean():.1f}% of image)")

    # Visualize
    overlay = img.copy()
    overlay[mask] = (overlay[mask] * 0.4 + np.array([0, 120, 255]) * 0.6).astype(np.uint8)
    cv2.circle(overlay, (point_x, point_y), 8, (255, 0, 0), -1)

    cv2.imshow("SAM Segmentation", overlay)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite("sam_result.jpg", overlay)
    print("sam_result.jpg saved.")

if __name__ == "__main__":
    sam_point_segmentation("lab.jpg", point_x=320, point_y=240)
```

With `multimask_output=True`, SAM produces three masks at different granularities (fragment, object, group). In most cases, the highest-scoring mask is what you want.

> **📌 Note:** SAM requires large model weights (vit_b: 375 MB, vit_h: 2.4 GB). For real-time apps, explore lighter variants like MobileSAM or EfficientSAM.

## Evaluation: IoU and mIoU

How accurate is your predicted mask? We measure this with **IoU (Intersection over Union)**.

The intuition: the overlap ratio between the predicted and true masks. Perfect overlap → 1, no overlap → 0.

$$\text{IoU} = \frac{|P \cap G|}{|P \cup G|}$$

The numerator is intersection (pixels in both masks), the denominator is union (pixels in at least one).

```python
import numpy as np

def calculate_iou(prediction: np.ndarray, ground_truth: np.ndarray) -> float:
    """
    Calculate IoU between two binary masks.
    prediction, ground_truth: bool or uint8 (0/1) ndarray
    """
    prediction = prediction.astype(bool)
    ground_truth = ground_truth.astype(bool)

    intersection = (prediction & ground_truth).sum()
    union = (prediction | ground_truth).sum()

    if union == 0:
        return 1.0   # Both empty = perfect overlap

    return float(intersection) / float(union)

def calculate_miou(predictions: list, ground_truths: list) -> float:
    """Calculate mIoU across multiple classes or instances."""
    iou_values = [calculate_iou(p, g) for p, g in zip(predictions, ground_truths)]
    return float(np.mean(iou_values))

# Test
pred = np.array([[1, 1, 0], [1, 0, 0]], dtype=bool)
gt   = np.array([[1, 1, 1], [0, 0, 0]], dtype=bool)
print(f"IoU: {calculate_iou(pred, gt):.3f}")   # 2/4 = 0.5
```

**mIoU (mean IoU)** is the average IoU across all classes or instances. It's the standard evaluation metric for segmentation models — you'll see "COCO val mIoU" in papers.

> **💡 Tip:** An IoU of 0.5 is a widely accepted success threshold (PASCAL VOC standard). Medical imaging usually expects higher thresholds (0.7-0.9).

## Method Comparison

| Method | Speed | Accuracy | Requires Training? | Best Use |
|--------|-------|----------|-------------------|----------|
| **Watershed** | Very fast | Limited | No | Known-shape objects, cell counting |
| **YOLOv8n-seg** | Fast (~30 FPS GPU) | Medium-high | Fine-tune optional | Real-time, multi-class |
| **YOLOv8x-seg** | Slow (~5 FPS GPU) | Very high | Fine-tune optional | Accuracy-critical apps |
| **SAM (vit_b)** | Medium | Very high | No | Interactive segmentation, data labeling |

> **📌 Note:** SAM is too slow for real-time video; but integrating it with labeling tools (Roboflow, Label Studio) dramatically cuts annotation workload.

## Summary & Further Reading

- Semantic segmentation classifies pixels; instance segmentation keeps each object separate; panoptic combines both.
- Watershed uses distance transform and markers to separate touching objects — a classical tool.
- YOLOv8-seg returns `results[0].masks.data` as `(N, H, W)` tensors; scale to original size with `cv2.resize`.
- Semi-transparent mask overlay uses `cv2.addWeighted` or NumPy alpha blending.
- SAM needs no training — segment anything from point/box input; vit_b model is 375 MB.
- IoU measures overlap between prediction and ground truth (0-1); mIoU averages across all classes.
- Don't forget `.cpu().numpy()` conversion if masks are on CUDA.

### References

- He, K. et al. (2017). "Mask R-CNN." *ICCV 2017*: https://arxiv.org/abs/1703.06870
- Kirillov, A. et al. (2023). "Segment Anything." *ICCV 2023*: https://arxiv.org/abs/2304.02643
- Jocher, G. et al. (2023). "Ultralytics YOLOv8." https://github.com/ultralytics/ultralytics
- Watershed Documentation (OpenCV): https://docs.opencv.org/4.x/d3/db4/tutorial_py_watershed.html
