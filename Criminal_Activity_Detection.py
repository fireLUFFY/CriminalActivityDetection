from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
from collections.abc import Mapping
from keras.models import load_model
from collections import deque
import numpy as np
import ast
import pickle
import sklearn
import cv2
import os

model=load_model("ClassModel")
lb=pickle.loads(open("ClassModelbinarizer.pickle","rb").read())

w=Tk()
w.geometry('925x500')
w.title('Login')
w.configure(bg='#ff4f5a')
w.minsize(925,500)


def signin():
    signin_win=Frame(w,width=925,height=500,bg='white')
    signin_win.place(x=0,y=0)
    f1=Frame(signin_win,width=350,height=350,bg='white')
    f1.place(x=480,y=100)
    
    global img1
    img1 = ImageTk.PhotoImage(Image.open("signin.png"))
    Label(signin_win,image=img1,border=0,bg='white').place(x=50,y=50)

    l2=Label(signin_win,text="Sign in",fg='#ff4f5a',bg='white')
    l2.config(font=('Microsoft YaHei UI Light',23, 'bold'))
    l2.place(x=600,y=60)

    def on_enter(e):
        e1.delete(0,'end')    
    def on_leave(e):
        if e1.get()=='':   
            e1.insert(0,'Username')

    
    e1 =Entry(f1,width=25,fg='black',border=0,bg='white')
    e1.config(font=('Microsoft YaHei UI Light',11, ))
    e1.bind("<FocusIn>", on_enter)
    e1.bind("<FocusOut>", on_leave)
    e1.insert(0,'Username')
    e1.place(x=30,y=60)

    Frame(f1,width=295,height=2,bg='black').place(x=25,y=87)

    #------------------------------------------------------

    def on_enter(e):
        e2.delete(0,'end')    
    def on_leave(e):
        if e2.get()=='':   
            e2.insert(0,'Password')

    
    e2 =Entry(f1,width=21,fg='black',border=0,bg='white')
    e2.config(font=('Microsoft YaHei UI Light',11, ))
    e2.bind("<FocusIn>", on_enter)
    e2.bind("<FocusOut>", on_leave)
    e2.insert(0,'Password')
    e2.place(x=30,y=130)

    Frame(f1,width=295,height=2,bg='black').place(x=25,y=157)

    #-mech------------------------------------------------
    def signin_cmd():
        
        file=open('datasheet.txt','r')
        d=file.read()
        r=ast.literal_eval(d)
        file.close()
        

        key=e1.get()
        value=e2.get()
        
        if key in r.keys() and value==r[key]:           
            messagebox.showinfo("","     successfully logged in    ")
            w.destroy()

            print("enter choice: V for input video or C for camera: ")
            response = input("V/C: ")

            if(response == "V" or response == "v"):
                input_video_path = input("enter the path of the input video: ")
            
            mean=np.array([123.68,116.779,103.939][::1],dtype="float32")
            Q=deque(maxlen=256)

            if response=="V" or response=="v":
                capture_video=cv2.VideoCapture(input_video_path)
            else:
                capture_video=cv2.VideoCapture(0)
                
            writer=None
            (Width, Height)=(None,None)

            # def run():
            while True:
                (taken,frame)=capture_video.read()
                if not taken:
                    break;
                if Width is None or Height is None:
                    (Width, Height)=frame.shape[:2]
                
                output=frame.copy()
                frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                frame=cv2.resize(frame,(224,224)).astype("float32")
                frame-=mean
                preds=model.predict(np.expand_dims(frame,axis=0))[0]
                Q.append(preds)
                results=np.array(Q).mean(axis=0)
                i=np.argmax(results)
                label=lb.classes_[i]
                text="Detected: {}".format(label)
                cv2.putText(output,text,(10,20),cv2.FONT_HERSHEY_SIMPLEX,1.00,(0,155,0),4)
                
                if writer is None:
                    fourcc=cv2.VideoWriter_fourcc(*"MJPG")
                    writer=cv2.VideoWriter("output_video",fourcc,30,(Width,Height),True)
                writer.write(output)
                cv2.imshow('in progress',output)
                key=cv2.waitKey(1)&0xFF

                if key==ord("q"):
                    break
                    
            print("Finalising...")
            writer.release()
            capture_video.release()
            cv2.destroyAllWindows()
        else:
            messagebox.showwarning('try again', 'invalid username or password')


    #------------------------------------------------------
    Button(f1,width=39,pady=7,text='Sign in',bg='#ff4f5a',fg='white',border=0,command=signin_cmd).place(x=35,y=204)
    l1=Label(f1,text="Don't have an account?",fg="black",bg='white')
    l1.config(font=('Microsoft YaHei UI Light',9, ))
    l1.place(x=75,y=250)

    b2=Button(f1,width=6,text='Sign up',border=0,bg='white',fg='#ff4f5a',command=signup)
    b2.place(x=215,y=250)




