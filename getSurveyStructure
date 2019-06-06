import json
import csv
from datetime import datetime
import requests
from configparser import ConfigParser

surveyId = 'SV_dou8kym9HnbJ00d'

"""Set up Names For Files Written"""
runDate = datetime.utcnow().strftime('%Y.%m.%d.T.%H.%M.%S')
jsonFileName = r'C:\Users\JefferyMcCain\Documents\Consulting\Athlete View\DataDumps\SurveyStructures\getSurveyResult_' + surveyId + '_' + runDate + '.json'
credentialFile = r'C:\Users\JefferyMcCain\Documents\PythonFiles\PrincetonQualtrics\QualtricsApi\venv\qualCred.txt'

"""Make Get Survey Request"""
cfg = ConfigParser()
cfg.read(credentialFile)
apiToken = cfg.get('qualtrics', 'apiToken')
# surveyId = cfg.get('surveys', 'saCore')
dataCenter = cfg.get('qualtrics', 'dataCenter')
userId = cfg.get('qualtrics', 'userId')
baseUrl = "https://az1.qualtrics.com/API/v3/surveys/" + surveyId
headers = {
    "x-api-token": apiToken,
    }

"""Mapping Live to API"""
response = requests.get(baseUrl, headers=headers)
data = response.json()

with open(jsonFileName, 'w') as f:
    data = json.dump(data, f)

