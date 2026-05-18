# Optik Karakter Tanıma (OCR)

Muhasebe departmanı her gün yüzlerce fatura görüntüsünü elle sisteme giriyor. Park otomasyonu araç plakasını kameradan okuyamıyor. Arşivdeki el yazısı notların aranabilir hale gelmesi gerekiyor. Üçü de aynı temel problemin farklı görünümleridir: görüntüdeki metin otomatik okunacak. Bu bölümde OCR pipeline'ının her adımını, Tesseract ve EasyOCR kullanımını ve metin tespiti ile tanımayı bir arada nasıl yapacağınızı öğreneceksiniz.

## OCR Pipeline

"Bir görüntüde metin oku" tek adım değildir. İyi bir OCR sistemi üç aşamadan oluşur:

1. **Görüntü önişleme:** Gürültü gider, kontrastı artır, metni yatay hizala.
2. **Metin tespiti:** Metnin görüntüde nerede olduğunu bul.
3. **Metin tanıma:** O bölgede ne yazıldığını oku.

Her adım bir sonrakinin başarısını belirler. Yırtık, soluk ya da eğik bir görüntü üzerinde doğrudan OCR çalıştırmak %40 daha düşük doğruluk anlamına gelebilir.

> **⚠️ Dikkat:** Kötü önişleme OCR doğruluğunu %40 düşürebilir. Modeli değiştirmeden önce önişlemeyi iyileştirmeyi deneyin.

## Görüntü Önişleme

```python
import cv2
import numpy as np

def ocr_icin_hazirla(img_path: str) -> np.ndarray:
    img = cv2.imread(img_path)
    if img is None:
        raise FileNotFoundError(f"{img_path} bulunamadı")

    # Gri dönüşüm
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Otsu eşikleme — iki tepe arasındaki eşiği otomatik seçer
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Gürültü giderme — küçük lekeleri temizle
    denoised = cv2.medianBlur(binary, 3)

    # Deskewing — metin eğriyse düzelt
    coords = np.column_stack(np.where(denoised < 127))  # Siyah piksel koordinatları
    if len(coords) > 0:
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle += 90
        if abs(angle) > 0.5:  # 0.5 dereceden büyük eğim varsa düzelt
            h, w = denoised.shape
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            denoised = cv2.warpAffine(denoised, M, (w, h),
                                       flags=cv2.INTER_CUBIC,
                                       borderMode=cv2.BORDER_REPLICATE)

    return denoised

prepared = ocr_icin_hazirla("fatura.jpg")
cv2.imshow("Önişlenmiş", prepared)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Beyaz arka plan üzerine siyah metin (veya tersi) OCR motorlarının beklediği standarttır. Otsu eşikleme el yazısı ve baskı metin için otomatik doğru eşiği seçer.

## Tesseract

Google'ın geliştirdiği ve açık kaynak haline getirdiği Tesseract 100'den fazla dili destekler; Türkçe dahil. Önce sisteme Tesseract binary yükleyin (`brew install tesseract` veya `sudo apt install tesseract-ocr`), ardından `pip install pytesseract`.

```python
import cv2
import pytesseract

# Windows için binary yolu belirtin:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = cv2.imread("belge.jpg")
if img is None:
    raise FileNotFoundError("belge.jpg bulunamadı")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Düz metin çıkar — lang: tur Türkçe, eng İngilizce
text = pytesseract.image_to_string(binary, lang="tur")
print("Okunan metin:\n", text)

# Bounding box + güven skoru
data = pytesseract.image_to_data(binary, lang="tur", output_type=pytesseract.Output.DICT)

