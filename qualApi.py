import requests
from configparser import ConfigParser
import zipfile
import io
import time
import datetime as dt
import csv
import pandas as pd
import os

"""*********************************************************************************************************************
    Define functions
*********************************************************************************************************************"""


def removeFile(fileName):
    try:
        if os.path.exists(fileName):
            os.remove(fileName)
            print('OS Check: ' + fileName + ' exists and was removed due to pre-processing rules')
        else:
            print('OS Check: ' + fileName + ' does not exist, proceed as planned')
    except PermissionError:
        os.chmod(fileName, stat.S_IRWXO)
        os.remove(fileName)
        print('OS Check: ' + fileName + ' was locked for editing by another user. The file mode was changed to allow '
                                        + 'deletion')


'''*********************************************************************************************************************
                                            Set up Variables To be used
*********************************************************************************************************************'''
cfg = ConfigParser()
cfg.read(r'C:\Users\JefferyMcCain\Documents\PythonFiles\PrincetonQualtrics\QualtricsApi\venv\qualCred.txt')
apiToken = cfg.get('qualtrics', 'apiToken')
surveyId = cfg.get('surveys', 'saCore')
dataCenter = 'az1'
fileFormat = 'csv'
"""********************************************************
    API Related Variables
********************************************************"""
v4ExportBaseurl = 'https://az1.qualtrics.com/API/v3/surveys/' + surveyId + '/export-responses'
v3ExportBaseurl = 'https://az1.qualtrics.com/API/v3/responseexports/'
progressStatus = 'inProgress'
getSurveyBaseUrl = 'https://az1.qualtrics.com/API/v3/surveys/' + surveyId
requestCheckProgress = 0
progressStatus = "in progress"

"""*******************************************************
    Time Related Variables: used to uniquely name files
*******************************************************"""
yesterday = (dt.datetime.utcnow() - dt.timedelta(days=1))
yesterdayDateFormat = yesterday.strftime("%Y-%m-%d")
currentTime = yesterday.strftime("%H.%M.%S")


"""******************************************************
    Create File Names
******************************************************"""

QualtricsDnldFilePath = r"C:\Users\JefferyMcCain\Documents\Consulting\Athlete View\DataDumps\OutputFiles"

QualtricsDnldFile = QualtricsDnldFilePath + r"\SA Core Survey.csv"

surveyResultCSV = r'C:\Users\JefferyMcCain\Documents\Consulting\Athlete View\DataDumps\OutputFiles\SA Core Survey.csv'

doNotPivotFile = r'C:\Users\JefferyMcCain\Documents\Consulting\Athlete View\DoNotPivotQuestions.csv'

embeddedDataFileName = r'C:\Users\JefferyMcCain\Documents\Consulting\Athlete View\DataDumps\OutputFiles' \
    '\EmbeddedSurveyResults' + ".txt"

outputPivotFile = r'C:\Users\JefferyMcCain\Documents\Consulting\Athlete View\DataDumps\OutputFiles' \
                  r'\PivotedSurveyResults' + ".txt"


"""********************************
    Test Connection to API
********************************"""
# testUrl ='https://az1.qualtrics.com/API/v3/surveys'
# testCall = requests.get(testUrl, headers=header)
# print(testCall.status_code)
# print(testCall.content)


"""*********************************************************************************************************************
                                Make Call to Qualtrics and begin download process
*********************************************************************************************************************"""
header = {'X-API-Token': apiToken, "content-type": "application/json"}
downloadRequestUrl = v3ExportBaseurl
downloadRequestPayload = '{"format":"' + fileFormat + '","surveyId":"' + surveyId + '"}'
downloadRequestResponse = requests.request("POST", downloadRequestUrl, data=downloadRequestPayload, headers=header)
print(downloadRequestResponse.text)
progressId = downloadRequestResponse.json()["result"]["id"]

"""***************************************************************************************
    Check on Data Export Progress and waiting until export is ready
***************************************************************************************"""
isFile = None

while requestCheckProgress < 100 and progressStatus is not "complete" and isFile is None:
    requestCheckUrl = v3ExportBaseurl + progressId
    requestCheckResponse = requests.request("GET", requestCheckUrl, headers=header)
    isFile = (requestCheckResponse.json()["result"]["file"])
    if isFile is None:
        print("file not ready")
    else:
        print("file created:", requestCheckResponse.json()["result"]["file"])
    requestCheckProgress = requestCheckResponse.json()["result"]["percentComplete"]
    print("Download is " + str(requestCheckProgress) + " complete")
    time.sleep(5)


"""********************************************
    Download the file
********************************************"""
requestDownloadUrl = v3ExportBaseurl + progressId + '/file'
requestDownload = requests.request("GET", requestDownloadUrl, headers=header, stream=True)

"""************************************
    Unzip and save the file
************************************"""
zipfile.ZipFile(io.BytesIO(requestDownload.content)).extractall(path=QualtricsDnldFilePath)
print('File Downloaded and Placed')


"""*********************************************************************************************************************
                                    Create | delimited output files
*********************************************************************************************************************"""


'''***************************************************
     Set Up Pivoted Data File to be written
***************************************************'''
removeFile(outputPivotFile)
removeFile(embeddedDataFileName)
writer = csv.writer(open(outputPivotFile, 'a', encoding='utf8'), delimiter="|")
header = ['ResponseID', 'Question', 'Answer']
rowCount = 1

'''***************************************************
    Create List of Questions to not pivot
***************************************************'''
doNotPivot = []
with open(doNotPivotFile) as file:
        doNotPivotReader = csv.reader(file, delimiter=",")
        for row in doNotPivotReader:
            doNotPivot.append(row[0])


'''**************************************************
        Write Pivoted Data Output File
**************************************************'''
csvFile = open(QualtricsDnldFile, 'r', encoding='utf8')
pivotedReader = csv.DictReader(csvFile)
# print(pivotedReader.fieldnames)
writer.writerow(header)
for row in pivotedReader:
    responseId = row['ResponseID']
    rowCount = rowCount + 1
    for item in row:
        listOfItems = [rowCount, responseId, item, row[item]]
        if listOfItems[0] > 3:
            if listOfItems[3] != "":
                surveyResults = listOfItems[1:]
                if surveyResults[1] not in doNotPivot:
                    # print(listOfItems[1:])
                    writer.writerow(surveyResults)

print('Pivoted Data File Complete')
'''**************************************************
        Write Embedded Data Output File
**************************************************'''
embeddedData = pd.read_csv(QualtricsDnldFile, usecols=doNotPivot, skiprows=(1, 2), dtype=object)
embeddedDataFile = pd.DataFrame.to_csv(embeddedData, embeddedDataFileName, sep="|", index=False)
csvFile.close()
print("Embedded Data File Complete")
print('Process Complete')


