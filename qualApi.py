import requests
from configparser import ConfigParser
import zipfile
import io
import time
import datetime as dt
import csv
# import pysftp

cfg = ConfigParser()
cfg.read(r'C:\Users\JefferyMcCain\Documents\PythonFiles\PrincetonQualtrics\QualtricsApi\venv\qualCred.txt')
apiToken = cfg.get('qualtrics','apiToken')
surveyId = cfg.get('surveys', 'saCore')
dataCenter = 'az1'
fileFormat = 'csv'
v4ExportBaseurl = 'https://az1.qualtrics.com/API/v3/surveys/' + surveyId + '/export-responses'
v3ExportBaseurl = 'https://az1.qualtrics.com/API/v3/responseexports/'
progressStatus = 'inProgress'
getSurveyBaseUrl = 'https://az1.qualtrics.com/API/v3/surveys/' + surveyId
requestCheckProgress = 0
progressStatus = "in progress"
# requestDate = (dt.datetime.utcnow().replace(microsecond=0) - dt.timedelta(days=1)).isoformat() + 'Z'
yesterday = (dt.datetime.utcnow() - dt.timedelta(days=1))
yesterdayDateFormat = yesterday.strftime("%Y-%m-%d")
currentTime = yesterday.strftime("%H.%M.%S")
requestDate = yesterdayDateFormat + "T" + '07:00:00Z'
hmsServerHost = '172.31.24.116'
hmsUserName = 'athleteviewpoint'
hmsPassword = 'AthL3te^!ewP0!nt'
QuatricsOutputFileName = r'C:\Users\JefferyMcCain\Downloads\v3.' + str(yesterdayDateFormat) \
                         + "T" + str(currentTime) +  'output.txt'
hmsServerSaveName = '/AthleteViewpoint/SA_Survey.txt'

header = {
    'X-API-Token' : apiToken,"content-type": "application/json" }

"""
Test Connection to API
"""
# testUrl ='https://az1.qualtrics.com/API/v3/surveys'
# testCall = requests.get(testUrl, headers=header)
# print(testCall.status_code)
# print(testCall.content)


downloadRequestUrl = v3ExportBaseurl
downloadRequestPayload = '{"format":"' + fileFormat + '","surveyId":"' + surveyId + '"}'
    #'","startDate":"' + requestDate + '"}'
downloadRequestResponse = requests.request("POST", downloadRequestUrl, data=downloadRequestPayload, headers=header)
print(downloadRequestResponse.text)
progressId = downloadRequestResponse.json()["result"]["id"]

# Step 2: Checking on Data Export Progress and waiting until export is ready

isFile = None

while requestCheckProgress < 100 and progressStatus is not "complete" and isFile is None:
    requestCheckUrl = v3ExportBaseurl + progressId
    requestCheckResponse = requests.request("GET", requestCheckUrl, headers=header)
    isFile = (requestCheckResponse.json()["result"]["file"])
    if isFile is None:
       print ("file not ready")
    else:
       print ("file created:", requestCheckResponse.json()["result"]["file"])
    requestCheckProgress = requestCheckResponse.json()["result"]["percentComplete"]
    print("Download is " + str(requestCheckProgress) + " complete")
    time.sleep(5)


# Step 3: Downloading file
requestDownloadUrl = v3ExportBaseurl + progressId + '/file'
requestDownload = requests.request("GET", requestDownloadUrl, headers=header, stream=True)

# Step 4: Unzipping the file
zipfile.ZipFile(io.BytesIO(requestDownload.content)).extractall(path=r"C:\Users\JefferyMcCain\Documents\Consulting\Athlete View\DataDumps\OutputFiles")

print('Complete')






try:

    with open(r'C:\Users\JefferyMcCain\Documents\Consulting\Athlete View\DataDumps\OutputFiles\SA Core Survey.csv',
              encoding="utf8") as fileIn:
        with open(QuatricsOutputFileName, 'w', newline='',
                  encoding="utf8") as fileOut:
            reader = csv.DictReader(fileIn, delimiter=",")
            writer = csv.DictWriter(fileOut, reader.fieldnames, delimiter="|" )
            writer.writeheader()
            writer.writerows(reader)
except PermissionError:
    print('Error')

###SFTP to Server
# cnopts = pysftp.CnOpts()
# cnopts.hostkeys = None
# srv = pysftp.Connection(host=hmsServerHost , username=hmsUserName,
#                         password=hmsPassword, cnopts=cnopts, port=6424)
#
# print('Connected')
#
# startDirectory = srv.pwd
#
#
# srv.put(QuatricsOutputFileName, hmsServerSaveName)
# print('File Placed')
#
# srv.close()
# print('Connection Closed')

