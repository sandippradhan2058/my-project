import hashlib
from subprocess import call
import pickle
import random
import smtplib
import sqlite3
from tkinter import END, Button, Entry, Label, PhotoImage, StringVar, Tk, Toplevel, messagebox
import tkinter
from login_pg import login

class forget_password:
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
#String         
                self.var_email = StringVar()
                self.code = StringVar()
                self.newpass = StringVar()
                self.confpass = StringVar()
                header = Label (self.root,text='Forget Password',fg='Red',bg ='#FDE8E3',font=("Times New Roman",40,'bold')).place(x=200,y=50)
                email= Label(self.root,text='Email address     :- ',fg='Black',bg ='#FDE8E3',font=("Times New Roman",30,)).place(x=50,y=200)
                otp= Label(self.root,text='One Time Password    :- ',fg='Black',bg ='#FDE8E3',font=("Times New Roman",24,)).place(x=50,y=300)

#Text box
                txt_user_id=Entry(self.root, textvariable=self.var_email,font=("Times New ROman",30)).place(x=380,y=200)
                txt_otp = Entry(self.root, textvariable=self.code,font=("Times New ROman",24)).place(x=380,y=300,width=150)
                

#Button 
                send_button = Button (self.root,text='Send',cursor = 'hand2',command=self.send,fg='blue',font=("Times New ROman",20)).place(x=380,y=260,height=35)
                
                check_button = Button(self.root,text='Check',cursor = 'hand2',fg='Red',command=self.check,font=("Times New ROman",20)).place(x=380,y=350,height=35)
                login_button=Button(self.root,text='Login',cursor = 'hand2',fg='green',command=self.login,font=("Times New ROman",20)).place(x=700,y=20,height=40)

    def check(self):
        
            if self.otp_number != self.code:
                messagebox.showerror('Error','Otp dont match',parent=self.root)
            else:
                newpass = Label (self.root,text='New Password           :-',fg='black',bg ='#FDE8E3',font=("Times New Roman",24)).place(x=50,y=400)
                confpass= Label(self.root,text='Confirm Passowrd     :- ',fg='Black',bg ='#FDE8E3',font=("Times New Roman",24,)).place(x=50,y=450)

                txt_nex=Entry(self.root, textvariable=self.newpass,font=("Times New ROman",24)).place(x=380,y=400)
                txt_pass = Entry(self.root, textvariable=self.confpass,font=("Times New ROman",24)).place(x=380,y=450)
                save_button = Button (self.root,text='Save',fg='Green',cursor = 'hand2',command=(),font=("Times New ROman",20)).place(x=380,y=500,height=35)

                if self.newpass.get()=='' or self.confpass.get()=='':
                    messagebox.showerror('Error','please fill all details',parent=self.root)
                elif self.newpass.get()!= self.confpass.get():
                    messagebox.showerror('Error','Password dosent match',parent=self.root)

                else:
                    newpass_hash_save = hashlib.sha1(bytes(self.newpass.get(),encoding='utf-8'))
                    password = newpass_hash_save.hexdigest()
                    con= sqlite3.connect( database=r'user.db')
                    cur = con.cursor()

                    cur.execute('update user set password=%s where email = %s',(password,self.var_email.get()))
                    con.commit()
                    con.close
                    messagebox.showinfo("Success", "Your password is reset.\nPlease, Login with new Password.", parent=self.root)
                    
                    
                    self.root.destroy()
                    call(["python", "login.py"])



                    

    def login(self):
        login(root)

    def send(self):
        resend_button = Button (self.root,text='Resend',cursor = 'hand2',command=self.resend,fg='blue',font=("Times New ROman",20)).place(x=480,y=260,height=35)
        if self.var_email.get()=='':
            messagebox.showerror('Error','Please enter your email address',parent=self.root)
        else:
            con= sqlite3.connect( database=r'user.db')
            cur = con.cursor()
            find_email = ("Select email from user where email = ?")
            cur.execute(find_email,[self.var_email.get()])
            user_email = cur.fetchone()
            
            if user_email[0] != self.var_email.get():
                messagebox.showerror('Error','Email dosent exist',parent= self.root)
            else:
                
                self.otp_number = ''.join([str(random.randint(0,9)) for i in range (6)]) 

                cur.execute("Select email from user where user_id = ?",[(self.var_email.get())])
                email = cur.fetchone()

                self.gmail_server = smtplib.SMTP('smtp.gmail.com',587)
                self.gmail_server.starttls()
                self.gmail_server.login('sandippradhan9810129148@gmail.com',password='cfsltjacqbodgkei')
                serialized = pickle.dumps(self.otp_number)
                self.code = pickle.loads(serialized)
                self.msg ='hello your OTP is '+self.otp_number
                self.gmail_server.sendmail('sandippradhan9810129148@gmail.com',self.var_email.get(),self.msg)
                self.gmail_server.quit()
                messagebox.showinfo('Success','OTP Sent')
                

    def resend(self):

        self.re_otp_number = ''.join([str(random.randint(0,9)) for i in range (6)])         
        self.gmail_server = smtplib.SMTP('smtp.gmail.com',587)
        self.gmail_server.starttls()
        self.gmail_server.login('sandippradhan9810129148@gmail.com',password='cfsltjacqbodgkei')
        self.msg ='hello your OTP is '+self.re_otp_number
        self.gmail_server.sendmail('sandippradhan9810129148@gmail.com',self.var_email.get(),self.msg)
        self.gmail_server.quit()
        messagebox.showinfo('Success','OTP  Resent',parent=self.root)
        self.otp_number.delete(0,END)




if __name__ == '__main__':
    root=Tk()
    register_object = forget_password(root)
    root.mainloop()