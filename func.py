import random as rand
import re
import csv
import numpy as np
import pandas as pd

def randomWheel():
    texts = ['perfect',
             'great',
             'miss']
    index = rand.randint(0, len(texts)-1)
    text = texts[index]
    return text

ver_list =["maimai", "green", "green+", "orange", "orange+", "pink", "pink+", 
        "murasaki", "murasaki+", "milk", "milk+", "finale", "dx", "dx+", 
        "splash", "splash+", "universe", "universe+"]

errormessage = ["コマンドを識別できませんでした。\nmanualコマンドで確認して下さい。\n",
                "Error:バージョン表記が正しくありません。"]

#searchMusic()
def searchMusic(mode, q):
    pd.set_option('display.max_columns', 4)
    df = pd.read_csv('./table.csv')
    # music_df = pd.read_csv('./data/musiclist.csv')
    # print(music_df.head())

    if mode == "ver":
        if len(q)==1:
            #print(q[0])
            #df_s = df[(df["version"]==q)]
            if (q[0] in ver_list) == False:
                err = df[0:1]
                err.iat[0, 7] = 1
                return err
            else:
                df_s = df[(df["version"] == q[0])]
                index = rand.randint(0, len(df_s)-1)
                music = df_s[index:index+1]
                print(music)
                return music
        else:
            #index = rand.randint(0, len(df)-1)
            return df[0:1]
    elif mode == "dif":
        low = q[0]
        high = q[1]
        if q[0]>q[1]:
            high = q[0]
            low = q[1]
        if low<13.7:
            low=13.7
        if high>15.0:
            high=15.0
        
        df_s = df[(df["difficulty"] >= low) & (df["difficulty"] <= high)]
        index = rand.randint(0, len(df_s)-1)
        music = df_s[index:index+1]
        print(df_s)
        return music


def mannual():
    man = "./manual.txt"
    with open(man, "r", encoding="utf-8") as f:
        text = f.read()
    return text

def random(query):
    res = ["", ""]

    #バージョン検索
    if query[0].lower() in "version":
        q = query[1:]
        mode = "ver"
        return searchMusic(mode, q)

     #難易度検索
    else:
        mode = "dif"
        query = [float(x) for x in query]
        return searchMusic(mode, query)
    return res

#manual = ["manual", "man", "マニュアル", "まにゅある"]


spl = '\n| |\t'
manual_list = ["manual", "man"]
random_list = ["random", "rand"]
bon_list = ["bon"]
def makeres(music_info):
    head = ""
    
    level = f'レベル: {music_info.iat[0, 0]}\n'
    genre = f'ジャンル: {music_info.iat[0, 1]}\n'
    title = f'タイトル: {music_info.iat[0, 2]}\n'
    composer = f'コンポーザー: {music_info.iat[0, 3]}\n'
    bpm = f'BPM: {music_info.iat[0, 4]}\n'
    notes = f'ノーツ数: {music_info.iat[0, 5]}\n'
    version = f'バージョン: {music_info.iat[0, 6]}\n'
    difficulty = f'定数: {music_info.iat[0, 7]}\n'

    res = title + level + difficulty + version + composer + genre + bpm
    return res

def createResponse(text):
    target = re.split(spl, text.strip())
    command = target[0].lower()
    print(target)
    print(command)
    res = errormessage[0]
    # if re.search(r'[ぁ-ん]+|[ァ-ヴー]+', command): #日本語判定
    #     if command == "マニュアル":
    #         res = mannual()
    #     if command == "ランダム":
    #         res = random(target[1:])
    # else:
    if command in manual_list:
        res = mannual()
    elif command in random_list:
        music_info = random(target[1:])
        if music_info.iat[0, 7]==1:
            res = errormessage[1]
        else:
            res = makeres(music_info)
    elif command == "bon":
        res = ":parrot:"
    #elif command:
    
    return res

text = "rand ver murasaki+"
r = createResponse(text)
print(r)