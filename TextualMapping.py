import json
import csv
from datetime import datetime
import requests
from configparser import ConfigParser

##Make Get Survey Request
cfg = ConfigParser()
cfg.read(r'C:\Users\JefferyMcCain\Documents\PythonFiles\PrincetonQualtrics\QualtricsApi\venv\qualCred.txt')
apiToken = cfg.get('qualtrics','apiToken')
surveyId = cfg.get('surveys', 'saCore')
dataCenter = cfg.get('qualtrics', 'dataCenter')
userId = cfg.get('qualtrics', 'userId')
baseUrl = "https://az1.qualtrics.com/API/v3/surveys/" + surveyId
headers = {
    "x-api-token": apiToken,
    }


###Mapping Live to API
response = requests.get(baseUrl, headers=headers)
data = response.json()

#
# ##Test Mapping Document Offline
# # with open(r'C:\Users\JefferyMcCain\Documents\Consulting\Athlete View\DataDumps\SurveyStructure.json') as f :
# #     data = json.load(f)

#######******Create the text file to write Mapping Document
runDate = datetime.utcnow().strftime('%Y.%m.%d.T.%H.%M.%S')
mapFileName = r'C:\Users\JefferyMcCain\Documents\Consulting\Athlete View\DataDumps\Textual Map\TextMap_' + runDate + \
              '.txt'
header = ['QuestionID', 'QuestionName', 'NumericAnswer', 'TextualAnswer']
writer = csv.writer(open(mapFileName, 'a', encoding='utf8'), delimiter="|")
writer.writerow(header)



questions = data['result']['questions']



for question in questions:
    qName = questions[question]['questionName']
    qDes = questions[question]['questionText']
    qType = questions[question]['questionType']

    if qType['selector'] == 'MAVR':
        choices = questions[question]['choices']

        for choice in choices:
            QID = str(question) + '_' + choice
            mappedValues = [QID, qName, 1, 'True']
            print(mappedValues)
            writer.writerow(mappedValues)
            mappedValues = [QID, qName, 0, 'False']
            print(mappedValues)
            QID = question
            writer.writerow(mappedValues)
    elif qType['selector'] == 'MACOL':
        choices = questions[question]['choices']
        for choice in choices:
            QID = str(question) + '_' + choice
            mappedValues = [QID, qName, 1, 'True']
            print(mappedValues)
            writer.writerow(mappedValues)
            mappedValues = [QID, qName, 0, 'False']
            print(mappedValues)
            QID = question
            writer.writerow(mappedValues)
    elif  qType['selector'] == 'NPS':
        choices = questions[question]['choices']
        for choice in choices:
            QID = question
            npsValue = int(choice)
            if npsValue >= 0 and npsValue <= 6:
                npsScore = "Detractor"
            elif npsValue >= 7 and npsValue <= 8:
                npsScore = "Passive"
            elif npsValue >= 9 and npsValue <= 10:
                npsScore = "Promoter"
            mappedValues = [QID, qName, choice, npsScore]
            print(mappedValues)
            writer.writerow(mappedValues)
            QID = question
    elif qType['selector'] == "Likert":
        choices = questions[question]['choices']
        for choice in choices:
            choiceNum = choices[choice]['recode']
            choiceText = choices[choice]['choiceText']
            mappedValues = [question, qName, choiceNum, choiceText]
            print(mappedValues)
            writer.writerow(mappedValues)
    elif qType['selector'] == "DL":
        choices = questions[question]['choices']
        for choice in choices:
            choiceNum = choices[choice]['recode']
            choiceText = choices[choice]['choiceText']
            mappedValues = [question, qName, choiceNum, choiceText]
            print(mappedValues)
            writer.writerow(mappedValues)
    elif qType['selector'] == "SAVR":
        choices = questions[question]['choices']
        for choice in choices:
            choiceNum = choices[choice]['recode']
            choiceText = choices[choice]['choiceText']
            mappedValues = [question, qName, choiceNum, choiceText]
            print(mappedValues)
            writer.writerow(mappedValues)
