# Öznitelik Çıkarımı ve Eşleştirme

İki farklı açıdan çekilmiş aynı binanın fotoğrafını panorama hâline getirmek istiyorsunuz. Bunun için bilgisayarın iki görüntüdeki aynı noktaları — binanın köşesini, pencere pervazını, kapı tutamağını — bulması ve hizalaması gerekir. Ama piksel piksel karşılaştırma yaparsanız, ışık farkı veya ufak bir açı değişikliği eşleşmeyi mahveder. Bu bölümde bu sorunu çözen öznitelik (feature) dedektörlerini ve tanımlayıcıları inceleyeceğiz; ardından iki görüntüyü gerçekten hizalayana kadar gideceğiz.

## Öznitelik Nedir?

Görüntünün "dikkat çeken" bölgeleridir öznitelikler — köşeler, lekeler (blob), belirgin kenarlar. İyi bir öznitelik, bakış açısı değişse de, nesne yaklaştırılıp uzaklaştırılsa da, sahne daha aydınlık veya daha karanlık olsa da tanınabilir olmak zorundadır. Bu üç dayanıklılığa sırasıyla **döndürme değişmezliği**, **ölçek değişmezliği** ve **aydınlık değişmezliği** denir.

Neden köşe? Düz bir kenar hayal edin: boyunca kaydırsanız fark etmezsiniz — görüntü aynı kalır. Köşe ise iki yönde de bilgi taşır; sizi tam olarak o noktaya sabitler. Taklit edilemeyen, tekrarlanabilir bir referans noktasıdır.

> **📌 Not:** Dedektör (detector) ilgi noktasını *nerede* bulacağını söyler; tanımlayıcı (descriptor) o noktanın etrafının *nasıl göründüğünü* sayısal bir vektöre dönüştürür. İkisi birlikte çalışır.

## SIFT: Ölçek Değişmezliği

Görüntüyü bir büyüteçle inceler gibi farklı büyütme seviyelerinde tarayan bir algılama yöntemi düşünün. Nesne yakın veya uzakta olsa bile her ölçekte belirgin olan noktalar gerçek özniteliklerdir — bunları bulan algoritma SIFT'tir (Scale-Invariant Feature Transform).

**Nasıl çalışır, özet olarak:**

1. Görüntüyü farklı sigma değerleriyle Gaussian blur ile yumuşat.
2. Ardışık iki Gaussian'ın farkını al — bu DoG (Difference of Gaussians) görüntüleridir.
3. DoG piramidinde yerel maksimum ve minimum noktaları ilgi noktası olarak işaretle.
4. Her noktanın etrafındaki 16×16 piksellik pencereyi 4×4 hücreye böl; her hücrede 8 yön içeren gradyan histogramı hesapla. Sonuç: 128 boyutlu bir vektör — noktanın parmak izi.

128 boyutlu bu vektör, döndürmeye ve ölçek değişimine dayanıklıdır çünkü hem ana yönü hizalanarak normalize edilmiş hem de ölçek uzayında lokalize edilmiştir.

> **📌 Not:** OpenCV 4.4'ten itibaren SIFT patent koruması sona ermiştir ve ana `opencv-python` paketinde mevcuttur; artık `opencv-contrib-python` gerekmez.

```python
import cv2
import numpy as np

def sift_oznitelikler(goruntu_yolu: str) -> None:
    """SIFT ile öznitelik tespit et ve görselleştir."""
    img = cv2.imread(goruntu_yolu)
    if img is None:
        raise FileNotFoundError(f"{goruntu_yolu} bulunamadı")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    sift = cv2.SIFT_create(nfeatures=500)
    keypoints, descriptors = sift.detectAndCompute(gray, None)

    print(f"Bulunan anahtar nokta sayısı : {len(keypoints)}")
    print(f"Tanımlayıcı matrisi boyutu   : {descriptors.shape}")  # (N, 128)

    # Anahtar noktaları görselleştir
    img_kp = cv2.drawKeypoints(
        img, keypoints, None,
        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
    )
    cv2.imshow("SIFT Anahtar Noktaları", img_kp)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    sift_oznitelikler("bina.jpg")
```

