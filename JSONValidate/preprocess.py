import json
import sys
import numpy as np
#Missing Indices: Document is missing some indices (index goes higher than number of sentences)
#Duplicate Indices: Document has duplicate indicies
#Wrong Indices: Document indices are random and not in order
def checkIndex(data):
    issues = []
    dupeExtract = 0
    docsExtract = []
    for document in data['documents']:
        count = -1
        numDupes = 0
        wrongIdx = 0
        inOrder = True
        missing = []
        dupes = []
        current =[]
        for sentence in document['text']:
            for phrase in sentence:
                index=phrase['index']
                #Index Order Check
                if index != count+1:
                    wrongIdx+=1
                #Index Duplicate Check
                if index in current:
                    numDupes+=1
                    if index not in dupes:
                        dupes.append(index)
                count+=1
                current.append(index)
        #Missing indices
        completeList = list(range(0,count+1))
        missing = np.setdiff1d(completeList,current,assume_unique=False)
        #Is in Order
        if len(missing) > numDupes:
            inOrder = False
        if 'extractive' in document:
            extractive = document['extractive']
            if extractive != 0:
                my_dict = {i:extractive.count(i) for i in extractive}
                for key in my_dict:
                    if my_dict[key]>1:
                        dupeExtract+=1
                        docsExtract.append({ 'id': document['id'], 'title': document['title']})
                        break

        if wrongIdx > 0 or numDupes > 0 or len(missing)>0 :
            issues.append({
                 'docID': document['id'],
                 'wrongIdx': wrongIdx,
                 'numDupes': numDupes,
                 'dupes': dupes,
                 'missing': missing,
                 'inOrder': inOrder
                })
    return issues, dupeExtract, docsExtract

#Load JSON
with open(sys.argv[1], 'r') as filename:
    data = json.load(filename)
    #Run Test
    results, dupeExtract, docsExtract = checkIndex(data)
    with open(sys.argv[2], "a") as f:
        print("File Name: ",sys.argv[1], file=f)
        print("",file=f)
        print("",file=f)

        for doc in results:
            print('ID: ', doc['docID'],file=f)
            print('    Is in Order: ', doc['inOrder'],file=f)
            print('    Duplicate Indices 수: ', doc['numDupes'],file=f)
            print('    Incorrect Indices 수: ', doc['wrongIdx'],file=f)
            print('',file=f)

            print('    Missing Indices: ', doc['missing'],file=f)
            print('    Duplicate Indices: ', doc['dupes'],file=f)

            print('', file=f)
        # print("Total Number of Problematic Documents", len(results),file=f)
        print("Documents with Duplicates", file=f)
        print("", file=f)
        for doc in docsExtract:
            print('ID: ', doc['id'], " Title: ", doc['title'], file=f)
        print('',file=f)
        print("Total Number of Extractive Dupes: ", dupeExtract,file=f)
        print("Total Number of Documents: ", len(data['documents']), file=f)
        print("────────────────────────────────────────────────────────────────────────────────────",file=f)
