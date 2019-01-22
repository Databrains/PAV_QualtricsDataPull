import csv
import json
from  datetime import datetime as dt
import pandas as pd


'''****************************************************
    Set Up CSV Files
****************************************************'''
runDate = dt.utcnow().strftime('%Y.%m.%d.T.%H.%M.%S')
# jsonFileName = r'C:\Users\JefferyMcCain\Documents\Consulting\Athlete View\DataDumps\OutputFiles\surveyOutput_' + runDate
csvFileName = r'C:\Users\JefferyMcCain\Documents\Consulting\Athlete View\DataDumps\OutputFiles\SA Core Survey.csv'
outputPivotFile = r'C:\Users\JefferyMcCain\Documents\Consulting\Athlete View\DataDumps\OutputFiles\PivotedSurveyResults_' + runDate + ".txt"
doNotPivotFile = r'C:\Users\JefferyMcCain\Documents\Consulting\Athlete View\DoNotPivotQuestions.csv'
embeddedDataFileName = r'C:\Users\JefferyMcCain\Documents\Consulting\Athlete View\DataDumps\OutputFiles\EmbeddedResults_' + runDate + ".txt"
csvFile = open(csvFileName, 'r',encoding='utf8')

'''***************************************************
     Set Up Pivoted Data File to be written
***************************************************'''
writer=csv.writer(open(outputPivotFile,'a',encoding='utf8'),delimiter="|")
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
pivotedReader = csv.DictReader(csvFile)
print(pivotedReader.fieldnames)
writer.writerow(header)
for row in pivotedReader:
    responseId = row['ResponseID']
    rowCount = rowCount + 1
    for item in row:
        listOfItems =[rowCount,responseId, item, row[item]]
        if listOfItems[0] > 3:
            if listOfItems[3] != "":
                surveyResults = listOfItems[1:]
                if surveyResults[1] not in doNotPivot:
                    print(listOfItems[1:])
                    writer.writerow(surveyResults)



'''**************************************************
        Write Embedded Data Output File
**************************************************'''
embeddedData = pd.read_csv(csvFileName, usecols=doNotPivot, skiprows=(1,2), dtype=object)
embeddedDataFile = pd.DataFrame.to_csv(embeddedData,embeddedDataFileName,sep="|", index=False)
print("Embedded Data File Complete")

print('Process Complete')






