# It's a class that creates a GUI window with a background image, a login button, a forget password
# button, and a new user button. 
# 
# The login button is supposed to check the user's credentials against a database and if they match,
# it should open a new window. 
# 
# The forget password button is supposed to open a new window that allows the user to reset their
# password. 
# 
# The new user button is supposed to open a new window that allows the user to create a new account. 
# 
# The problem is that when I run the code, the GUI window opens, but when I click on any of the
# buttons, nothing happens. 
# 
# I've tried to debug the code, but I can't figure out what's wrong. 
# 
# I've tried to run the code on both Python 2.7 and Python 3.6, but I get import hashlib
import hashlib
import sqlite3
from subprocess import call
from tkinter import Button, Entry, Label, PhotoImage, StringVar, Tk, messagebox
import cryptography
from cryptography.fernet import Fernet

class login:
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
                user_id = Label(self.root,text='USER ID      :- ',fg='Black',bg ='#FDE8E3',font=("Times New Roman",30,)).place(x=50,y=130)
                password =Label (self.root,text='PASSWORD :-',fg='Black',bg = '#FDE8E3',font=("Times New Roman",30,)).place(x=50,y=250)

# Variables
                self.var_user_id = StringVar()
                self.var_password = StringVar()
# Text box
                txt_user_id=Entry(self.root, textvariable=self.var_user_id,bg = 'white',font=("Times New ROman",30)).place(x=325,y=130)
                txt_passowrd=Entry(self.root, textvariable=self.var_password,bg ="white",font=("Times New ROman",30)).place(x=325,y=250)

#Login button
                login_button = Button(self.root,text="Login ",command =self.login,font=("Times New Roman",35,),bg="#795756",fg="white",cursor='hand2', ).place(x=320,y=360,width=200,height=55)
                forget_button= Button(self.root,text="Forget ",command = self.forget,font=("Times New Roman",30,),fg="red",cursor='hand2', ).place(x=200,y=500,width=200,height=55)
                create_button= Button(self.root,text="New One ",command = self.create,font=("Times New Roman",30,),fg="red",cursor='hand2', ).place(x=450,y=500,width=200,height=55)
                

        def forget(self):
                self.root.destroy()
                call(["python", "forget_password.py"])
        

        def login(self):
                con= sqlite3.connect( database=r'user.db')
                cur = con.cursor()
                if self.var_user_id.get()=='' or self.var_password.get() == '':
                        messagebox.showerror("Error ","Please fill the required details",parent= self.root)

                else:
                        cur.execute('select user_id from user where user_id = ?',(self.var_user_id.get()))
                        user = cur.fetchone()

                        try:
                                
                                if user == None:
                                        messagebox.showerror('Error',"User Doesn't exist",parent=self.root)

                                else :
                                        
                                        cur.execute('select password from user where user_id= ? ',(self.var_user_id.get()))
                                        user_pass = cur.fetchone()
                                        
                                        password  = hashlib.sha1(bytes(self.var_password.get(),encoding='utf-8'))
                                        print('ds')
                                        hex_password = password.hexdigest()  

                                        cur.execute('select fullname from user where user_id= ? ',(self.var_user_id.get()))
                                        data_name = cur.fetchone()                                    
                                        

                                        if hex_password!= user_pass[0]:
                                                
                                                messagebox.showerror("Error",'Wrong password',parent=self.root) 
                                        else:
                                                name = data_name[0]
                                                self.root.destroy()
                                                call(["python",'main_play.py',f'{name}']) 

                                        con.close()                                  

                        except Exception as e:
                                messagebox.showerror("Error",'Error on login due to :',parent= self.root)



        def create(self):
                self.root.destroy()
                call(['python','registration_pg.py'])
                



                
if __name__ == '__main__':
    root=Tk()
    register_object = login(root)
    root.mainloop()