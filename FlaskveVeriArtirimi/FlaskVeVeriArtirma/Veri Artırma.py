import os
import cv2


def AsilFotolar(klasor_yolu,fotograflar):
    for dosya_adi in os.listdir(klasor_yolu):
        dosya_yolu = os.path.join(klasor_yolu, dosya_adi)
        if os.path.isfile(dosya_yolu) and dosya_adi.endswith('.jpg'):
            img = cv2.imread(dosya_yolu)
            fotograflar.append(img)
    return fotograflar


def Rotationlar(klasor_yolu,fotograflar):
    for i in range(0, len(fotograflar)):
        (h, w) = fotograflar[i].shape[:2]
        (cX, cY) = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D((cX, cY), 90, 1.0)
        rotated = cv2.warpAffine(fotograflar[i], M, (w, h))
        cv2.imwrite("{}/90{}.jpg".format(klasor_yolu, i + 1), rotated)
        fotograflar.append(rotated)

        N = cv2.getRotationMatrix2D((cY, cX), 180, 1.0)
        rotated2 = cv2.warpAffine(fotograflar[i], N, (w, h))
        cv2.imwrite("{}/180{}.jpg".format(klasor_yolu,i + 2), rotated2)
        fotograflar.append(rotated2)

        B = cv2.getRotationMatrix2D((cY, cX), 270, 1.0)
        rotated3 = cv2.warpAffine(fotograflar[i], B, (w, w))
        cv2.imwrite("{}/270{}.jpg".format(klasor_yolu,i + 3), rotated3)
        fotograflar.append(rotated3)
    return fotograflar


def Verticallar(klasor_yolu,fotograflar):
    for i in range(0, len(fotograflar)):
        flipVertical = cv2.flip(fotograflar[i], 0)
        cv2.imwrite("{}/FlipVertical{}.jpg".format(klasor_yolu,i + 1), flipVertical)
        fotograflar.append(flipVertical)
        flipHorizontal = cv2.flip(fotograflar[i], 1)
        cv2.imwrite("{}/FlipVertical{}.jpg".format(klasor_yolu,i + 2),
                    flipHorizontal)
        fotograflar.append(flipHorizontal)
        flipBoth = cv2.flip(fotograflar[i], -1)
        cv2.imwrite("{}/flipBoth{}.jpg".format(klasor_yolu,i + 3), flipBoth)
        fotograflar.append(flipBoth)
    return fotograflar


def BlurBright(klasor_yolu,fotograflar):
    for i in range(0, len(fotograflar)):
        median = cv2.medianBlur(fotograflar[i], 5)
        cv2.imwrite("{}/Blur{}.jpg".format(klasor_yolu,i + 1), median)
        #contrast = 1.4
        #brightness = 100
        #out = cv2.addWeighted(fotograflar[i], contrast, fotograflar[i], 0, brightness)
        #cv2.imwrite("{}/Brightness{}.jpg".format(klasor_yolu,i + 2), out)
        contrast = 1.8
        contrasted_image = cv2.convertScaleAbs(fotograflar[i], alpha=contrast)


        cv2.imwrite("{}/contrast{}.jpg".format(klasor_yolu,i + 2), contrasted_image)


        brightness = 40
        brightened_image = cv2.add(fotograflar[i], brightness)


        cv2.imwrite("{}/brightened{}.jpg".format(klasor_yolu,i + 2), brightened_image)
    return fotograflar



klasor_yolu = 'Fotograflar'

alt_klasorler = []
for klasor_adi in os.listdir(klasor_yolu):
    klasor_yol = os.path.join(klasor_yolu, klasor_adi)
    if os.path.isdir(klasor_yol):
        alt_klasorler.append(klasor_adi)


for x in alt_klasorler:
    fotograflar = []
    x = "Fotograflar/" + x
    foto = AsilFotolar(x,fotograflar)
    foto1 = Rotationlar(x,foto)
    foto2 = Verticallar(x, foto1)
    foto3 = BlurBright(x, foto)


