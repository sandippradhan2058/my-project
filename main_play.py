# Import the required libraries
import ssl
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from subprocess import call
import subprocess
from PIL import Image, ImageTk
from urllib.request import urlopen
from requests import Session
import json
from tkinter import END, Image

import requests
import urllib.request
import bs4
import base64
import io
from PIL import ImageTk, Image
import time
import sys

 
root = tk.Tk()
root.title("smiley_game")
root.geometry("800x600+350+100")
root.resizable(False, False)
 
 
class Smiley_Game:
    def __init__(self, ques, soln) :
        self.ques = ques
        self.soln = soln
        self.score = 0
        self.name = sys.argv[1]
        name= self.name.upper()
        self.imagelab = tk.Label(root)
        self.imagelab.place(x=70,y=100)
        
 
 
        # logout button
        logout = Button(root, text="Log Out", command=self.logout_function, cursor="hand2", font=(
            "Helvetica 15 underline"), bg="#d77337", fg="white", activebackground="white", bd=0)
        logout.place(x=600, y=20, width=120)
 
        # label
        title = Label(root, text=f'WELCOME {(name)}',
                      font=("Impact", 36, "bold"),bg='#FDE8E3', fg="Red")
        title.place(x=220, y=10)
 
 
        # Entry Input
        self.answer = Entry(root,  font=(
            "times new Roman", 14), bg="lightgray")
        self.answer.place(x=300, y=520, width=200, height=50)
 
        result = Button(root, text="Submit", cursor="hand2", command=self.result_function,
                        font=("times new Roman", 14), bg="#d25d17", fg="white")
        result.place(x=100, y=525, width=120)
 
        self.score_res = tk.Label(root,font=(
            "times new Roman", 22))
        self.score_res.place(x=600, y=525)
        self.score_res.config(text=f'Score:- {str(self.score)}')
        self.show_image()
 
 
    # functionality   
    def show_image(self):
        self.ques, self.soln = Smiley_Game.create_image()
        with urllib.request.urlopen(self.ques) as u:
            raw_data = u.read()
        self.image = tk.PhotoImage(data=base64.encodebytes(raw_data))
        image = Image.open(io.BytesIO(raw_data))
        self.image = ImageTk.PhotoImage(image)
        self.imagelab.config(image=self.image)
        root.after(1000*10, self.show_image)
 
    def logout_function(self):
        time.sleep(0)
        root.destroy()
        call(["python", "login.py"])
 
    @staticmethod
    def create_image():
        ssl._create_default_https_context = ssl._create_unverified_context
        api_url = "https://marcconrad.com/uob/smile/api.php"
        response = urllib.request.urlopen(api_url)
        smileJson = json.loads(response.read())
        question = smileJson['question']
        solution = smileJson['solution']
        return question, solution
 
 
    def result_function(self):
        if self.answer.get() == "":
            messagebox.showerror(
                "Error", "Please submit the answer", parent=root)
        elif self.answer.get() != str(self.soln):
            messagebox.showerror(
                "Error", "Try Again!", parent=root)
            self.answer.delete(0, END)
        else:
            messagebox.showinfo(
                "Success", "Correct Answer!", parent=root)
            self.score += 1
            self.answer.delete(0, END) 
            self.score_res.config(text=f'Score :-{str(self.score)}')
            self.show_image()
 
 
if __name__ == '__main__':
    ques, soln= Smiley_Game.create_image()
    print(ques, soln)
    img = Smiley_Game(ques, soln)
 
    # icon_img = PhotoImage(file="Image\icon.png")
    # root.iconphoto(False, icon_img)
    root.config(bg='#FDE8E3')
    root.mainloop()
