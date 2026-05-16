# Bilgisayarlı Görü Kitabı — Kapsamlı Revizyon & Genişletme Tasarımı

**Tarih:** 2026-05-16  
**Kapsam:** Mevcut 25 bölümün akademik derinlikle revizyonu + 6 yeni bölüm eklenmesi  
**Dil:** Türkçe (öncelikli), İngilizce çeviri sonraki aşama  
**Hedef:** Hem üniversite öğrencisi hem pratisyen geliştiriciyi kapsayan katmanlı kaynak

---

## 1. Hedef Kitle

- **Başlangıç katmanı:** Lisans/yüksek lisans öğrencisi, CV'ye yeni başlıyor, temel matematik bilgisi var
- **İleri katman:** Yazılım geliştirici / araştırmacı, OpenCV ve modern DL framework'lerini kullanmak istiyor

Her bölüm her iki kitleye hitap eder: teorik kısım öğrenciyi, kod kısmı geliştiriciyi karşılar.

---

## 2. İçerik Standardı (Her Bölüm İçin Zorunlu Şablon)

```markdown
## [Bölüm Adı]

### Teorik Temel
- Konunun akademik tanımı ve tarihsel bağlamı
- Matematiksel formüller (inline LaTeX: $f(x)$, blok: $$...$$)
- Her formülün sezgisel Türkçe açıklaması
- Kilit paper referansları: [Yazar et al., Yıl](arXiv/DOI linki)

### Algoritma / Yöntem Detayı
- Adım adım açıklama (numaralı liste)
- Yöntemler arası karşılaştırma tablosu (avantaj/dezavantaj/kullanım durumu)

### Pratik Uygulama
- Tam çalışan Python kodu (kopyala-çalıştır, gereksiz import yok)
- Gerçek dünya senaryosu (neden bu yöntemi seçtik)
- Beklenen çıktı açıklaması

### Özet & İleri Okuma
- Madde madde kilit çıkarımlar (5-7 madde)
- Önerilen kaynaklar (paper, kitap, kurs)
```

---

## 3. İçerik Haritası

### 3.1 Revize Edilecek Mevcut Bölümler (15 bölüm)

| # | Dosya | Revizyon Odağı |
|---|-------|----------------|
| 1 | `docs/1-opencv-nedir.md` | OpenCV 5.0 ekosistemi, tarihsel bağlam, alternatif kütüphaneler karşılaştırması |
| 2 | `docs/6-giris-temel-kavramlar.md` | Piksel matematiği, matris teorisi, renk modeli formülleri, görüntü uzayı |
| 3 | `docs/8-goruntu-manipulasyonu.md` | Affine/perspektif dönüşüm matrisleri, interpolasyon teorisi |
| 4 | `docs/9-renk-uzaylari.md` | Renk uzayı dönüşüm matrisleri, perceptual color theory, ICC profilleri |
| 5 | `docs/10-morfolojik-goruntu-isleme.md` | Minkowski sum matematiği, structuring element seçimi, morfolojik gradyan |
| 6 | `docs/11-filtreler-ve-kenar-belirleme.md` | Konvolüsyon teorisi, Fourier analizi, Canny iki eşik matematiği |
| 7 | `docs/12-arka-plan-cikarma.md` | GMM istatistiksel model, EM algoritması, Bayesian yaklaşım |
| 8 | `docs/13-video-analiz.md` | Optik akış denklemleri (Lucas-Kanade, Horn-Schunck), Kalman filtresi |
| 9 | `docs/14-nesne-tespiti.md` | YOLO mimarisi (anchor, loss, NMS), mAP/IoU/precision-recall matematiği |
| 10 | `docs/15-kamera-kalibrasyonu-ve-3d-goru.md` | Pinhole model, epipolar geometri, DLT algoritması |
| 11 | `docs/17-yuz-tanima.md` | PCA/LDA matematiği, FaceNet triplet loss, ArcFace margin |
| 12 | `docs/18-optik-karakter-tanima.md` | CTC loss türetimi, attention mekanizması, seq2seq mimarisi |
| 13 | `docs/19-oznitelik-cikarimi.md` | SIFT matematiksel türetim, descriptor L2 normalizasyonu, RANSAC |
| 14 | `docs/21-poz-tahmini.md` | Keypoint heatmap regresyon, PAF (Part Affinity Fields), OKS metriği |
| 15 | `docs/22-segmentasyon.md` | Mask R-CNN pipeline, SAM (Segment Anything) mimarisi, IoU/mIoU |

