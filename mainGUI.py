import re
import random
from tkinter import Button, Checkbutton, IntVar, Label, Menu, Radiobutton, Tk, DISABLED,filedialog, messagebox,scrolledtext,INSERT,END,IntVar,Scale,HORIZONTAL,LabelFrame,WORD,NORMAL
import os
import threading

class Mainwindow:
    #声明
    library = ''
    wordslist = []
    libsent = []
    questions = []
    sentences = []
    usedsentences = []
    grammars = ""
    questionsnoa = []
    saved = None

    #构造窗体
    def __init__(self):
        mainwindow = Tk()
        mainwindow.title("Forformer")
        mainwindow.geometry('1000x618')
        mainmenu = Menu(mainwindow)
        menuFile = Menu(mainmenu)
        menuFile0 = Menu(mainmenu)
        self.fast = IntVar()
        self.txt = scrolledtext.ScrolledText(mainwindow, height=15,wrap=WORD)
        self.txtword = scrolledtext.ScrolledText(mainwindow, width=20)
        self.grammar = scrolledtext.ScrolledText(mainwindow, width=20,wrap=WORD)
        self.fast.set(1)
        self.txt.pack(side='top', fill='x')
        self.txtword.pack(side='left', expand='no', fill='y')
        self.grammar.pack(side='left', expand='no',fill='y')
        self.btg = Button(mainwindow, text="生成", command=lambda :self.thread_it(self.process),width=10,height=3)
