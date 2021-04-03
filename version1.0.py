import re
import random
import tkinter as tk
from tkinter import Button, Checkbutton, IntVar, Label, Menu, Radiobutton, Tk, filedialog, messagebox,scrolledtext,INSERT,END
import os
from tkinter import *

class Mainwindow:
    #声明
    library = ''
    wordslist = []
    libsent = []
    questions = []
    sentences = []
    usedsentences = []
    grammars = ""

    grammv = 1
    fast = 1
    maxlen = 100

    #构造窗体
    def __init__(self):
        mainwindow = Tk()
        mainwindow.title("Forformer")
        mainwindow.geometry('1000x500')
        mainmenu = Menu(mainwindow)
        menuFile = Menu(mainmenu)
        self.txt = scrolledtext.ScrolledText(mainwindow, height=15,wrap=tk.WORD)
        self.txtword = scrolledtext.ScrolledText(mainwindow, width=20)
        self.grammar = scrolledtext.ScrolledText(mainwindow, width=20,wrap=tk.WORD)

        self.txt.pack(side='top', fill='x')
        self.txtword.pack(side='left', expand='no', fill='y')
        self.grammar.pack(side='left', expand='no',fill='y')
        btg = Button(mainwindow, text="生成", command=self.process,width=10,height=3)
        btg.pack(side='right', expand='no',anchor='se')
        Radiobutton(mainwindow,text="快速索引",variable=self.fast,value =1).pack(side='left',anchor='ne')
        Radiobutton(mainwindow,text="包含索引",variable=self.fast,value =0).pack(side='left',anchor='ne')

        self.grammar.insert(INSERT,"to #\nto be #\nhave #")
        self.txtword.insert(INSERT,"exampleA0,exampleA1\nexampleB0,exampleB1")
        mainmenu.add_cascade(label="文件",menu=menuFile)
        menuFile.add_command(label="导入语料库",command=self.importlibrary)
        menuFile.add_command(label="导入单词",command=self.importwords)
        menuFile.add_command(label="导出题库",command=self.exportquestion)
        mainwindow.config(menu=mainmenu)
        mainwindow.bind('Button-3',self.popupmenu)
        mainwindow.mainloop()
        sency = []

 

    #构造方法


    #导入
    def importlibrary(self):
        filepath = "".join(filedialog.askopenfilenames(initialdir=os.path.dirname(__file__)))
        self.library = open(filepath,"r",encoding='utf-8-sig').read()
        self.library = self.library.replace("\n","")
        self.sentences = re.findall("[A-Z]{1}[^.]*.",self.library)
        return (len(self.sentences))
    
    def importwords(self):
        self.txtword.delete(0.0,END)
        filepath = "".join(filedialog.askopenfilenames(initialdir=os.path.dirname(__file__)))
        wordslist0 = open(filepath,"r",encoding='utf-8-sig').readlines()
        for i in wordslist0:
            self.wordslist.append(i.replace('\n',''))
            self.txtword.insert(INSERT,i)
        return (len(self.wordslist))

    def readwords(self):
        wordslist00 = []
        wordslist = self.txtword.get(1.0,END)
        while True:
            if wordslist.find('\n') != -1:
                wordslist00.append(wordslist[:wordslist.find('\n')])
                wordslist00 =wordslist[wordslist.find('\n') + 1:]
            else:
                wordslist00.append(wordslist)
        for i in wordslist00:
            self.wordslist.append(i.replace('\n',''))

    
    def exportquestion(self):
        txt = self.txt.get('1.0','end')
        print(txt)
        file0 = filedialog.askopenfilenames(initialdir=os.path.dirname(__file__))
        questionfile = open("".join(file0),"r+",encoding='utf-8')
        questionfile.write(txt)
        questionfile.close

    def fastchangeto(self,sentence,wordlist,maxlen,targetqword=None):
        selflist = []
        if len(sentence) <= self.maxlen:
            while True:
                if wordlist.find(',') != -1:
                    selflist.append(wordlist[:wordlist.find(',')])
                    wordlist =wordlist[wordlist.find(',') + 1:]
                else:
                    selflist.append(wordlist)
                    break
            
            for word in selflist:
                if word in sentence and sentence not in self.usedsentences:
                    qword = "".join(random.sample(selflist,1))
                    if targetqword == None:
                        question = re.sub("\w*"+word+"\w*","_____("+qword+")",sentence)
                    else:
                        question = re.sub("\w*"+word+"\w*","_____("+targetqword+")",sentence)

                    answer = "".join(re.findall("\w*"+word+"\w*",sentence))
                    self.questions.append(question+"\n答案:"+answer+"\n\n")
                    self.usedsentences.append(sentence)
                    break

    def chuti(self,sentence,word,maxlen,targetword):
        if len(sentence) <= self.maxlen and word in sentence and sentence not in self.usedsentences:
            question = re.sub("\w*"+word+"\w*","_____("+targetword+")",sentence)
            answer = "".join(re.findall("\w*"+word+"\w*",sentence))
            self.questions.append(question+"\n答案:"+answer+"\n\n")
            self.usedsentences.append(sentence)

    def changeto(self,sentence,wordlist,grammars):
        if len(sentence) <= self.maxlen:
            selflist = []
            prelist = []
            allmakeup = []
            grammars = self.grammars
            while True:
                if wordlist.find(',') != -1:
                    selflist.append(wordlist[:wordlist.find(',')])
                    wordlist =wordlist[wordlist.find(',') + 1:]
                else:
                    selflist.append(wordlist)
                    break
            while True:

                if grammars.find('\n') != -1:
                    prelist.append(grammars[:grammars.find('\n')])
                    grammars =grammars[grammars.find('\n') + 1:]
                else:
                    prelist.append(grammars)
                    break
            while '' in prelist:
                prelist.remove('')
            for word in selflist:
                for preposition in prelist:

                    pre = preposition.replace('#',word)
                    if pre in sentence and sentence not in self.usedsentences:
                        question = re.sub("\w*"+pre+"\w*","_____("+selflist[0]+")",sentence)
                        answer = "".join(re.findall("\w*"+pre+"\w*",sentence))
                        self.questions.append(question+"\n答案:"+answer+"\n\n")
                        self.usedsentences.append(sentence)
            for word in selflist:
                if word in sentence:
                    selflist0 = selflist.copy()
                    selflist0.remove(word)
                    self.chuti(sentence,word,self.maxlen,"".join(random.sample(selflist0,1)))

    def process(self):
        self.grammars = self.grammar.get('1.0','end')
        print(self.grammars)

        listsc =[]
        fastsentences = []
        if  self.library == '':
            messagebox.showwarning('生成失败','你的句库是不是还没导入？')
        elif self.wordslist == []:
            messagebox.showwarning('生成失败','你的词库是不是还没导入？')
        else:
            if self.fast == 0:
                for sentence in self.sentences:
                    for wordlist in self.wordslist:
                        if self.grammv == 1:
                            self.changeto(sentence,wordlist,self.grammars)
                        if self.grammv == 0:
                            self.fastchangeto(sentence,wordlist,self.maxlen)
            if self.fast == 1:
                for wordlist in self.wordslist:
                    selflist =[]
                    while True:
                        if wordlist.find(',') != -1:
                            selflist.append(wordlist[:wordlist.find(',')])
                            wordlist =wordlist[wordlist.find(',') + 1:]
                        else:
                            selflist.append(wordlist)
                            break
                    for word in selflist:
                        wordpace = " "+word+" "
                        fastsentences.extend(re.findall("[A-Z]{1}[^.]*"+wordpace+"[^.]*.",self.library))
                for sentence in fastsentences:
                    for wordlist in self.wordslist:
                        if self.grammv == 1:
                                self.changeto(sentence,wordlist,self.grammars)
                        if self.grammv == 0:
                                self.fastchangeto(sentence,wordlist,self.maxlen)
        formatList = list(set(self.questions))
        for question in formatList:
            self.txt.insert(INSERT,question)

                        

            


    def popupmenu(self,event):
        self.mainmenu.post(event.x_root,event.y_root)





if __name__ == "__main__":
    Mainwindow()