for i, word in enumerate(data["text"]):
    if word.strip() and int(data["conf"][i]) > 60:  # Güven eşiği
        x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
        cv2.putText(img, word, (x, y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

cv2.imshow("Tesseract Sonuçları", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Tesseract PSM (Page Segmentation Mode) parametresi metnin yapısını tanımlar:

- `--psm 6`: Tek düzgün metin bloğu (fatura, kitap sayfası)
- `--psm 7`: Tek satır metin (plaka, başlık)
- `--psm 11`: Seyrek metin, farklı konumlarda (form alanları, etiketler)

```python
custom_config = r"--psm 6 --oem 3"  # OEM 3: LSTM + eski motor karma
text = pytesseract.image_to_string(binary, lang="tur", config=custom_config)
```

> **💡 İpucu:** Türkçe + İngilizce karışık belgeler için `lang="tur+eng"` kullanın. Dil paketi kurulu değilse `tesseract --list-langs` ile kontrol edin.

## EasyOCR

EasyOCR 80'den fazla dil destekler, GPU ile hızlanır, kurulumu `pip install easyocr` kadardır. Her tespit `[bounding_box, text, confidence]` üçlüsü döndürür.

```python
import cv2
import easyocr
import numpy as np

img = cv2.imread("karma_dil_belge.jpg")
if img is None:
    raise FileNotFoundError("karma_dil_belge.jpg bulunamadı")

# İlk çalıştırmada model dosyaları (~500MB) indirilir
reader = easyocr.Reader(["tr", "en"], gpu=False)  # gpu=True ise CUDA gerekli
results = reader.readtext(img)

overlay = img.copy()

for (bbox, text, confidence) in results:
    if confidence < 0.4:
        continue

    # bbox: [[x1,y1],[x2,y1],[x2,y2],[x1,y2]] dörtgen köşeleri
    pts = np.array(bbox, dtype=np.int32).reshape((-1, 1, 2))
    cv2.polylines(overlay, [pts], isClosed=True, color=(0, 200, 255), thickness=2)

    # Metin etiketini sol üst köşeye yaz
    x, y = int(bbox[0][0]), int(bbox[0][1])
    label = f"{text} ({confidence:.2f})"
    cv2.putText(overlay, label, (x, max(y - 6, 10)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 255), 1)
    print(f"'{text}' — güven: {confidence:.2f}")

cv2.imshow("EasyOCR Sonuçları", overlay)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

EasyOCR dörtgen bounding box döndürür (Tesseract dikdörtgen döndürür) — eğimli metinde daha doğru konumlandırma sağlar.

> **💡 İpucu:** Türkçe + İngilizce karışık belgeler için `["tr", "en"]` listesi verin. Dil listesi ne kadar uzun olursa başlangıç süresi o kadar artar — sadece ihtiyacınız olan dilleri ekleyin.

## EAST: Metin Tespiti

Tesseract ve EasyOCR tespit + tanımayı bir arada yapar. Ancak önce sadece "bu görüntüde metin nerede?" sorusuna cevap vermek ve ardından o bölgeleri ayrı bir tanıyıcıya vermek bazen daha iyi sonuç verir.

EAST (Efficient and Accurate Scene Text Detector) eğimli ve çok yönlü metinleri dışında bile tespit eder; sokak levhası, reklam panosu gibi sahnelerde güçlüdür.

```python
import cv2
import numpy as np

net = cv2.dnn.readNet("frozen_east_text_detection.pb")

img = cv2.imread("sokak_levhasi.jpg")
if img is None:
    raise FileNotFoundError("sokak_levhasi.jpg bulunamadı")

orig_h, orig_w = img.shape[:2]

# EAST 32'nin katı boyutlar ister
new_w, new_h = (orig_w // 32) * 32, (orig_h // 32) * 32
blob = cv2.dnn.blobFromImage(
    cv2.resize(img, (new_w, new_h)), 1.0, (new_w, new_h),
    (123.68, 116.78, 103.94), swapRB=True, crop=False,
)

net.setInput(blob)
layer_names = ["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]
scores, geometry = net.forward(layer_names)

# Tespit edilen kutucukları filtrele
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

        # Orijinal görüntü boyutuna ölçekle
        sx = orig_w / new_w
        sy = orig_h / new_h
        boxes.append((int(start_x * sx), int(start_y * sy),
                       int(end_x * sx), int(end_y * sy)))
        confidences.append(score)

# NMS ile çakışan kutuları temizle
indices = cv2.dnn.NMSBoxes(
    [(x, y, x2 - x, y2 - y) for x, y, x2, y2 in boxes],
    confidences, 0.5, 0.4,
)

for i in indices.flatten():
    x1, y1, x2, y2 = boxes[i]
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.imshow("EAST Metin Tespiti", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

## Yöntem Karşılaştırması

| Yöntem | Dil Desteği | Hız | Doğruluk | Kurulum |
|--------|------------|-----|----------|---------|
| Tesseract | 100+ dil | Orta | Orta-yüksek (temiz belge) | pip + binary |
| EasyOCR | 80+ dil | Yavaş (CPU) / hızlı (GPU) | Yüksek | pip (model indirir) |
| PaddleOCR | 80+ dil | Hızlı | Çok yüksek | pip (ağır bağımlılık) |
| EAST (tespit) | — (sadece tespit) | Hızlı | Eğimli metin için güçlü | pb dosyası gerekli |

## Özet

- OCR pipeline üç adımdan oluşur: önişleme → tespit → tanıma. Her adım sonrakini etkiler.
- Otsu eşikleme, gürültü giderme ve deskewing önişlemenin temel adımlarıdır.
- Tesseract PSM modlarıyla farklı metin düzenlerine uyum sağlar; Türkçe `lang="tur"` ile çalışır.
- EasyOCR dörtgen bounding box döndürür — eğimli metin için Tesseract'tan üstündür.
- EAST önce "metin nerede?" sorusunu çözer; sahnedeki eğimli ve çok yönlü metinlerde güçlüdür.
- Düşük güven (`conf < 0.5`) filtrelemesi yanlış okumaları temizlemenin en basit yoludur.
- GPU varsa EasyOCR ve PaddleOCR CPU'ya göre 5-10× hızlanır.

## İleri Okuma

- Shi et al., "An End-to-End Trainable Neural Network for Image-based Sequence Recognition (CRNN)" (IEEE TPAMI 2017): https://arxiv.org/abs/1507.05717
- Zhou et al., "EAST: An Efficient and Accurate Scene Text Detector" (CVPR 2017): https://arxiv.org/abs/1704.03155
- Tesseract OCR Belgeleri: https://tesseract-ocr.github.io/tessdoc
- EasyOCR GitHub: https://github.com/JaidedAI/EasyOCR
