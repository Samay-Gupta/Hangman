from tkinter import *
from Categories import *
from random import choice as rnd
from time import time

class Hangman:

    def __init__(self, easy_mode=True):
        self.size = (1240, 720)
        self.easy_mode = easy_mode
        self.used_base = [' ', ',', '.', '?', '/', '\\', '(', ')', '{', '}', '[', ']', ':', ';', '<', '>', '!', '#', '@', '$', '%', '^', '&', '*', '~', '`', '|', 'I', 'V', 'L', 'X', 'C']
        self.stop = False
        if easy_mode:
            self.used_base.extend(list('0123456789aeiou'))
        self.window = Tk()
        self.window.title('Hangman')
        self.window.configure(bg='white')
        self.window.grid_columnconfigure(1, minsize=540)
        self.canvasframe = Frame(self.window)
        self.canvasframe.grid(row=0, column=0, rowspan=18)
        self.categories = categories
        self.chosen = False
        self.category = ''
        self.entry_box = ''
        for each in self.categories:
            var_name = 'self.'+each
            exec(var_name + '=' + str(eval(each)))
        self.figure = ['rope', 'head', 'body', 'hand1', 'hand2', 'leg1', 'leg2']
        if not(easy_mode):
            del self.figure[0]
        self.total_lives = len(self.figure)
        self.widget_data = []
        self.used = []
        self.base()
        self.main_screen()
        self.window.update()
        

    def main_screen(self):
        self.clear_screen()
        self.widget_data = []
        lbl = Label(self.window, font=('Helvetica', 45, "bold"), text="HANGMAN", bg='white')
        lbl.grid(row=0, column=1, rowspan=2)
        self.widget_data.append(lbl)
        lbl = Label(self.window, font=('Helvetica', 30, "bold"), text="Categories: ", bg='white')
        lbl.grid(row=2, column=1)
        self.widget_data.append(lbl)
        for i in range(len(self.categories)):
            category = self.categories[i]
            text = '{}) {}'.format(i+1, category.capitalize())
            cmd = lambda category=category : self.get_category(category)
            btn = Button(self.window, font=('Helvetica', 25, 'italic'), text=text, bg='white', relief='flat', command=cmd, width=15, anchor='w', bd=0)
            btn.grid(row=i+3, column=1)
            self.widget_data.append(btn)

    def clear_screen(self):
        for each in self.widget_data:
            each.destroy()
        if self.entry_box != '':
            self.entry_box.destroy()
        self.entry_box = ''
        self.cvs.delete("all")
        self.base()
        self.window.update()

    def play_screen(self, initialize=False):
        self.clear_screen()
        if initialize:
            self.play_round('', True)
        else:
            temp = ''.join(self.guessed)
            raw_word = self.get_formatted_word(temp)
            limit = len(raw_word)
            self.widget_data = []
            lbl = Label(self.window, font=('Helvetica', 45, "bold"), text=self.category.upper(), bg='white')
            lbl.grid(row=0, column=1, rowspan=2)
            self.widget_data.append(lbl)
            self.entry_box = Entry(self.window, font=('Helvetica', 30, "bold"), text="Guess: ", bg='white')
            self.entry_box.bind('<Return>', lambda event: self.get_guess(event))
            self.entry_box.grid(row=3, column=1)
            self.widget_data.append(self.entry_box)
            for i in range(limit):
                word = raw_word[i]
                text = " ".join(list(word)).upper()
                lbl = Label(self.window, font=('Helvetica', 20, 'italic'), text=text, bg='white')
                ln = i+4
                lbl.grid(row=ln, column=1)
                self.widget_data.append(lbl)
            lim = self.fig
            shift=ln
            for j in range(lim):
                fig = self.figure[j]
                cmd = 'self.'+fig+'()'
                exec(cmd)
            if self.fig == self.total_lives:
                self.stop = True
                raw_word = self.get_formatted_word(self.word)
                for i in range(limit):
                    word = raw_word[i]
                    text = " ".join(list(word)).upper()
                    lbl = Label(self.window, font=('Helvetica', 20, 'italic'), text=text, bg='white', fg='red')
                    lbl.grid(row=shift+i+1, column=1)
                    self.widget_data.append(lbl)
                self.end_time = time()
                shift += 2+i
                time_taken = self.end_time-self.start_time
                text = 'Time Taken: {}s'.format(round(time_taken, 1))
                lbl = Label(self.window, font=('Helvetica', 20, 'italic'), text="YOU LOSE", bg='white', fg='red')
                lbl.grid(row=shift, column=1)
                self.widget_data.append(lbl)
                lbl = Label(self.window, font=('Helvetica', 20, 'italic'), text=text, bg='white', fg='black')
                lbl.grid(row=shift+1, column=1)
                self.widget_data.append(lbl)
            elif "".join(self.guessed) == self.word:
                self.end_time = time()
                time_taken = self.end_time-self.start_time
                self.stop = True
                shift += 1
                lbl = Label(self.window, font=('Helvetica', 20, 'italic'), text="YOU WIN", bg='white', fg='green')
                lbl.grid(row=shift, column=1)
                self.widget_data.append(lbl)
                text = 'Time Taken: {}s'.format(round(time_taken,1))
                lbl = Label(self.window, font=('Helvetica', 20, 'italic'), text=text, bg='white', fg='black')
                lbl.grid(row=shift+2, column=1)
                self.widget_data.append(lbl)
            btn = Button(self.window, font=('Helvetica', 20, 'italic'), text='New Game', command=self.new_game, bg='white', width = 15, bd=2)
            btn.grid(row=15, column=1)
            self.widget_data.append(btn)
            btn = Button(self.window, font=('Helvetica', 20, 'italic'), text='Change Category', command=self.main_screen, bg='white', width = 15, bd=2)
            btn.grid(row=16, column=1)
            self.widget_data.append(btn)
            self.window.update()
        
    def play_round(self, user_guesses='', initialize=False):
        if self.stop:
            return None
        if self.chosen:
            if initialize:
                self.used_in_round = list(self.used_base)
                self.stop = False
                self.start_time = time()
                self.word = self.get_word(self.category)
                self.base()
                self.fig = 0
                self.guessed = list("_" * len(self.word))
                for each in self.used_in_round:
                    if each in self.word:
                        indices = self.get_indices(self.word, each)
                        for ind in indices:
                            self.guessed[ind] = each
            if user_guesses != '':
                for guess in user_guesses:
                    if guess not in self.used_in_round:
                        self.used_in_round.append(guess)
                        if guess in self.word:
                            indices = self.get_indices(self.word, guess)
                            for ind in indices:
                                self.guessed[ind] = guess
                        else:
                            self.fig += 1
            self.play_screen()

    def new_game(self):
        self.stop = False
        self.clear_screen()
        self.stop = False
        self.play_round('', True)

    def get_formatted_word(self, word):
        char_limit = 16
        val = []
        ref = word
        mn = word
        while True:
            if len(ref) < char_limit:
                val.append(ref)
                break
            else:
                basic = list(ref[:char_limit])
                ind = char_limit-list(basic[::-1]).index(' ')
                ref = list(mn[ind:])
                val.append(list(basic[:ind]))
        return val

    def get_indices(self, word, char):
        marker = 0
        data = []
        while char in word[marker:]:
            temp = word[marker:]
            ind = temp.index(char)
            data.append(marker+ind)
            marker += ind+1
        return data
    
    def get_guess(self, event):
        guess = str(self.entry_box.get()).lower()
        self.entry_box.delete(0, END)
        self.play_round(guess)

    def get_category(self, category):
        self.category = category
        self.chosen = True
        self.play_screen(True)

    def get_word(self, cat):
        cat_words = eval('self.'+cat)
        used = list(self.used)
        word = ''
        while word == '':
            temp = rnd(cat_words)
            if temp not in used:
                word = temp
        return word
        

    def base(self):
        self.cvs = Canvas(self.canvasframe, bg='white', width=640, height=720)
        self.cvs.grid(row=0, column=0)
        self.cvs.create_line(75, 80, 565, 80, width=10)
        self.cvs.create_line(80, 80, 80, 640, width=10)
        self.cvs.create_line(75, 640, 565, 640, width=10)
        self.window.update()

    def rope(self):
        self.cvs.create_line(325, 80, 325, 120, width=10)

    def head(self):
        self.cvs.create_oval(275, 125, 375, 225, width=10)

    def body(self):
        self.cvs.create_line(325, 230, 325, 420, width=10)

    def hand1(self):
        self.cvs.create_line(325, 270, 225, 170, width=10)

    def hand2(self):
        self.cvs.create_line(325, 270, 425, 170, width=10)

    def leg1(self):
        self.cvs.create_line(325, 417, 225, 517, width=10)

    def leg2(self):
        self.cvs.create_line(325, 417, 425, 517, width=10)

game = Hangman(easy_mode=False)

