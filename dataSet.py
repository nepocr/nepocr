'''
dataSet.py
Training data synthesizer


USAGE: this program uses the font files and font data with random offsets and rotations to create
randomly oriented and placed training data.
font2images(fontCharSet, fontAttachment, "name of font")

RETURNS: A number of folders with training data

'''

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import PIL.ImageOps
import random as r
import os


#character set and attachment set for the fonts
#using क in front of attachment without space aligns it to the left of main charset
rukminiCharSet = "s v u 3 8= r 5 h em ` 6 7 8 9 0f t y b w g k km a e d o / n j z ; if x If q 1"
rukminiAttachments = " f कl L ' \" ] } f] f} + M"

preetiCharSet = "s v u 3 8= r 5 h em ` 6 7 8 9 0f t y b w g k km a e d o / n j z ; if x If q 1"
preetiAttachments = " f कl L ' \" ] } f] f} + M"


#Utilites For Image Transformations

#Rotate paste and return the image
def rotate_image(imgSrc, angle, image_size):
    dst_im = Image.new("L", (image_size, image_size), 0)
    rot = imgSrc.rotate(angle).resize(
        (image_size, image_size), Image.BILINEAR)
    center = int(image_size * 0.5)
    dst_im.paste(rot, (0, 0), rot)
    return dst_im


#To be implemented skew features
def skew_image():
    return None

#Convert text to image
def image_char(font_path, char, image_size, font_size):
    img = Image.new("L", (image_size, image_size), 0)

    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(font_path, font_size)

    #draw.text((0, 0)," "+char+" ", 0, font=font)
    draw.text((r.randint(1, 6), r.randint(0, 3)), char + " ", 255, font=font)
    return img
    # img.show()
    # img.save(os.path.join(dir, fileName + ".jpeg"), "JPEG")


#Iterate through charset and attachment set to create training data
def font2images(charSet, charAttachments, font_path="Preeti_0.ttf", imgDir="images", numInEach=50):
    convUnicode = "क ख ग घ ड. च छ ज झ ञ ट ठ ड ढ ण त थ द ध न प फ ब भ म य र ल व श स ष ह क्ष त्र ज्ञ"
    convUnicodeAttach = "ा ि ी ु ू े ै ो ौ ं ः"
    # Split the char sets for both font and unicode
    charList = charSet.split()
    charAttachmentsList = charAttachments.split()
    charAttachmentsList.insert(0, '')

    unicodeList = convUnicode.split()
    unicodeAttachmentsList = convUnicodeAttach.split()
    unicodeAttachmentsList.insert(0, '')

    print(font_path)

    # Loop to create directory and images within it
    for i in range(0, len(charList)):

        # looping through attachments

        for atInd in range(0, len(charAttachmentsList)):
            # if folder is not present create it
            pathReq = os.path.join(imgDir, str(i) + '_' + str(atInd))

            # the final attached string

            # if ka is attached in front then the attache should be kept in
            # front
            if("क" in charAttachmentsList[atInd]):
                toAtch = charAttachmentsList[atInd].replace("क", "")
                actChar = toAtch + charList[i]
            else:
                actChar = charList[i] + charAttachmentsList[atInd]

            unicodeChar = unicodeList[i] + unicodeAttachmentsList[atInd]

            if not os.path.isdir(pathReq):
                os.makedirs(pathReq)
                print ("Creating ", i, unicodeChar)
            else:
                print ("Already Exists", unicodeChar)

            for j in range(0, numInEach):
                img = image_char(font_path,   # fontName.ttf
                                 actChar,  # character
                                 30,          # image size
                                 25          # font size
                                 )

                img_rot = rotate_image(img, r.randint(-15, 15), 30)
                img = PIL.ImageOps.invert(img)
                img_rot = PIL.ImageOps.invert(img_rot)

                img.save(
                    os.path.join(pathReq, str(j) + "_" + font_path.split('.')[0] + ".jpeg"), "JPEG")

                img_rot.save(
                    os.path.join(pathReq, str(j) + "_" + font_path.split('.')[0] + "_rot.jpeg"), "JPEG")


#Create the test set
def font2imagesTest(charSet, font_path="rukmini.ttf", imgDir="images_test"):
    convUnicode = "क ख ग घ ड. च छ ज झ ञ ट ठ ड ढ ण त थ द ध न प फ ब भ म य र ल व श स ष ह क्ष त्र ज्ञ"
    convUnicodeAttach = "ा ि ी ु ू े ै ो ौ ं ः"
    # Split the char sets for both font and unicode
    charList = charSet.split()
    unicodeList = convUnicode.split()

    if not os.path.isdir(imgDir):
        os.makedirs(imgDir)

    for i in range(0, len(charList)):
        image_char(font_path,
                   charList[i],
                   30,
                   25,
                   imgDir,
                   unicodeList[i]
                   )


if __name__ == "__main__":
    font2images(preetiCharSet, rukminiAttachments, "rukmini.ttf")
    font2images(preetiCharSet, preetiAttachments, "Preeti_0.ttf")
    font2images(preetiCharSet, preetiAttachments, "Preeti_Bold.ttf")
