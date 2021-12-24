from PIL import Image
from pytesseract import pytesseract
# pytesseract.pytesseract.tesseract_cmd = "C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
text = pytesseract.image_to_string(Image.open("hjNum.png"),lang="eng",config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
print(text)
text=" "+text+" "
text=text.strip().replace("\n","")
c=0
if len(text)==8 and text[2]==":" and text[5]==":":
    print(text)
    sec = (int(text[0])*10 + int(text[1]))*3600 + (int(text[3])*10 + int(text[4]))*60 + (int(text[6])*10 + int(text[7]))
else:
    print(text)

if c>13:
    sec = 600
else:
    c+=1