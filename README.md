[![Downloads](https://img.shields.io/npm/dm/eslint-config-airbnb-base.svg)](https://www.npmjs.com/package/eslint-config-airbnb-base) [![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/airbnb/javascript?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

# Görüntü İşleme ve Bilgisayarlı Görü


OpenCV ile bilgisayarlı görü ve görüntü işleme eğitim dokümanı içerisinde görüntü işleme algoritmalarını öğrenecek yeri geldiğinde ise **Java**, **Python** yeri geldiğinde ise **Csharp** programlama dilleri kullanarak örnek uygulamalara geliştireceğiz. Bu doküman daha önce görüntü işleme ile uğraşmamış veya farklı kütüphaneleri kullanmış OpenCV öğrenmek isteyenlere yöneliktir. Temel kavramlardan başlayarak birçok kavram ve algoritma ele alınmıştır. Yer alan örnek uygulamalar birçok farklı sürümü kullanılarak geliştirilmiştir. Gereken yerlerde sürümler arası farklılıklara değinilmiştir, **yararlı olması dileğiyle.**

---

<p align="center">
 ★★★ Dokumantasyonu beğendiyseniz ve destek olmak isterseniz; anlatım bozuklukları, kod değişikliği veya yeni bir örnek göndermekten çekinmeyin. Buradaki dokümantasyonun orijinaline <a href="http://mesutpiskin.com/blog">bu adresten</a> ulaşabilirsiniz. İletişime geçmek isterseniz  <a href="https://github.com/mesutpiskin">profilimdeki</a> eposta adresini kullanabilirsiniz. Teşekkürler! ★★★
</p>

---

## İçerik
 1. **GİRİŞ VE TEMEL KAVRAMLAR**
	* [OpenCV Nedir?](#default-methods-for-interfaces)
	* [Neden OpenCV](#lambda-expressions)
	* [OpenCV Wrappers](#lambda-expressions)
		* [Wrappers vs OpenCV](#lambda-scopes)
		* [EmguCV](#functional-interfaces)
		* [JavaCV](#method-and-constructor-references)
		* [LiveCV](#method-and-constructor-references)
		* [OpenCV.js](#method-and-constructor-references)
	* [OpenCV 2 vs OpenCV 3](#accessing-local-variables)
	* [Platform ve Geliştirme Ortamı Seçimi](#accessing-fields-and-static-variables)
	* Derleme ve Kurulum
		* [Windows](#built-in-functional-interfaces)
		* [Linux](#built-in-functional-interfaces)
		* [macOS](#built-in-functional-interfaces)
		* [Raspberry Pi](#built-in-functional-interfaces)
	* Geliştirme Ortamları için Yapılandırma
		* [Eclipse](#built-in-functional-interfaces)
		* [Netbeans](#built-in-functional-interfaces)
		* [Android Studio](#built-in-functional-interfaces)

 2. **GÖRÜNTÜ I/O VE RENK UZAYLARI**
	* [Temel Kavramlar](#default-methods-for-interfaces)
	* Görüntü Okuma
		*  [Dosya Sistemleri](#default-methods-for-interfaces)
		*  [Video Kamera](#default-methods-for-interfaces)
		*  [IP Kamera](#default-methods-for-interfaces)
	* [Görüntü Stream Etme](#default-methods-for-interfaces)
	* [Java için imshow()](#default-methods-for-interfaces)
	* Görüntü Yazma
		* [Temel Video Write](#default-methods-for-interfaces)
		* [Codec ve FourCC](#default-methods-for-interfaces)
	* [Piksel İşlemleri](#default-methods-for-interfaces)
	* [Yeniden Boyutlandırma](#default-methods-for-interfaces)
	*  [Çizim İşlemleri](#default-methods-for-interfaces)
	*  [Görüntü Kırpma](#default-methods-for-interfaces)
	*  [Java ile GUI](#default-methods-for-interfaces)
	*  [Renk Uzayları](#default-methods-for-interfaces)
		* [Renk Uzayı Dönüşümü](#default-methods-for-interfaces) 

 3. **GÜRÜLTÜ, FİLTRE VE KENAR ÇIKARMA**
	* [Morfolojik Operatörler ve Filtreler](#default-methods-for-interfaces)
		* [Erosion (Aşındırma)](#default-methods-for-interfaces)
		* [Dilation (Yayma – Genişletme)](#default-methods-for-interfaces)
		* [Opening (Açınım)](#default-methods-for-interfaces)
		* [Closing (Kapanım)](#default-methods-for-interfaces)
		* [Morphological Gradient](#default-methods-for-interfaces)
		* [Top Hat](#default-methods-for-interfaces)
	* [Thresholding (Eşikleme)](#default-methods-for-interfaces)
	* [Filtreler](#default-methods-for-interfaces)
	* [Kenar Belirleme Algoritmaları](#default-methods-for-interfaces)
	* [Görüntü Bozulmaları ve Kamera Kalibrasyonu](#default-methods-for-interfaces)

4. **ARKA PLAN ÇIKARMA VE HAREKET ANALİZİ**
	* [Arka Plan Çıkarma](#default-methods-for-interfaces)
		* [Absdiff](#default-methods-for-interfaces)
		* [BackgroundSubtractorMOG](#default-methods-for-interfaces)
		* [BackgroundSubtractorMOG2](#default-methods-for-interfaces)
		* [BackgroundSubtractorGMG](#default-methods-for-interfaces)
	* [Ağırlıklı Ortalama Öteleme (Mean Shift)](#default-methods-for-interfaces)
	* Camshift
	* Optik Akış

4. **NESNE TESPİTİ, YÜZ TANIMA, MAKİNE ÖĞRENMESİ VE DERİN ÖĞRENME**
	* Temel Kavramlar
		* [Nesne Tespiti ve Nesne Tanıma Süreçleri](#default-methods-for-interfaces)
		* [Nesne Tespit Yöntemleri](#default-methods-for-interfaces)
	* Renk Tabanlı Nesne Tespiti
		* [Bölüm 1](#default-methods-for-interfaces)
		* [Bölüm 2](#default-methods-for-interfaces)
	* [Haar Cascades Sınıflandırıcısı](#default-methods-for-interfaces)
		* [Örnek 1: Yüz Tespiti](#default-methods-for-interfaces)
		* [Örnek 2: Yüz, Göz ve Burun Tespiti](#default-methods-for-interfaces)
	* Yüz Tanıma
		* [Yüz Tanımaya Giriş](#default-methods-for-interfaces)
		* [Eigenfaces, Fisherfaces, LBPH](#default-methods-for-interfaces)
			* [Örnek 1: JavaCV ile Yüz Tanıma](#default-methods-for-interfaces)
			* [Örnek 2: EmguCV ile Yüz Tanıma](#default-methods-for-interfaces)
	* SIFT
	* SURF
	* Derin Öğrenme
		* [Derin Sinir Ağı ile Nesne Tanıma (DNN)](#default-methods-for-interfaces)
		* Deeplearning4j	
			* [Deeplearning4j ile Derin Öğrenmeye Giriş ](#default-methods-for-interfaces)
			* [Deeplearning4j Mimarisi](#default-methods-for-interfaces)
			* [Yapay Sinir Ağları (ANN)](#default-methods-for-interfaces)			
			* [İleri Beslemeli Sinir Ağı ile El Yazısı Sınıflandırma](#default-methods-for-interfaces)
		* Caffe Kütüphanesi
			* [Windows için Caffe Kurulumu](#default-methods-for-interfaces)			
		* TensorFlow Kütüphanesi
			* [Sınıflandırıcı Eğitimi ve Görüntü Sınıflandırma](#default-methods-for-interfaces)	
		* Dlib Kütüphanesi
			* [Dlib ile Makine Öğrenimi ve Görüntü İşlemeye Giriş](#default-methods-for-interfaces)	
	* KNN, K En Yakın Komşu
	* SVM, Destek Vektör Makinesi