`DRAW_RICH_KEYPOINTS` bayrağı her noktanın ölçeğini (daire çapı) ve baskın yönünü (çizgi) de çizer — hangi ölçekte tespit edildiğini ve yönelimi görmek için kullanışlıdır.

## ORB: Hız ve Patent Özgürlüğü

SIFT iyi çalışır, ama her piksel için 128 float hesaplamak mobil cihazda veya gömülü sistemde yavaştır. ORB (Oriented FAST + Rotated BRIEF) bu sorunu farklı bir stratejiyle çözer: anahtar noktaları FAST köşe dedektörüyle bulur, tanımlayıcıyı ise float değil **binary** (0/1 bit dizisi) olarak üretir.

İki binary descriptor'ı karşılaştırmak kolaydır: XOR alırsınız, 1-bitleri sayarsınız. Bu işlem, Hamming mesafesidir ve CPU'da son derece hızlı çalışır. SIFT'e kıyasla yaklaşık 100 kat daha hızlı çalışır.

```python
import cv2
import numpy as np

def orb_oznitelikler(goruntu_yolu: str) -> None:
    """ORB ile öznitelik tespit et ve görselleştir."""
    img = cv2.imread(goruntu_yolu)
    if img is None:
        raise FileNotFoundError(f"{goruntu_yolu} bulunamadı")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create(nfeatures=500)
    keypoints, descriptors = orb.detectAndCompute(gray, None)

    print(f"Bulunan anahtar nokta sayısı : {len(keypoints)}")
    print(f"Tanımlayıcı matrisi boyutu   : {descriptors.shape}")  # (N, 32) — 256 bit

    img_kp = cv2.drawKeypoints(img, keypoints, None, color=(0, 255, 0))
    cv2.imshow("ORB Anahtar Noktaları", img_kp)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    orb_oznitelikler("bina.jpg")
```

ORB tanımlayıcısı 32 byte (256 bit) uzunluğundadır — SIFT'in 512 byte'ının çok altında. Bellek kısıtlı ortamlarda bu fark belirleyicidir.

## Öznitelik Eşleştirme

İki görüntüden çıkarılan tanımlayıcılar elimizde. Soru şu: hangi nokta hangi noktaya karşılık gelir?

### Kaba Kuvvet Eşleştirici (BFMatcher)

Her tanımlayıcıyı diğer görüntünün tüm tanımlayıcılarıyla karşılaştırır — yavaştır ama en doğru eşleşmeyi verir.

- SIFT gibi float tanımlayıcılar için `cv2.NORM_L2` (Öklid mesafesi)
- ORB gibi binary tanımlayıcılar için `cv2.NORM_HAMMING`

### FLANN Eşleştirici

FLANN (Fast Library for Approximate Nearest Neighbors), büyük tanımlayıcı setlerinde kaba kuvvetten çok daha hızlıdır. Yaklaşık en yakın komşu araması yapar — ufak doğruluk kaybı karşılığında büyük hız kazancı.

### Lowe Oran Testi

Ham eşleştirme çıktısı gürültülüdür — pek çok yanlış eşleşme içerir. David Lowe'un SIFT makalesinde önerdiği **oran testi** bunu filtreler:

Her tanımlayıcı için en yakın iki eşleşmeyi bul. En yakın, ikinci en yakından çok daha yakınsa eşleşme güvenilirdir. Formüle dökersek:

$$\text{eşleşme geçerli} \iff d_1 < 0.75 \cdot d_2$$

Sezgi: İyi bir eşleşme rakipsiz olmalıdır. Eğer ikinci aday da neredeyse aynı uzaklıktaysa, birinci adayın doğru olduğundan emin olamayız.

> **⚠️ Dikkat:** Oran testi uygulamadan doğrudan ham eşleşmeleri kullanmayın — yanlış eşleşmeler, sonraki homografi hesabını mahveder.

