import pandas as pd
import csv
from datetime import datetime as dt

header=['QID', 'Numeric Answer','Question Description']
numberMap = pd.read_csv(r'C:\Users\JefferyMcCain\Downloads\v3.12.9.18output.txt', delimiter="|")
# writer=csv.writer(open(r'C:\Users\JefferyMcCain\Downloads\NumberMapPy.txt','a',encoding='utf8'),delimiter="|", )
# df = pd.DataFrame(columns=['QID', 'Numeric Answer'],index=None)
qidMapFrame = pd.DataFrame(columns=["QID", 'Q', 'Question Description'], index=None)

#textMap = pd.read_csv(r'C:\Users\JefferyMcCain\Downloads\textMap.txt', delimiter="|")
# writer=csv.writer(open(r'C:\Users\JefferyMcCain\Downloads\TextMapPy.txt','a',encoding='utf8'),delimiter="|")

#Mapping for QID and Q

utctime = dt.utcnow().strftime('%d-%m.-%y %H.%M.%S')

writer=csv.writer(open(r'C:\Users\JefferyMcCain\Downloads\QDesMap' + str(utctime) + 'UTC.txt','a',encoding='utf8'),delimiter="|", )


##select single QID Number
# col = numberMap['Q450_Q450_11']
# uniqueItems = col.unique()
# print(uniqueItems)
# firstItem = uniqueItems[1]
# print(firstItem)
# QID =  firstItem.split(":", 1)[1][:-1]
# print(QID)
# print(uniqueItems[0])
#
# # print(firstItem['ImportedId'])
# firstItemQ = firstItem.split("-", 1)[0]
# firstItemDes = firstItem.split("-", 1)[1]

#print(uniqueItems)
# print(firstItemQ)
###***Get List of
for column in numberMap.columns:
    if  "Q" in column and "embedded" not in column:
        uniqueItems = numberMap[column].unique()
        questionDescription = uniqueItems[0].replace('"','')
        if "-" in questionDescription:
            finalQ = questionDescription
            questionDescription2 = questionDescription.split("-",6)
            print("***Question Length***" + str(len(questionDescription2)))
            print('Original Question: ' + questionDescription)
            # print('Question Split: ' + str(questionDescription2))
            
            questionDescription3 = questionDescription2[-1]
            if questionDescription3.strip() == 'Group' or questionDescription3 == "Text"\
                    :
                finalQ = questionDescription2
            elif "On a scale from" in questionDescription:
                finalQ = questionDescription
            elif "Please" in questionDescription and "-" in questionDescription \
                    and "non-athle" not in questionDescription:
                pleaseq = questionDescription.split('-', 1)
                finalQ = pleaseq[-1]
            else:
                finalQ = questionDescription3
        else: finalQ = questionDescription
        firstItem = uniqueItems[1]
        QID = firstItem.split(":", 1)[1][:-1]
        QID1 = QID.replace("'","")
        if len(finalQ) > 75:
            finalQ = finalQ[:75] + '...'
        else:
            finalQ = finalQ
        QIDparse = QID1.strip()
        if QIDparse[:4] == QIDparse[5:]:
            QIDfinal = (QIDparse[5:])
        else:
            QIDfinal = QIDparse
        if QIDfinal == "QID218":
            QIDfinal = "QID_218_NPS_GROUP"
        outputList = [QIDfinal, column, finalQ]
        print(outputList)

        writer.writerow(outputList)

# get all of the columns print their headers and ID value
# for col in numberMap.columns:
#     uniqueValues = numberMap[col].unique()
#     firstItem = uniqueValues[0]
#     if len(firstItem.split("-", 1)) == 2:
#         firstItemQ = firstItem.split("-", 1)[0]
#         firstItemDes = firstItem.split("-", 1)[1]
#         dict = [col, firstItemQ, firstItemDes]
#     elif len(firstItem.split("-", 1)) == 1:
#         firstItemQ = firstItem.split("-", 1)[0]
#         firstItemDes = firstItemQ
#         dict = [col, firstItemQ, firstItemDes]
#     print(dict)
#     writer.writerow(dict)
#     qidMapFrame.append(dict, ignore_index=True)
