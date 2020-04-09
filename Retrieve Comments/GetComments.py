#-----------------------------------------Retrieve Comments from Regulations.gov---------------------------------------#
#---------------------------------------------The GW Regulatory Studies Center-----------------------------------------#
#--------------------------------------------------Author: Zhoudan Xie-------------------------------------------------#

# Import packages
import pandas as pd
import urllib
import json
import time
import os

#-----------------------------------------------------------------------------------------------------------------------
#--------------------------------------------Get comments by Document ID------------------------------------------------

docketFile='Retrieve Comments/DocketExample.csv'    #! Specify the path of your docket metadata file exported from Regulation.gov
docket = pd.read_csv(docketFile,skiprows=4)
docket=docket[docket['Document Type']=='PUBLIC SUBMISSIONS']

APIkey="YOUR API KEY"   #! Add your API key here

#------------------------------------------Retrieve text comments-------------------------------------------------------

saveFile='Retrieve Comments/Text Comments Example.csv'   #! Specify the path and name of the file you want to save the text comments as

if os.path.isfile(saveFile):
    commentsRetrieved=pd.read_csv(saveFile)
    dic_comments=commentsRetrieved.set_index('Document ID')['Text Comment'].T.to_dict()
else:
    dic_comments = {}

baseURL = "https://api.data.gov:443/regulations/v3/document.json?api_key="+APIkey+"&documentId="
commentCount=len(docket['Document ID'])     # It may take a long time if you are requesting a large number of comments
print("Total number of text comments you are requesting is:", commentCount)

while len(dic_comments)<commentCount:
    print("Number of text comments you have retrieved is:", len(dic_comments), "(requesting more...)")
    for docID in docket['Document ID']:
        comment=""
        if docID in dic_comments.keys():
            pass
        else:
            try:
                request = urllib.request.urlopen(baseURL + docID)
                comment = json.loads(request.read())['comment']['value']
                dic_comments.update({docID: comment})
                time.sleep(0.2)     # Sleep to avoid the Too Many Requests error due to the rate limit set by Regulations.gov
            except:
                commentsRetrieved = pd.DataFrame(dic_comments, index=[0]).T.reset_index().rename(
                    columns={'index': 'Document ID', 0: 'Text Comment'})
                commentsRetrieved.to_csv(saveFile, index=False)
                time.sleep(60)      # Sleep longer if you have reached the rate limit
                pass
else:
    if len(dic_comments)==commentCount:
        print("Number of text comments you have retrieved is:", len(dic_comments), "(request completed)")
        print("END")
textComments = pd.DataFrame(dic_comments,index=[0]).T.reset_index().rename(columns={'index': 'Document ID',0:'Text Comment'})
textComments.to_csv(saveFile,index=False)


#----------------------------Retrieve comments submitted as PDF or DOC attachments--------------------------------------

docket_att=docket[docket["Attachment Count"].notnull()]

baseURL1 = "https://api.data.gov/regulations/v3/download?api_key="+APIkey+"&documentId="
baseURL2="&attachmentNumber="
baseURL3_pdf="&contentType=pdf"
baseURL3_doc="&contentType=msw"

folderPath="Retrieve Comments/Comment Attachments/"    #! Specify the path of the folder where you want to save the downloaded files

totalAtt=sum(docket_att['Attachment Count'])    # It may take a long time if you are downloading a large number of attachments
print("Total number of attachments you are requesting to downloaded is:", totalAtt)
downloaded=[]
undownloaded=[]
attempt=0
max_attempt=10    # Define the maximum times you want to loop over the docket metadata file
while (len(downloaded)<totalAtt) & (attempt<=max_attempt):
    if attempt>1:
        print("Number of attachments you have downloaded is:", len(downloaded),"(downloading more...)")
    for docID in docket_att["Document ID"]:
        no=1
        attNo = docket_att[docket_att["Document ID"] == docID]["Attachment Count"].values[0]
        while no <= attNo:
            fileName=docID+"_"+str(no)
            if (os.path.isfile(folderPath+docID+"_"+str(no)+".pdf")) or (os.path.isfile(folderPath+fileName+".doc")):
                if fileName not in downloaded:
                    downloaded.append(fileName)
                pass
            else:
                try:
                    urllib.request.urlretrieve(baseURL1 + docID + baseURL2 + str(no) + baseURL3_pdf, folderPath+fileName+".pdf")
                    downloaded.append(fileName)
                    time.sleep(5)      # Sleep to avoid the Too Many Requests error due to the rate limit set by Regulations.gov
                except:
                    try:
                        urllib.request.urlretrieve(baseURL1 + docID + baseURL2 + str(no) + baseURL3_doc,
                                                   folderPath + fileName + ".doc")
                        downloaded.append(fileName)
                        time.sleep(5)  # Sleep to avoid the Too Many Requests error due to the rate limit set by Regulations.gov
                    except:
                        if attempt==max_attempt:
                            undownloaded.append(fileName)
                        time.sleep(60)  # Sleep longer if you have reached the rate limit
                        pass
            no=no+1
    attempt=attempt+1
else:
    if len(downloaded)==totalAtt:
        print("Number of attachments you have downloaded is:", len(downloaded), "(downloading completed)")
    else:
        print("Number of attachments you have downloaded is:", len(downloaded), "(downloading incompleted)")
        print("Request attempts exceeded "+str(max_attempt)+". The following file(s) could not be downloaded:")
        print(undownloaded)
        print("Note: You need to manually download the attachments not in PDF or DOC format.")
    print("END")