```python
import cv2
import numpy as np

def oznitelik_eslestir(yol1: str, yol2: str) -> tuple:
    """SIFT + FLANN + Lowe oran testi ile iki görüntüyü eşleştir."""
    img1 = cv2.imread(yol1)
    img2 = cv2.imread(yol2)
    if img1 is None:
        raise FileNotFoundError(f"{yol1} bulunamadı")
    if img2 is None:
        raise FileNotFoundError(f"{yol2} bulunamadı")

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # SIFT özniteliklerini çıkar
    sift = cv2.SIFT_create()
    kp1, desc1 = sift.detectAndCompute(gray1, None)
    kp2, desc2 = sift.detectAndCompute(gray2, None)

    # FLANN parametreleri (SIFT için)
    index_params = dict(algorithm=1, trees=5)   # FLANN_INDEX_KDTREE = 1
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # k=2: her nokta için en yakın 2 eşleşme
    matches = flann.knnMatch(desc1, desc2, k=2)

    # Lowe oran testi
    iyi_eslesmeler = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            iyi_eslesmeler.append(m)

    print(f"Toplam eşleşme   : {len(matches)}")
    print(f"Lowe testi sonrası: {len(iyi_eslesmeler)}")

    return img1, img2, kp1, kp2, iyi_eslesmeler
```

## Homografi ve RANSAC ile Görüntü Hizalama

Güvenilir eşleşmeler elimizde. Şimdi iki görüntü arasındaki **perspektif dönüşümünü** bulmamız gerekiyor — buna homografi denir. Homografi, bir düzlemden diğerine her noktayı doğru konuma taşıyan 3×3 bir matristir.

Sorun şu: bazı eşleşmeler hâlâ yanlış olabilir (aykırı değer / outlier). RANSAC (Random Sample Consensus) bu durumla başa çıkar: rastgele 4 nokta çifti seçer, homografi tahmin eder, diğer noktaların ne kadarı bu modele uyuyor diye bakar. En fazla noktayı açıklayan model kazanır.

```python
import cv2
import numpy as np

def goruntu_hizala(yol1: str, yol2: str) -> None:
    """SIFT + FLANN + Lowe + Homografi ile iki görüntüyü hizala ve kaydet."""
    img1, img2, kp1, kp2, iyi_eslesmeler = oznitelik_eslestir(yol1, yol2)

    if len(iyi_eslesmeler) < 10:
        print("Yeterli eşleşme bulunamadı.")
        return

    # Eşleşen nokta koordinatlarını numpy dizisine çevir
    src_pts = np.float32([kp1[m.queryIdx].pt for m in iyi_eslesmeler]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in iyi_eslesmeler]).reshape(-1, 1, 2)

    # RANSAC ile homografi bul
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, ransacReprojThreshold=5.0)
    inlier_sayisi = int(mask.sum())
    print(f"RANSAC inlier sayısı: {inlier_sayisi} / {len(iyi_eslesmeler)}")

    # img1'i img2'nin perspektifine dönüştür
    h2, w2 = img2.shape[:2]
    warped = cv2.warpPerspective(img1, H, (w2, h2))

    # Eşleşmeleri görselleştir (sadece inlier'lar)
    matchesMask = mask.ravel().tolist()
    draw_params = dict(
        matchColor=(0, 255, 0),
        singlePointColor=None,
        matchesMask=matchesMask,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )
    img_matches = cv2.drawMatches(img1, kp1, img2, kp2, iyi_eslesmeler, None, **draw_params)

    cv2.imshow("Eşleşmeler (RANSAC inlier)", img_matches)
    cv2.imshow("Hizalanmış Görüntü", warped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite("eslesmeler.jpg", img_matches)
    cv2.imwrite("hizalanmis.jpg", warped)
    print("eslesmeler.jpg ve hizalanmis.jpg kaydedildi.")

def oznitelik_eslestir(yol1: str, yol2: str) -> tuple:
    img1 = cv2.imread(yol1)
    img2 = cv2.imread(yol2)
    if img1 is None:
        raise FileNotFoundError(f"{yol1} bulunamadı")
    if img2 is None:
        raise FileNotFoundError(f"{yol2} bulunamadı")

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    sift = cv2.SIFT_create()
    kp1, desc1 = sift.detectAndCompute(gray1, None)
    kp2, desc2 = sift.detectAndCompute(gray2, None)

    index_params = dict(algorithm=1, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(desc1, desc2, k=2)

    iyi_eslesmeler = [m for m, n in matches if m.distance < 0.75 * n.distance]

    return img1, img2, kp1, kp2, iyi_eslesmeler

if __name__ == "__main__":
    goruntu_hizala("bina_sol.jpg", "bina_sag.jpg")
```

