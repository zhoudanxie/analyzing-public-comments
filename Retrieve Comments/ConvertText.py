#--------------------------------------Convert Attachment (DOC & PDF) Comments to Text---------------------------------#
#---------------------------------------------The GW Regulatory Studies Center-----------------------------------------#
#--------------------------------------------------Author: Zhoudan Xie-------------------------------------------------#

# Import packages
import sys
import os
import comtypes.client
from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path
import fitz
import json

filePath="Retrieve Comments/Comment Attachments/"   #! Specify the path of the folder where the comment attachments are saved

#-------------------------------------------Convert DOC files to PDF----------------------------------------------------
# Define a function to convert doc to pdf
def docToPdf(filePath,fileName):
    wdFormatPDF = 17

    in_file = os.path.abspath(filePath+fileName+'.doc')
    out_file = os.path.abspath(filePath+fileName+'.pdf')

    word = comtypes.client.CreateObject('Word.Application')
    word.Visible = False
    doc = word.Documents.Open(in_file)
    doc.SaveAs(out_file, FileFormat=wdFormatPDF)
    doc.Close()
    word.Quit()

# Convert DOC comments to PDF
for file in os.listdir(filePath):
    if file.endswith(".doc"):
        fileName = str(file).split('.doc')[0]
        if os.path.isfile(filePath + fileName + ".pdf"):
            pass
        else:
            docToPdf(filePath,fileName)

#---------------------------------------------Convert PDF files to text-------------------------------------------------
# Define a function to convert scanned PDF to text
def convertScanPDF(file):
    ## Part 1 : Converting PDF to images
    # Store all the pages of the PDF in a variable
    pages = convert_from_path(file, 500)
    # Counter to store images of each page of PDF to image
    image_counter = 1
    # Iterate through all the pages stored above
    for page in pages:
        # Declaring filename for each page of PDF as JPG
        # For each page, filename will be:
        # PDF page 1 -> page_1.jpg
        # ....
        # PDF page n -> page_n.jpg
        filename = "page_" + str(image_counter) + ".jpg"
        # Save the image of the page in system
        page.save(filename, 'JPEG')
        # Increment the counter to update filename
        image_counter = image_counter + 1

    ##Part 2 - Recognizing text from the images using OCR
    # Variable to get count of total number of pages
    filelimit = image_counter - 1
    text=''
    # Iterate from 1 to total number of pages
    for i in range(1, filelimit + 1):
        # Set filename to recognize text from
        # Again, these files will be:
        # page_1.jpg
        # page_2.jpg
        # ....
        # page_n.jpg
        filename = "page_" + str(i) + ".jpg"
        # Recognize the text as string in image using pytesserct
        new_text = str(((pytesseract.image_to_string(Image.open(filename)))))
        # The recognized text is stored in variable text.
        # Any string processing may be applied on text
        # Here, basic formatting has been done: In many PDFs, at line ending, if a word can't be written fully,
        # a 'hyphen' is added. The rest of the word is written in the next line. Eg: This is a sample text this
        # word here GeeksF-orGeeks is half on first line, remaining on next. To remove this, we replace every '-\n' to ''.
        new_text = new_text.replace('-\n', '')
        # Finally, write the processed text to the file.
        text += new_text
    return text

# Convert PDF comments to text
dic_pdfComments={}
notConverted=[]
for file in os.listdir(filePath):
    if file.endswith(".pdf"):
        doc = fitz.open(filePath+file)
        fileName=str(file).split('.pdf')[0]
        num_pages = doc.pageCount
        count = 0
        text = ""
        while count < num_pages:
            page = doc[count]
            count += 1
            text += page.getText('text')
        if text != "":
            text=text.replace('\n',' ')
            dic_pdfComments.update({fileName: text})
        else:
            try:
                text = convertScanPDF(filePath+file)
                text = text.replace('\n', ' ')
                dic_pdfComments.update({fileName: text})
            except:
                notConverted.append(file)
        doc.close
print("The number of PDF files that have been converted to text is:", len(dic_pdfComments))
if len(notConverted)>0:
    print("The following PDF files could not be converted:")
    print(notConverted)
print("END")

#---------------------------------------------Export converted text-------------------------------------------------
# Export to JSON
js_pdfComments=json.dumps(dic_pdfComments)
with open('Retrieve Comments/Attachment Comments Example.json', 'w', encoding='utf-8') as f:
    json.dump(js_pdfComments, f, ensure_ascii=False, indent=4)
