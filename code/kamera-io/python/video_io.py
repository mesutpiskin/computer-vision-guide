import cv2


def web_kamera():
    #Varsayılan kamera
    capture = cv2.VideoCapture(0)
    while True:
        ret, frame = capture.read()
        # alınan görüntüyü göster
        cv2.imshow('Web Kamera',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def video_dosyasi():
    capture = cv2.VideoCapture("videodosyasi.avi")
    while True:
        ret, frame = capture.read()
        # alınan görüntüyü göster
        cv2.imshow('Video Dosyası',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def ip_kamera():
    #Kullanıcı adı ve şifre ile local ip kamera yayınına erişim
    capture = cv2.VideoCapture("http://admin:admin@192.168.1.51/cgi/stream.mjpg")
    while True:
        ret, frame = capture.read()
        # alınan görüntüyü göster
        cv2.imshow('Web Kamera',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def fotograf_oku():
    img = cv2.imread('foto.jpg')
    cv2.imshow('Fotoğraf',img)


def main():
    web_kamera()
    #video_dosyasi()
    #ip_kamera()
    #fotograf_oku()

if __name__ == '__main__':
    main()