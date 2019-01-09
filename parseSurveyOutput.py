import csv
import json
from  datetime import datetime as dt

runDate = dt.utcnow().strftime('%Y.%m.%d.T.%H.%M.%S')
# jsonFileName = r'C:\Users\JefferyMcCain\Documents\Consulting\Athlete View\DataDumps\OutputFiles\surveyOutput_' + runDate
csvFileName = r'C:\Users\JefferyMcCain\Documents\Consulting\Athlete View\DataDumps\OutputFiles\SA Core Survey.csv'
outputPivotFile = r'C:\Users\JefferyMcCain\Documents\Consulting\Athlete View\DataDumps\OutputFiles\PivotedSurveyResults_' + runDate + ".txt"

# file = pd.read_csv(csvFileName, skiprows=range(1,3))
# pivot = file.pivot(index='ResponseID', columns='Q5', )
#
# csvFile = open(, 'r', encoding="utf8")
# jsonFile = open(jsonFileName, 'w')
# # reader = csv.DictReader(csvFile)
# # for row in reader:
# #     json.dump(row, jsonFile)
# #     jsonFile.write('\n')
# #
# # print(jsonFile)
#
#
#
# print(file.head(5))
# print(pivot)

writer=csv.writer(open(outputPivotFile,'a',encoding='utf8'),delimiter="|")
header = ['ResponseID', 'Question', 'Answer' ]
rowCount = 1
csvFile = open(csvFileName, 'r',encoding='utf8')

reader = csv.DictReader(csvFile)
print(reader.fieldnames)
writer.writerow(header)
for row in reader:
    responseId = row['ResponseID']
    rowCount = rowCount + 1
    for item in row:
        listOfItems =[rowCount,responseId, item, row[item]]
        if listOfItems[0] > 3:
            if listOfItems[3] != "":
                surveyResults = listOfItems[1:]
                print(listOfItems[1:])
                writer.writerow(surveyResults)





