import re
import random

library = open(r"./articles.txt","r",encoding='utf-8').read()
lines = open(r"./words.txt","r",encoding='utf-8').readlines()
questionfile = open(r"./questions.txt","r+",encoding='utf-8')
answerlist = []


for eachline in lines:
    eachline = "".join(eachline.splitlines(False))
    selflist = []
    while True:
        if eachline.find(',') != -1:
            selflist.append(eachline[:eachline.find(',')])
            eachline =eachline[eachline.find(',') + 1:]
        else:
            selflist.append(eachline)
            break
        
    sentences = re.findall("[A-Z]{1}[^.]*.",library)  #分析所有语句
    for i in selflist:
        for sentence in sentences:
            while True:
                qword = "".join(random.sample(selflist,1))
                question = re.sub("\w*"+i+"\w*","_____("+qword+")",sentence)
                answer = "".join(re.findall("\w*"+i+"\w*",sentence))
                if qword != answer:
                    break
            if question != sentence and answer not in answerlist:
                    print(question,"\n答案:"+answer)
                    questionfile.write(question+"\n答案:"+answer+"\n")
                    answerlist.append(answer)     #避免出答案相同的题目