Çıktı iki dosya üretir: `eslesmeler.jpg` iki görüntü yan yana eşleşme çizgileriyle, `hizalanmis.jpg` ise birinci görüntünün ikincinin perspektifine dönüştürülmüş hâlidir.

> **💡 İpucu:** `ransacReprojThreshold=5.0` değeri piksel cinsinden yeniden projeksiyon hatasına toleransı belirtir. Görüntü yüksek çözünürlüklüyse 5-10 piksel makul; düşük çözünürlüklüyse 2-3 deneyin.

## Yöntem Karşılaştırması

| Yöntem | Doğruluk | Hız | Patent | En İyi Kullanım |
|--------|----------|-----|--------|-----------------|
| **SIFT** | Yüksek | Yavaş | Özgür (4.4+) | Panorama, 3D yeniden yapılandırma, araştırma |
| **ORB** | Orta | Çok hızlı | Özgür | Mobil uygulama, gömülü sistem, gerçek zamanlı AR |
| **AKAZE** | Yüksek | Orta | Özgür | Doku zengin sahneler, rotasyon değişmezliği kritik |

> **📌 Not:** Hassasiyet kritik değilse ve cihaz kaynakları kısıtlıysa ORB genellikle yeterlidir. Araştırma kalitesinde sonuç gerekiyorsa SIFT veya AKAZE tercih edin.

## Özet & İleri Okuma

- Öznitelik dedektörü, görüntüdeki ilgi noktalarını bulur; tanımlayıcı, bu noktaların görünümünü sayısal vektöre dönüştürür.
- SIFT, DoG piramidiyle ölçek değişmezliği sağlar ve 128 boyutlu float tanımlayıcı üretir; OpenCV 4.4+'tan itibaren patentsizdir.
- ORB, binary tanımlayıcı kullandığı için Hamming mesafesiyle SIFT'ten ~100x hızlı karşılaştırma yapar.
- FLANN, büyük tanımlayıcı setlerinde kaba kuvvetten çok daha hızlı yaklaşık eşleştirme sunar.
- Lowe oran testi (`d1 < 0.75 * d2`) yanlış eşleşmeleri etkili şekilde eleminasyon eder — her zaman uygulanmalıdır.
- Homografi, iki görüntü arasındaki perspektif dönüşümünü tanımlar; RANSAC aykırı eşleşmelere rağmen doğru tahmini bulmayı sağlar.
- `cv2.findHomography` + `cv2.warpPerspective` ikilisi, panorama ve görüntü hizalama boru hatlarının temelini oluşturur.

### Referanslar

- Lowe, D.G. (2004). "Distinctive Image Features from Scale-Invariant Keypoints." *IJCV*: https://doi.org/10.1023/B:VISI.0000029664.99615.94
- Rublee, E. et al. (2011). "ORB: An efficient alternative to SIFT or SURF." *ICCV 2011.*
- Alcantarilla, P. et al. (2012). "KAZE Features." *ECCV 2012.*
- Fischler, M. & Bolles, R. (1981). "Random Sample Consensus." *CACM*: https://doi.org/10.1145/358669.358692
