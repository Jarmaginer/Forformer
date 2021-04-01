import re
import random
import tkinter.ttk
import tkinter
from tkinter import filedialog,scrolledtext, messagebox
from tkinter import *
import os


answerlist = []
n = 1


window = Tk()
window.title("Forformer")
window.geometry('1000x700')
library = None
lines = None
questionfile = None
mainmenu = Menu(window)
menuFile = Menu(mainmenu)

def main():
    return None

def exportquestion():
    global questionfile
    global txt
    txtline = txt.get('1.0','end').replace('\n','')
    print(txtline)
    file0 = filedialog.askopenfilenames(initialdir=os.path.dirname(__file__))
    questionfile = open("".join(file0),"r+",encoding='utf-8')
    questionfile.write(txtline)
    questionfile.close

def fastsearchX():
    global library
    fastsearch(library)


def fastsearch(library):
    wordslist = []
    for eachline in lines:
        while True:
                if eachline.find(',') != -1:
                    wordslist.append(eachline[:eachline.find(',')].replace('\n',''))
                    eachline =eachline[eachline.find(',') + 1:]
                else:
                    wordslist.append(eachline.replace('\n',''))
                    break
    print(wordslist)


def library():
    global library
    file0 = filedialog.askopenfilenames(initialdir=os.path.dirname(__file__))
    file1 = "".join(file0)
    library = open(file1,"r",encoding='utf-8').read()

def words():
    global lines
    lines = filedialog.askopenfilenames(initialdir=os.path.dirname(__file__))
    lines1 = "".join(lines)
    lines = open(lines1,"r",encoding='utf-8').readlines()
    for line in lines:
        bringline ="".join(line)
        txtworld.insert(INSERT, bringline)


def getwordsfromtext():
    newlines = txtworld.get()

# def fastsearch(library):
#     for eachline in lines:


def printquestion(lines,library):
        global n
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
            try:
                sentences = re.findall("[A-Z]{1}[^.]*.",library)  #分析所有语句
            except:
                messagebox.showwarning('生成失败','句库发生错误')
            for i in selflist:
                for sentence in sentences:
                    while True:
                        qword = "".join(random.sample(selflist,1))
                        question = re.sub("\w*"+i+"\w*","_____("+qword+")",sentence)
                        answer = "".join(re.findall("\w*"+i+"\w*",sentence))
                        if qword != answer:
                            break
                    if question != sentence and answer not in answerlist:
    #                        print(question,"\n答案:"+answer)
    #                        questionfile.write(question+"\n答案:"+answer+"\n")
                            answerlist.append(answer)     #避免出答案相同的题目
                            bringquestion = question+"\n"
                            bringanswer = answer+"\n"
                            print (question,answer)
                            txt.insert(INSERT, str(n)+". "+bringquestion+"答案:"+bringanswer+"\n")
                            n+=1

def popupmenu(event):
     mainmenu.post(event.x_root,event.y_root)


def process():
    global library
    global lines
    global n
    if library == None:
        messagebox.showwarning('生成失败','你的句库是不是还没导入？')
    elif lines == None:
        messagebox.showwarning('生成失败','你的词库是不是还没导入？')
    else:
        printquestion(lines,library)
        if n != 1:
            messagebox.showinfo("生成完毕","共生成"+str(n)+"个题目")
        else:
            messagebox.showwarning("生成失败","未找到匹配项")



txt = scrolledtext.ScrolledText(window, width=80, height=50)
txt.place(x=20,y=20)

txtworld = scrolledtext.ScrolledText(window, width=40, height=50)
txtworld.place(x=700,y=20)

btn = Button(window, text="debug", command=fastsearchX)
btn.place(x=600,y=70)

btn = Button(window, text="导入句库", command=library)
btn.place(x=600,y=20)

btg = Button(window, text="生成", command=process)
btg.place(x=600,y=630)

btg = Button(window, text="导入词库", command=words)
btg.place(x=600,y=50)

mainmenu.add_cascade(label="文件",menu=menuFile)
menuFile.add_command(label="导入语料库",command=library)
menuFile.add_command(label="导入单词",command=words)
menuFile.add_command(label="导出题目",command=words)

window.config(menu=mainmenu)
window.bind('Button-3',popupmenu)
window.mainloop()

if __name__ == "__main__":
    main()
