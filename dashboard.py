from tkinter import *
from PIL import Image,ImageTk,ImageDraw
import sqlite3
from course import Course
from student import Student
from result import Result
from report import Report
import os
from datetime import datetime
from math import *
from tkinter import messagebox
import time

class RMS:
    def __init__(self,root):
        self.root=root
        self.root.title("Student Result Management System")
        self.root.geometry("1350x700+80+170")
        self.root.config(bg="white")
        #-----Icons-----
        img = Image.open("images/logo_p.png")
        img = img.resize((40,40),Image.Resampling.LANCZOS)
        self.logo_dash=ImageTk.PhotoImage(img)
        #-----Title-----
        title=Label(self.root,text="Student Result Management System",compound=LEFT,padx=10,height=10,image=self.logo_dash,font=("goudy old style",20,"bold"),bg="#033054",fg="white").place(x=0,y=0,relwidth=1,height=60)
        #----Menu-----
        M_Frame = LabelFrame(self.root,text="Menus",font=("times new roman",15),bg="white")
        M_Frame.place(x=10,y=70,width=1330,height=80)

        btn_course=Button(M_Frame,text="Course",font=("goudy old style",15,"bold"),bg="#0b5377",fg="white",cursor="hand2",command=self.add_course).place(x=20,y=5,width=200,height=40)
        btn_student=Button(M_Frame,text="Student",font=("goudy old style",15,"bold"),bg="#0b5377",fg="white",cursor="hand2",command=self.add_student).place(x=240,y=5,width=200,height=40)
        btn_result=Button(M_Frame,text="Result",font=("goudy old style",15,"bold"),bg="#0b5377",fg="white",cursor="hand2",command=self.add_result).place(x=460,y=5,width=200,height=40)
        btn_view=Button(M_Frame,text="View Student Results",font=("goudy old style",15,"bold"),bg="#0b5377",fg="white",cursor="hand2",command=self.add_view).place(x=680,y=5,width=200,height=40)
        btn_logout=Button(M_Frame,text="Logout",font=("goudy old style",15,"bold"),bg="#0b5377",fg="white",cursor="hand2",command=self.logout).place(x=900,y=5,width=200,height=40)
        btn_exit=Button(M_Frame,text="Exit",font=("goudy old style",15,"bold"),bg="#0b5377",fg="white",cursor="hand2",command=self.exit).place(x=1120,y=5,width=200,height=40)

        #-----Content_Window-----
        #------Clock------
        self.lbl = Label(self.root,text="\nAnalog Clock",font=("Book Antiqua",25,"bold"),compound=BOTTOM,bg="#081923",fg="white",bd=0)
        self.lbl.place(x=26, y=180, height=450, width=350)
        self.working()
        # self.bg_img=Image.open("images/bg.png")
        self.bg_img=Image.open("images/bg.png")
        self.bg_img=self.bg_img.resize((620,350),Image.Resampling.LANCZOS)
        self.bg_img=ImageTk.PhotoImage(self.bg_img)

        self.lbl_bg=Label(self.root,image=self.bg_img).place(x=400,y=180,width=620,height=350)

        #-----Update_Details-----
        self.lbl_course=Label(self.root,text="Total Course\n[ 0 ]",font=("goudy old style",20),bd=10,relief=RIDGE,bg="#e43b06",fg="white")
        self.lbl_course.place(x=400,y=530,width=300,height=100)

        self.lbl_student=Label(self.root,text="Total Students\n[ 0 ]",font=("goudy old style",20),bd=10,relief=RIDGE,bg="#0676ad",fg="white")
        self.lbl_student.place(x=710,y=530,width=300,height=100)

        self.lbl_result=Label(self.root,text="Total Results\n[ 0 ]",font=("goudy old style",20),bd=10,relief=RIDGE,bg="#038074",fg="white")
        self.lbl_result.place(x=1020,y=530,width=300,height=100)
        
        self.update_details()

        #-----Footer-----
        footer=Label(self.root,text="SRMS -- Student Result Management System\nContact Us for any Technical Issue: 9635219993",font=("goudy old style",12),bg="#262626",fg="white").pack(side=BOTTOM,fill=X)
    
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

    def add_course(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=Course(self.new_win)
    
    def add_student(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=Student(self.new_win)
    
    def add_result(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=Result(self.new_win)
    
    def add_view(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=Report(self.new_win)
    
    def update_details(self):
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        try:
            cur.execute("select count(*) from course")
            course_count = cur.fetchone()[0]
            self.lbl_course.config(text=f"Total Course\n[ {course_count} ]")
            cur.execute("select count(*) from student")
            student_count = cur.fetchone()[0]
            self.lbl_student.config(text=f"Total Students\n[ {student_count} ]")
            cur.execute("select count(*) from result")
            result_count = cur.fetchone()[0]
            self.lbl_result.config(text=f"Total Results\n[ {result_count} ]")
        except Exception as ex:
            print("Error:", ex)
        self.lbl_result.after(2000, self.update_details)

    def logout(self):
        op=messagebox.askyesno("Confirm","Do you really want to logout?",parent=self.root)
        if op==True:
            self.root.destroy()
            os.system("python login.py")
    
    def exit(self):
        op=messagebox.askyesno("Confirm","Do you really want to exit?",parent=self.root)
        if op==True:
            self.root.destroy()

if __name__=="__main__":
    root=Tk()
    obj=RMS(root)
    root.mainloop()
