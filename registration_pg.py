# USER REGISTRSTION INTERFACE

import hashlib
import sqlite3
from subprocess import call
import re
from tkinter import *
from tkinter import messagebox
from tkinter.tix import IMAGETEXT
from tokenize import String
import subprocess
from cryptography.fernet import Fernet
class registration:

        def __init__(self,root):
                self.root = root #GUI Container
                self.root.geometry('800x600+350+100') #GUI AREA SIZE
                self.root.title(' ☺SMILE QUIZ GAME☺') # Windows Title
                self.root.config(bg='white') 

#Icon
                photo_icon = PhotoImage(file='images/icon/smileicon.png')
                self.root.iconphoto(False,photo_icon)

#Background Image
                self.background_img_file = PhotoImage(file="images/background/background.png")
                self.background_image = Label(self.root, image=self.background_img_file)
                self.background_image.pack()
        
#Label
                registration_headline_label= Label (self.root,text='REGISTRATION FORM',fg='Black',font=("Times New Roman",40,"bold")).place(x=100,y=10)
                user_id= Label (self.root,text='USER ID        :-',fg='Black',bg = '#FDE8E3',font=("Times New Roman",20,)).place(x=30,y=150)
                full_name=Label (self.root,text='FULL NAME :-',fg='Black',bg = '#FDE8E3',font=("Times New Roman",20,)).place(x=30,y=200)
                email= Label (self.root  ,text='EMAIL           :-',fg='Black',bg = '#FDE8E3',font=("Times New Roman",20,)).place(x=30,y=250)
                password=Label (self.root,text='PASSWORD  :-',fg='black',bg = '#FDE8E3',font=("Times New Roman",20,)).place(x=30,y=300)


#Variables
                self.var_user_id =StringVar()
                self.var_full_name =StringVar()
                self.var_email =StringVar()
                self.var_password = StringVar()
                

# Text box
                txt_user_id=Entry(self.root, textvariable=self.var_user_id,font=("Times New ROman",20)).place(x=300,y=150)
                txt_full_name=Entry(self.root, textvariable=self.var_full_name,font=("Times New ROman",20)).place(x=300,y=200)
                txt_email=Entry(self.root, textvariable=self.var_email,font=("Times New ROman",20)).place(x=300,y=250)
                txt_password=Entry(self.root,textvariable = self.var_password,show="*",font=("Times New ROman",20)).place(x=300,y=300)


#Button
                save_button = Button(self.root,text="Save ",command = self.save ,font=("Times New Roman",25),bg="Green",fg="black",cursor='hand2').place(x=300,y=420,width=100,height=35)
                back_button = Button(self.root,text="Back ",command = self.back,font=("Times New Roman",25),bg="#D95750",fg="black",cursor='hand2').place(x=482,y=420,width=100,height=35)


        def emailcheck(self,email):
                if re.match("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", email):
                        return True
                else :
                        
                        return False
        def save(self):
                con= sqlite3.connect( database=r'user.db')
                cur = con.cursor()
                                
                if self.var_user_id.get()=='' or self.var_full_name.get()=='' or self.var_email.get()=='' or self.var_password.get()=='':
                                messagebox.showerror("Error","Please enter required details",parent= self.root)
                elif len(self.var_password.get())< 8 :
                                        messagebox.showerror("Error","Password must be at least 8 character",parent=self.root)
                elif (self.emailcheck(self.var_email.get()) != True):
                                messagebox.showerror('Invalid','Invalid Email',parent= self.root)
                                        

                else:
                        try:

                                                              

                                
                                cur.execute("select * from user where user_id = ?",(self.var_user_id.get()))
                                user_exist = cur.fetchone()
                                
                                find_email = ("Select * from user where user_id= ?")
                                cur.execute(find_email,(self.var_user_id.get()))
                                email_exist = cur.fetchone()
                                


                                
                        
                                if user_exist != None :
                                        messagebox.showerror('Error','users id lready exist',parent= self.root)                     
                                elif email_exist != None:
                                        messagebox.showerror('Error','email address already exist',parent= self.root)                     
                                else:                                 
                                        hash_pass = hashlib.sha1(bytes(self.var_password.get(),encoding='utf-8'))
                                        hex_password = hash_pass.hexdigest()
                                        
                                
                                        cur.execute("Insert into user ( user_id, fullname, email, password ) values(?, ?, ?, ?)",(self.var_user_id.get(),self.var_full_name.get(),self.var_email.get(),hex_password))
                                 
                                        
                                 
                                        messagebox.showinfo("Successful",f"Successfully Registered : {self.var_full_name.get()}", parent=self.root)
                                        self.root.destroy()
                                        con.commit()
                                        con.close()
                                        call(["python",'login_pg.py'])                      
                                 
                                
                        
                        

                        except Exception as e:
                                messagebox.showerror("Error",'Error on find_user due to :',parent= self.root)

                
        
        def back(self):
                pass
                self.root.destroy()
                call (["python",'login_pg.py'])

        

                
                
if __name__ == '__main__':
     root=Tk()
     register_object = registration(root)
     root.mainloop()