#        self.btg = Button(mainwindow, text="生成", command=self.process,width=10,height=3)   #禁用多线程
        self.btg.pack(side='right', expand='no',anchor='se')

        group0 = LabelFrame(mainwindow, text="单句匹配字数上限")
        group0.pack(anchor='nw')
        self.maxlen = Scale(group0, orient=HORIZONTAL, showvalue=1,from_=10,to=1000)
        self.maxlen['length'] = 7000
        self.maxlen.set(800)
        self.maxlen.pack()
        group = LabelFrame(mainwindow, text="索引方式")
        group.pack(anchor='nw')
        Radiobutton(group,text="快速索引",variable=self.fast,value =1,command=self.checkbottom).pack(side='top',anchor='n')
        Radiobutton(group,text="包含索引",variable=self.fast,value =0,command=self.checkbottom).pack(side='bottom',anchor='s')
        self.grammv = IntVar()
        self.grammvall = IntVar()
        c = Checkbutton(mainwindow, text="启用语法匹配", variable=self.grammv,command=self.checkbottom)
        c.pack(anchor="nw")
        c.select()
        self.b = Checkbutton(mainwindow, text="语法内匹配所有单词", variable=self.grammvall,state=DISABLED)
        self.b.pack(anchor="nw")
        self.btgg = Button(mainwindow, text="清库", command=self.clear,width=4,height=1)
        self.btgg.pack(side='left', expand='no',anchor='ne')        

        self.grammar.insert(INSERT,"to #\nto be #\nhave #")
        self.txtword.insert(INSERT,"exampleA0,exampleA1\nexampleB0,exampleB1")
        mainmenu.add_cascade(label="导入",menu=menuFile)
        menuFile.add_command(label="导入语料库",command=self.importlibrary)
        menuFile.add_command(label="导入单词",command=self.importwords)
        mainmenu.add_cascade(label="导出",menu=menuFile0)
        menuFile0.add_command(label="导出题库",command=self.exportquestion)
        menuFile0.add_command(label="导出试卷",command=self.exportquestionnoa)
        mainwindow.config(menu=mainmenu)
        mainwindow.bind('Button-3',self.popupmenu)
        mainwindow.protocol('WM_DELETE_WINDOW',self.on_closing)
        
        mainwindow.mainloop()
        sency = []



 

    #构造方法


    #导入
    def importlibrary(self):
        try:
            filepath = "".join(filedialog.askopenfilenames(initialdir=os.path.dirname(__file__)))
            self.library = open(filepath,"r",encoding='utf-8-sig').read()
        except:
            messagebox.showwarning("导入失败","导入出错啦,请确保文件编码为UTF-8")
        self.library = self.library.replace("\n","")
        self.sentences = re.findall("[A-Z]{1}[^.]*.",self.library)
        return (len(self.sentences))
    
    def importwords(self):
        try:
            filepath = "".join(filedialog.askopenfilenames(initialdir=os.path.dirname(__file__)))
            wordslist0 = open(filepath,"r",encoding='utf-8-sig').readlines()
        except:
            messagebox.showwarning("导入失败","导入出错啦,请确保文件编码为UTF-8")
        self.txtword.delete(0.0,END)
        for i in wordslist0:
            self.wordslist.append(i.replace('\n',''))
            self.txtword.insert(INSERT,i)
        
        return (len(self.wordslist))

    def readwords(self):
        self.wordslist.clear()
        wordslist00 = []
        wordslist = self.txtword.get(0.0,END)
        while True:
            if wordslist.find('\n') != -1:
                wordslist00.append(wordslist[:wordslist.find('\n')])
                wordslist =wordslist[wordslist.find('\n') + 1:]
            else:
                wordslist00.append(wordslist)
                break
        self.wordslist.clear()
        for i in wordslist00:
            if i != '':
                self.wordslist.append(i.replace('\n',''))

    
    def exportquestion(self):
        txt = self.txt.get('1.0','end')
        file0 = filedialog.askopenfilenames(initialdir=os.path.dirname(__file__))
        questionfile = open("".join(file0),"r+",encoding='utf-8')
        questionfile.write(txt)
        questionfile.close
        self.saved = True

    def exportquestionnoa(self):
        file0 = filedialog.askopenfilenames(initialdir=os.path.dirname(__file__))
        questionfile = open("".join(file0),"r+",encoding='utf-8')
        n = 1
        for i in self.questionsnoa:
            questionfile.write(str(n)+". "+i)
            n += 1
        questionfile.close
        self.saved = True

    def fastchangeto(self,sentence,wordlist,maxlen,targetqword=None):
        selflist = []
        wordA = "&"
        if len(sentence) <= self.maxlen.get():
            while True:
                if wordlist.find(',') != -1:
                    selflist.append(wordlist[:wordlist.find(',')])
                    wordlist =wordlist[wordlist.find(',') + 1:]
                else:
                    selflist.append(wordlist)
                    break
            
            for word in selflist:
                if self.fast.get() == 1:
                    wordA = " "+word+" "
                if wordA in sentence and sentence not in self.usedsentences:
                    selflist.remove(word)
                    qword = "".join(random.sample(selflist,1))
                    if targetqword == None:
                        question = re.sub("\w*"+word+"\w*","_____("+qword+")",sentence)
                    else:
                        question = re.sub("\w*"+word+"\w*","_____("+targetqword+")",sentence)

                    answer = "".join(re.findall("\w*"+word+"\w*",sentence))
                    self.questions.append(question+"\n答案:"+answer+"\n\n")
                    self.questionsnoa.append(question+"\n\n")
                    self.usedsentences.append(sentence)
                    break
                elif word in sentence and sentence not in self.usedsentences:

                    qword = "".join(word)
                    if targetqword == None:
                        question = re.sub("\w*"+word+"\w*","_____("+qword+")",sentence)
                    else:
                        question = re.sub("\w*"+word+"\w*","_____("+targetqword+")",sentence)

                    answer = "".join(re.findall("\w*"+word+"\w*",sentence))
                    self.questions.append(question+"\n答案:"+answer+"\n\n")
                    self.questionsnoa.append(question+"\n\n")
                    self.usedsentences.append(sentence)
                    break


    def chuti(self,sentence,word,maxlen,targetword):
        if len(sentence) <= self.maxlen.get() and word in sentence and sentence not in self.usedsentences:
            question = re.sub("\w*"+word+"\w*","_____("+targetword+")",sentence)
            answer = "".join(re.findall("\w*"+word+"\w*",sentence))
            self.questions.append(question+"\n答案:"+answer+"\n\n")
            self.questionsnoa.append(question+"\n\n")
            self.usedsentences.append(sentence)

    def changeto(self,sentence,wordlist,grammars):
        if len(sentence) <= self.maxlen.get():
            selflist = []
            prelist = []
            allmakeup = []
            grammars = self.grammars
            press = []
            presss = []
            targetword = None
            
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
            if self.grammvall.get() == 1:
                for preposition in prelist:
                    preab = preposition.replace(r'#',r"\w*")
                    answers = "".join(re.findall(preab,sentence))
                    if answers != '':

                        answerlist = answers.split(' ')
                        prelist0 = preposition.split(' ')
                        for i in answerlist:
                            if i not in prelist0:
                                qword = i
                                break
                        try:
                            if sentence not in self.usedsentences:
                                question = re.sub("\w*"+answers+"\w*","_____("+qword+")",sentence)
                                answer = answers
                                self.questions.append(question+"\n答案:"+answer+"\n\n")
                                self.questionsnoa.append(question+"\n\n")
                                self.usedsentences.append(sentence)
                        except:
                            continue                            
    
            else:
                for word in selflist:
                    for preposition in prelist:
                        pre = preposition.replace('#',word)
                        if pre in sentence and sentence not in self.usedsentences:
                            question = re.sub("\w*"+pre+"\w*","_____("+selflist[0]+")",sentence)
                            answer = "".join(re.findall("\w*"+pre+"\w*",sentence))
                            self.questions.append(question+"\n答案:"+answer+"\n\n")
                            self.questionsnoa.append(question+"\n\n")
                            self.usedsentences.append(sentence)              
                for word in selflist:
                        if word in sentence:
                            selflist0 = selflist.copy()
                            selflist0.remove(word)
                            if " "+word+" " in sentence:
                                self.chuti(sentence,word,self.maxlen.get(),"".join(random.sample(selflist0,1)))
                            elif word in sentence:
                                self.chuti(sentence,word,self.maxlen.get(),word)


    def process(self):
        print(self.grammv.get(),self.grammvall.get())
        self.grammars = self.grammar.get('1.0','end')
        print(self.grammars)
        self.readwords()
        print(self.wordslist)
        listsc =[]
        fastsentences = []
        if  self.library == '':
            messagebox.showwarning('生成失败','语料库未导入')
        elif self.wordslist == []:
            messagebox.showwarning('生成失败','词库为空')
        else:
            self.btg.config(state=DISABLED,text = "生成中")
            if self.fast.get() == 0:
                for sentence in self.sentences:
                    for wordlist in self.wordslist:
                        if self.grammv.get() == 1:
                            self.changeto(sentence,wordlist,self.grammars)
                        if self.grammv.get() == 0:
                            self.fastchangeto(sentence,wordlist,self.maxlen.get())
            if self.fast.get() == 1:
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
                        if self.grammv.get() == 1:
                                self.changeto(sentence,wordlist,self.grammars)
                        if self.grammv.get() == 0:
                                self.fastchangeto(sentence,wordlist,self.maxlen.get())
        formatList = list(set(self.questions))
        for question in formatList:
            self.txt.insert(INSERT,question)
            self.questions.clear()
        print("#本次操作共生成"+str(len(formatList))+"个题目#")
        self.btg.config(state=NORMAL,text ="生成")

    def on_closing(self):
        if self.saved or self.txt.get(2.0,END) == '':
            exit()
        else:
            if messagebox.askokcancel("退出", "题库未保存，您真的要退出吗？"):
                exit()

    def checkbottom(self):
        if self.grammv.get() == 1 and self.fast.get() == 0:
            self.b.config(state = NORMAL)
        else:
            self.b.deselect()
            self.b.config(state = DISABLED)

    def clear(self):
        if messagebox.askokcancel("清库", "您真的要清库吗？此操作不可逆"):
            self.txt.delete(0.0,END)
            self.questions.clear()
            self.usedsentences.clear()
            self.questionsnoa.clear()

    def thread_it(self,func, *args):
        t = threading.Thread(target=func, args=args) 
        t.start()

    
    def popupmenu(self,event):
        self.mainmenu.post(event.x_root,event.y_root)





if __name__ == "__main__":
    Mainwindow()



