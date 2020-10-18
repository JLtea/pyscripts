import pandas as pd
import json
import sys
# from pandas.io.json import json_normalize
import xlsxwriter

with open(sys.argv[1], 'r') as filename:
    data = json.load(filename)
    # print(type(filename))
    workbook = xlsxwriter.Workbook(sys.argv[1][:-5]+'.xlsx',{'strings_to_formulas': False})
    worksheet = workbook.add_worksheet()

    worksheet.write(0,0,'기사번호')
    worksheet.write(0,1,'기사카테고리')
    worksheet.write(0,2,'매체유형')
    worksheet.write(0,3,'매체구분')
    worksheet.write(0,4,'매체명')
    worksheet.write(0,5,'기사대중소')
    worksheet.write(0,6,'기사본문글자수')
    worksheet.write(0,7,'발행일시')
    worksheet.write(0,8,'제목')
    worksheet.write(0,9,'내용')
    worksheet.write(0,10,'가독성')
    worksheet.write(0,11,'정확성')
    worksheet.write(0,12,'정보성')
    worksheet.write(0,13,'신뢰성')
    worksheet.write(0,14,'생성')
    worksheet.write(0,15,'추출1')
    worksheet.write(0,16,'추출2')
    worksheet.write(0,17,'추출3')

    row = 1
    col = 0
    for doc in data['documents']:
        paragraph = ''
        extractiveIdx = doc['extractive']
        extractive = []
        for text in doc['text']:
            if paragraph:
                paragraph +='\n'
            for sentence in text:
                if sentence['index'] in extractiveIdx:
                    extractive.append(sentence['sentence'])
                if paragraph:
                    paragraph +='\n'
                paragraph += sentence['sentence']


        scores = doc['document_quality_scores']
        abstractive=''
        for abstract in doc['abstractive']:
            if abstractive:
                abstractive += '\n'
            abstractive += abstract

        worksheet.write(row,0,doc['id'])
        worksheet.write(row,1,doc['category'])
        worksheet.write(row,2,doc['media_type'])
        worksheet.write(row,3,doc['media_sub_type'])
        worksheet.write(row,4,doc['media_name'])
        worksheet.write(row,5,doc['size'])
        worksheet.write(row,6,doc['char_count'])
        worksheet.write(row,7,doc['publish_date'])
        worksheet.write(row,8,doc['title'])
        worksheet.write(row,9,paragraph)
        worksheet.write(row,10,scores['readable'])
        worksheet.write(row,11,scores['accurate'])
        worksheet.write(row,12,scores['informative'])
        worksheet.write(row,13,scores['trustworthy'])
        worksheet.write(row,14,abstractive)
        for i in range(0,len(extractive)):
            worksheet.write(row,15+i,extractive[i])

        row+=1

    workbook.close()