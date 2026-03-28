from tkinter import *
from PIL import Image, ImageTk, ImageDraw
from datetime import datetime
from math import *
import time
import sqlite3
from tkinter import messagebox,ttk
import os

class Login_Window:
        def __init__(self, root):
                self.root = root
                self.root.title("Login Window")
                self.root.geometry("1350x700+100+80")
                self.root.config(bg="#021e2f")

                #----------Background Colors----------
                left_lbl=Label(self.root,bg="#08A3D2",bd=0)
                left_lbl.place(x=0,y=0,relheight=1,width=600)
                right_lbl=Label(self.root,bg="#031F3C",bd=0)
                right_lbl.place(x=600,y=0,relheight=1,relwidth=1)

                #-----------Frames-----------
                login_frame=Frame(self.root,bg="white")
                login_frame.place(x=250,y=100,width=800,height=500)

                title=Label(login_frame,text="LOGIN HERE",font=("times new roman",30,"bold"),bg="white",fg="#08A3D2").place(x=250,y=50)

                email=Label(login_frame,text="EMAIL ADDRESS",font=("times new roman",16,"bold"),bg="white",fg="grey").place(x=250,y=150)
                self.txt_email=Entry(login_frame,bg="lightgray",font=("times new roman",15))
                self.txt_email.place(x=250,y=190,width=350,height=35)

                password=Label(login_frame,text="PASSWORD",font=("times new roman",16,"bold"),bg="white",fg="grey").place(x=250,y=250)
                self.txt_password=Entry(login_frame,bg="lightgray",font=("times new roman",15))
                self.txt_password.place(x=250,y=280,width=350,height=35)

                btn_reg=Button(login_frame,text="Register new Account?",font=("times new roman",14),bd=0,bg="white",fg="#B00857",cursor="hand2",command=self.register_window).place(x=250,y=320)
                btn_forget=Button(login_frame,text="Forgot Password?",font=("times new roman",14),bd=0,bg="white",fg="red",cursor="hand2",command=self.forget_password_window).place(x=460,y=320)
                btn_login=Button(login_frame,text="Login",font=("times new roman",20,"bold"),fg="white",bg="#B00857",cursor="hand2",command=self.login).place(x=250,y=380,width=180,height=40)

                #----------Clock----------
                self.lbl = Label(self.root,text="\nAnalog Clock",font=("Book Antiqua",25,"bold"),compound=BOTTOM,bg="#081923",fg="white",bd=0)
                self.lbl.place(x=90, y=120, height=450, width=350)

                self.working()
        
        def reset(self):
                self.cmb_quest.current(0)
                self.txt_answer.delete(0,END)
                self.txt_new_password.delete(0,END)
                self.txt_password.delete(0,END)
                self.txt_email.delete(0,END)

        def forget_password(self):
                if self.cmb_quest=="Select" or self.txt_answer=="" or self.txt_password=="":
                        messagebox.showerror("Error","All Fields Are Required",parent=self.root2)
                else:
                        try:
                                con=sqlite3.connect(database="rms.db")
                                cur=con.cursor()
                                cur.execute("select * from Users where email=? and question=? and answer=?",(self.txt_email.get(),self.cmb_quest.get(),self.txt_answer.get()))
                                row=cur.fetchone()
                                if row==None:
                                        messagebox.showerror("Error","Please Select Correct Security Question / Enter Answer",parent=self.root2)
                                else:
                                        cur.execute("update Users set password=? where email=?",(self.txt_new_password.get(),self.txt_email.get()))
                                        con.commit()
                                        con.close()
                                        messagebox.showinfo("Success","You password has been reset,please login with new password",parent=self.root2)
                                        self.reset()
                                        self.root2.destroy()
                        except Exception as e:
                                messagebox.showerror("Error",f"Error due to: {str(e)}",parent=self.root2)


        def forget_password_window(self):
                if self.txt_email.get()=="":
                        messagebox.showerror("Error","Please enter the valid email address to reset your password",parent=self.root)
                else:
                        try:
                                con=sqlite3.connect(database="rms.db")
                                cur=con.cursor()
                                cur.execute("select * from Users where email=?",(self.txt_email.get(),))
                                row=cur.fetchone()
                                if row==None:
                                        messagebox.showerror("Error","Invalid Email Address",parent=self.root)
                                else:
                                        con.close()
                                        self.root2=Toplevel()
                                        self.root2.title("Forget Password")
                                        self.root2.geometry("400x400+595+240")
                                        self.root2.focus_force()
                                        self.root2.grab_set()
                                        self.root2.config(bg="white")
                                        t=Label(self.root2,text="Forget Password",font=("times new roman",20,"bold"),bg="white",fg="red").place(x=0,y=10,relwidth=1)

                                        #----------Forget Password----------
                                        question=Label(self.root2,text="Security Question",font=("times new roman",15,"bold"),bg="white",fg="grey").place(x=130,y=80)
                                        self.cmb_quest=ttk.Combobox(self.root2,font=("times new roman",13),state="readonly",justify=CENTER)
                                        self.cmb_quest['values']=("Select","Your First Pet Name","Your Birth Place","Your Best Friend Name")
                                        self.cmb_quest.place(x=80,y=110,width=250)
                                        self.cmb_quest.current(0)

                                        answer=Label(self.root2,text="Answer",font=("times new roman",15,"bold"),bg="white",fg="grey").place(x=170,y=160)
                                        self.txt_answer=Entry(self.root2,font=("times new roman",15),bg="lightgrey")
                                        self.txt_answer.place(x=80,y=190,width=250)

                                        new_password=Label(self.root2,text="New Password",font=("times new roman",15,"bold"),bg="white",fg="grey").place(x=130,y=240)
                                        self.txt_new_password=Entry(self.root2,font=("times new roman",15),bg="lightgrey")
                                        self.txt_new_password.place(x=80,y=270,width=250)

                                        btn_change_password=Button(self.root2,text="Reset Password",bg="green",fg="white",font=("times new roman",15,"bold"),cursor="hand2",command=self.forget_password).place(x=130,y=330)
                                        
                        except Exception as e:
                                messagebox.showerror("Error",f"Error due to: {str(e)}",parent=self.root)
                        

        def register_window(self):
                self.root.destroy()
                os.system("python register.py")

        def login(self):
                if self.txt_email.get()=="" or self.txt_password.get()=="":
                        messagebox.showerror("Error","All Fields Are Required",parent=self.root)
                else:
                        try:
                                con=sqlite3.connect(database="rms.db")
                                cur=con.cursor()
                                cur.execute("select * from Users where email=? and password=?",(self.txt_email.get(),self.txt_password.get()))
                                row=cur.fetchone()
                                if row==None:
                                        messagebox.showerror("Error","Invalid Username & Password",parent=self.root)
                                else:
                                        messagebox.showinfo("Success","Welcome",parent=self.root)
                                        self.root.destroy()
                                        os.system("python dashboard.py")
                                con.close()
                        except Exception as e:
                                messagebox.showerror("Error",f"Error due to: {str(e)}",parent=self.root)

        def clock_image(self, hr, min_, sec_):
                scale = 3
                size = 400 * scale
                clock = Image.new("RGB", (size, size), (8, 25, 35))
                draw = ImageDraw.Draw(clock)

                bg = Image.open("images/c.png").resize((300*scale, 300*scale), Image.LANCZOS)
                clock.paste(bg, (50*scale, 50*scale))
                center = 200 * scale
                #----------Hour Line----------
                draw.line((center, center,center + 50*scale*sin(radians(hr)),center - 50*scale*cos(radians(hr))),fill="#DF005E", width=8)
                #----------Minute Line---------
                draw.line((center, center,center + 80*scale*sin(radians(min_)),center - 80*scale*cos(radians(min_))),fill="white", width=5)
                #----------Second Line----------
                draw.line((center, center,center + 100*scale*sin(radians(sec_)),center - 100*scale*cos(radians(sec_))),fill="yellow", width=3)

                draw.ellipse((center-5*scale, center-5*scale,center+5*scale, center+5*scale), fill="cyan")

                clock = clock.resize((400, 400), Image.LANCZOS)

                return clock

        def working(self):
                now = datetime.now()

                h = now.hour % 12
                m = now.minute
                s = now.second

                hr = (h + m/60) * 30
                min_ = (m + s/60) * 6
                sec_ = s * 6

                img = self.clock_image(hr, min_, sec_)
                self.img = ImageTk.PhotoImage(img)
                self.lbl.config(image=self.img)

                self.lbl.after(1000, self.working)


root = Tk()
obj = Login_Window(root)
root.mainloop()