### 3.2 Eklenecek Yeni Bölümler (6 bölüm)

| # | Dosya | Konu | Kilit Konular |
|---|-------|------|---------------|
| 26 | `docs/26-vision-transformers.md` | Vision Transformers | ViT patch embedding, multi-head self-attention, DETR, Swin Transformer, DeiT |
| 27 | `docs/27-generatif-modeller.md` | Generatif Modeller & Diffusion | GAN eğitim dinamikleri, VAE ELBO, DDPM forward/reverse süreç, Stable Diffusion, ControlNet |
| 28 | `docs/28-3d-vision.md` | 3D Vision | Nokta bulutu (PointNet), NeRF radiance field, monoküler derinlik tahmini, SLAM |
| 29 | `docs/29-video-siniflandirma.md` | Video Anlama | Action recognition, SlowFast ağları, VideoMAE, temporal modeling |
| 30 | `docs/30-model-egitimi-ve-degerlendirme.md` | Model Eğitimi & Değerlendirme | Dataset hazırlık, augmentation stratejileri, mAP/F1/confusion matrix, transfer learning |
| 31 | `docs/31-vision-language-modeller.md` | Vision-Language Modeller | CLIP (contrastive loss), LLaVA, InstructPix2Pix, multimodal reasoning |

---

## 4. Agent Koordinasyon Stratejisi

### Paralellik Modeli

Tüm bölümler birbirinden bağımsız — paylaşılan state yok. 4 grup **aynı anda** başlar:

```
GRUP A — Temel Bölümler (6 agent paralel)
  Bölüm 6, 8, 9, 10, 11, 12

GRUP B — Orta Seviye Revizyon (5 agent paralel)
  Bölüm 13, 14, 15, 17, 18

GRUP C — İleri Seviye Revizyon (4 agent paralel)
  Bölüm 1, 19, 21, 22

GRUP D — Yeni Bölümler (6 agent paralel)
  Bölüm 26, 27, 28, 29, 30, 31
```

### Her Agent'ın Protokolü

1. Hedef `.md` dosyasını oku (varsa mevcut içerik)
2. Bölüm 2'deki standart şablonu uygula
3. Teorik kısım: formüller + referanslar ekle
4. Kod kısmı: tam çalışan Python (OpenCV 4.9+ / PyTorch / Ultralytics)
5. Git commit at

### Tamamlanma Sonrası

Tüm agentlar bitince ayrı bir görev:
- `README.md` tablosunu güncelle (yeni bölümler eklenir)
- `docs/terimler.md` yeni akademik terimlerle genişletilir

---

## 5. Teknik Kısıtlar

- **Dil:** Türkçe (tüm açıklamalar), kod değişkenleri İngilizce
- **Python versiyonu:** 3.10+
- **OpenCV:** 4.9+ (cv2)
- **DL Framework:** PyTorch (tercih), TensorFlow/Keras (alternatif olarak gösterilir)
- **Matematiksel gösterim:** GitHub Markdown'da inline `$...$` ve blok `$$...$$` LaTeX
- **Kod bloğu dili:** Her zaman `python` tag ile
- **Görseller:** Mevcut `docs/static/` klasörü kullanılır, yeni görseller için placeholder açıklama

---

## 6. Başarı Kriterleri

- [ ] Her revize bölümde en az 1 akademik paper referansı
- [ ] Her bölümde en az 1 matematiksel formül (sezgisel açıklamalı)
- [ ] Her bölümde en az 1 tam çalışan Python kodu bloğu
- [ ] Yeni 6 bölüm oluşturuldu ve README'ye eklendi
- [ ] Terimler sözlüğü güncellendi
