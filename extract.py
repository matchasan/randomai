# -coding by utf-8 -
from bs4 import BeautifulSoup
import csv
import re

def unifyString(row):
    if row[0]=="MST":
        row[0]="MASTER"
    elif row[0]=="Re:M":
        row[0]="Re:MASTER"

    if row[1]=="舞":
        row[1]="maimai"
    elif row[1]=="ゲ&バ":
        row[1]="ゲーム&バラエティ"
    elif row[1]=="nico":
        row[1]="ニコニコ&ボーカロイド"
    elif row[1]=="撃&チ":
        row[1]="オンゲキ&CHUNITHM"
    elif row[1]=="東方":
        row[1]="東方Project"
    
    if "でらっくす" in row[-1]:
        row[-1] = row[-1].replace("でらっくす","dx")
    else:
        row[-1] = row[-1].lower()
    return row

path = './maimai_constant.html'
with open(path, "rb") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

tables = soup.findAll("tbody")[1:] #難易度ごと

#ファイル書き込み準備
csvfile = open("table.csv", "w", newline="", encoding='utf-8')
writer = csv.writer(csvfile)
header = ["level","genre","name","composer","bpm","notes","version","difficulty"]
writer.writerow(header)

for table in tables:
    # table = tables[1] #15

    rows = table.findAll("tr") #表

    # csvfile = open("table.csv", "w", newline="", encoding='utf-8')
    # writer = csv.writer(csvfile)
    # header = ["level","genre","name","composer","bpm","notes","version","difficulty"]
    # writer.writerow(header)

    difficult = ""
    genre = ""
    setDG = 0
    setLevel = 0
    check=0
    preRow = []
    for i, row in enumerate(rows):
        # if i>4:
        #     break
        csvRow = []
        if len(row)==5:
            csvRow.append(difficult)
            csvRow.append(genre)
        elif len(row)==6:
            check = 1
        elif len(row)==7:
            setDG = 1
        elif len(row)==1:
            setLevel = 1

        print(len(row))
        for j, cell in enumerate(row.findAll("td")):
            
            #cell = row.findAll("td", text=re.compile("mu__table--col1"))
            # dif = cell.find('mu__table--col1').string

            if cell.find('span') != None:
                # print("find span")
                s = cell.find('span').string
                print(s)
                #print(type(cell.find('span').string))
            elif cell.find('a') != None:
                # print("find span")
                s = cell.find('a').string
                print(s)
            else:
                s = cell.string
                print(s)
            #print(type(cell.string))

            if s == None:
                s = cell.text
            #s = s.encode('utf-8').decode('utf-8')
            if setLevel==1:
                print("setLevel")
                level=s
                break
            csvRow.append(s)
        if setDG==1:
            print("setDG")
            difficult = csvRow[0]
            genre = csvRow[1]
            setDG=0
        elif setLevel==1:
            setLevel=0
            continue
        elif check==1:
            createRow =[]
            d = row.find("td", class_="mu__table--col1") #レベルチェック
            g = row.find("td", class_="mu__table--col2") #ジャンルチェック
            # print(d)
            # print(g.find('span').string)
            if d==None:
                createRow.append(preRow[0])
            else:
                createRow.append(d.find('span').string)

            if g==None:
                createRow.append(preRow[1])
            else:
                createRow.append(g.find('span').string)

            for k in range(1,6):
                createRow.append(csvRow[k])
            check=0
            csvRow=createRow
            
        # if csvRow[0]=="MST":
        #     csvRow[0]=="MASTER"
        # elif csvRow[0]=="Re:M":
        #     csvRow[0]=="Re:MASTER"
        
        # if "でらっくす" in csvRow[-1]:
        #     csvRow[-1] = csvRow[-1].replace("でらっくす","dx")
        # else:
        #     csvRow[-1] = csvRow[-1].lower()
        csvRow = unifyString(csvRow)
        csvRow.append(level)
        writer.writerow(csvRow)
        preRow=csvRow