def signup():
    signup_win=Frame(w,width=925,height=500,bg='white')
    signup_win.place(x=0,y=0)
    f1=Frame(signup_win,width=350,height=350,bg='white')
    f1.place(x=480,y=70)

    
    global img2
    img2 = ImageTk.PhotoImage(Image.open("signup.png"))
    Label(signup_win,image=img2,border=0,bg='white').place(x=30,y=90)

    l2=Label(signup_win,text="Sign up",fg='#ff4f5a',bg='white')
    l2.config(font=('Microsoft YaHei UI Light',23, 'bold'))
    l2.place(x=600,y=60)

    def on_enter(e):
        e1.delete(0,'end')    
    def on_leave(e):
        if e1.get()=='':   
            e1.insert(0,'Username')

    
    e1 =Entry(f1,width=25,fg='black',border=0,bg='white')
    e1.config(font=('Microsoft YaHei UI Light',11, ))
    e1.bind("<FocusIn>", on_enter)
    e1.bind("<FocusOut>", on_leave)
    e1.insert(0,'Username')
    e1.place(x=30,y=60)

    Frame(f1,width=295,height=2,bg='black').place(x=25,y=87)

    #------------------------------------------------------

    def on_enter(e):
        e2.delete(0,'end')    
    def on_leave(e):
        if e2.get()=='':   
            e2.insert(0,'Password')

    
    e2 =Entry(f1,width=21,fg='black',border=0,bg='white')
    e2.config(font=('Microsoft YaHei UI Light',11, ))
    e2.bind("<FocusIn>", on_enter)
    e2.bind("<FocusOut>", on_leave)
    e2.insert(0,'Password')
    e2.place(x=30,y=130)

    Frame(f1,width=295,height=2,bg='black').place(x=25,y=157)

    def on_enter(e):
        e3.delete(0,'end')    
    def on_leave(e):
        if e3.get()=='':   
            e3.insert(0,'Confirm Password')

    
    e3 =Entry(f1,width=21,fg='black',border=0,bg='white')
    e3.config(font=('Microsoft YaHei UI Light',11, ))
    e3.bind("<FocusIn>", on_enter)
    e3.bind("<FocusOut>", on_leave)
    e3.insert(0,'Confirm Password')
    e3.place(x=30,y=130+70)

    Frame(f1,width=295,height=2,bg='black').place(x=25,y=157+70)    

    
    #Mechenism------------------------------------------------
    
    def signup_cmd():
        key=e1.get()
        value=e2.get()
        value2=e3.get()
        
        if value==value2:
            file=open('datasheet.txt','r+')
            d=file.read()
            r=ast.literal_eval(d)
            print(r)
            

            dict2={key:value}
            print(dict2)
            r.update(dict2)
            print(r)
            file.truncate(0)
            file.close()
            print(r)
            file=open('datasheet.txt','w')
            w=file.write(str(r))
             
            messagebox.showinfo("","     successfully signed up     ")
            
        else:
            messagebox.showwarning('try again', 'password should match ')


    #-------------------------------------------------------
    Button(f1,width=39,pady=7,text='Sign up',bg='#ff4f5a',fg='white',border=0,command=signup_cmd).place(x=35,y=204+60)
    l1=Label(f1,text="Already have an account?",fg="black",bg='white')
    l1.config(font=('Microsoft YaHei UI Light',9, ))
    l1.place(x=70,y=250+63)

    b2=Button(f1,width=6,text='Sign in',border=0,bg='white',fg='#ff4f5a',command=signin)
    b2.place(x=210,y=250+63)


if __name__ == "__main__":
    signin() #default screen
    w.mainloop()
