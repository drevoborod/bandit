#!/usr/bin/env python3

import random
import tkinter as tk
import tkinter.font as fonter

from tkinter.messagebox import askyesno, showinfo


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("One-handed bandit")
        self.credit = tk.IntVar(value=0)
        self.stat = 0   # Режим вывода статистики
        self.games_count = tk.IntVar(value=0)   # Сыграно игр
        self.wins = tk.IntVar(value=0)
        self.jackpots = tk.IntVar(value=0)

        frame1 = tk.Frame(self)
        add_button = tk.Button(frame1, text="Pay!", command=self.pay)
        big_font(add_button, 20)
        add_button.grid(row=0, column=0)
        tk.Frame(frame1, height=10).grid(row=1, column=0, rowspan=3)
        tk.Button(frame1, text="Stat", command=self.stat_button).grid(row=5, column=0, rowspan=2, sticky='se')
        frame1.grid(row=0, column=0, sticky='news', padx=10, pady=10)
        frame2 = tk.Frame(self)
        self.text_1 = tk.StringVar(value="Credit:")
        tk.Label(frame2, textvariable=self.text_1).grid(row=0, column=0)
        self.label_1 = tk.Label(frame2, textvariable=self.credit)
        self.label_1.grid(row=1, column=0)
        self.text_2 = tk.StringVar(value="You earned:")
        tk.Label(frame2, textvariable=self.text_2).grid(row=2, column=0)
        self.earned = tk.IntVar(value=0)
        self.label_2 = tk.Label(frame2, textvariable=self.earned)
        self.label_2.grid(row=3, column=0)
        tk.Label(frame2, text="Games played:").grid(row=4, column=0)
        tk.Label(frame2, textvariable=self.games_count).grid(row=5, column=0)
        frame2.grid(row=0, column=1, sticky='news', padx=10, pady=10)
        self.balance = tk.IntVar(value=0)
        tk.Label(frame2, text="Balance:").grid(row=6, column=0)
        tk.Label(frame2, textvariable=self.balance).grid(row=7, column=0)

        frame3 = tk.Frame(self)
        self.result_1 = tk.IntVar()
        result_1 = tk.Label(frame3, width=2, textvariable=self.result_1, state="disabled", relief="sunken")
        self.result_2 = tk.IntVar()
        result_2 = tk.Label(frame3, width=2, textvariable=self.result_2, state="disabled", relief="sunken")
        self.result_3 = tk.IntVar()
        result_3 = tk.Label(frame3, width=2, textvariable=self.result_3, state="disabled", relief="sunken")
        for unit in (result_1, result_2, result_3):
            big_font(unit, 40)
        result_1.grid(row=0, column=0, padx=10, pady=10)
        result_2.grid(row=0, column=1, padx=10, pady=10)
        result_3.grid(row=0, column=2, padx=10, pady=10)
        play = tk.Button(frame3, text="Go!", command=self.play)
        big_font(play, 30)
        play.grid(row=0, column=3)
        frame3.grid(row=0, column=2, sticky='news', padx=10, pady=10)

    def pay(self):
        InputDialog(self, self.credit)

    def stat_button(self):
        if not self.stat:
            self.stat = 1
            self.text_1.set("Wins:")
            self.label_1.config(textvariable=self.wins)
            self.text_2.set("Jackpots:")
            self.label_2.config(textvariable=self.jackpots)
        else:
            self.stat = 0
            self.text_1.set("Credit:")
            self.label_1.config(textvariable=self.credit)
            self.text_2.set("You earned:")
            self.label_2.config(textvariable=self.earned)

    def play(self):
        if self.credit.get() - global_params['price'] < 0:
            showinfo("Out of money!", "Enter more money!")
        else:
            self.credit.set(self.credit.get() - global_params['price'])
            self.games_count.set(self.games_count.get() + 1)
            for result in (self.result_1, self.result_2, self.result_3):
                result.set(random.randint(0, 9))
            if self.result_1.get() == self.result_2.get() == self.result_3.get() == 0:
                self.earned.set(self.earned.get() + global_params['jackpot'])
                self.jackpots.set(self.jackpots.get() + 1)
                self.balance.set(self.balance.get() + global_params['jackpot'])
                showinfo("Jackpot!", "You win a jackpot!!!")
            elif self.result_1.get() == self.result_2.get() == self.result_3.get():
                self.earned.set(self.earned.get() + global_params['win'])
                self.balance.set(self.balance.get() + global_params['win'])
                self.wins.set(self.wins.get() + 1)
                showinfo("Winner!", "You win!")
            else:
                self.balance.set(self.balance.get() - global_params['price'])


class InputDialog(tk.Toplevel):
    def __init__(self, parent=None, variable=None, **options):
        super().__init__(master=parent, **options)
        self.variable = variable
        self.title("Enter money")
        tk.Label(self, text="Input money count:").grid(row=0, column=0)
        self.money = tk.Entry(self, width=7)
        self.money.grid(row=1, column=0, pady=5)
        tk.Button(self, text="Ok", command=self.enter).grid(row=2, column=0, pady=10)
        self.money.focus_set()
        self.money.bind("<Return>", lambda e: self.enter())
        self.wait_window()

    def enter(self):
        value = self.money.get()
        try:
            res = int(value)
        except ValueError:
            pass
        else:
            self.variable.set(self.variable.get() + res)
            self.destroy()


def big_font(unit, size=9):
    """Font size of a given unit change."""
    fontname = fonter.Font(font=unit['font']).actual()['family']
    unit.config(font=(fontname, size))


PRICE = 5
WIN = 100
JACKPOT = 1000
global_params = {'price': PRICE, 'win': WIN, 'jackpot': JACKPOT}

if __name__ == "__main__":
    run = MainWindow()
    run.mainloop()