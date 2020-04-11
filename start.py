import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import sys

try:
    email_user = sys.argv[1]
    email_password = sys.argv[2]
    try:
        server = sys.argv[3]
        values = server.split(":")
        mailserver = values[0]
        port = values[1]
    except:
        mailserver = 'smtp.gmail.com'
        port = 587
except:
    print('Usage: python start.py E-mail Password\n')
    print('OR\n')
    print('python start.py E-mail Password mailserver:port\n')
    sys.exit()

class SendMail:

    def __init__(self, master):
        
        master.title('Send Email')
        master.resizable(False, False)
        master.configure(background = '#bbb')
        
        self.style = ttk.Style()
        self.style.configure('TFrame', background = '#bbb')
        self.style.configure('TButton', background = '#bbb')
        self.style.configure('TLabel', background = '#bbb', font = ('Arial', 11))
        self.style.configure('Header.TLabel', font = ('Arial', 18, 'bold'))      

        self.frame_header = ttk.Frame(master)
        self.frame_header.pack()


        self.logo = PhotoImage(file = "logo.ppm")
        ttk.Label(self.frame_header, image = self.logo).grid(row = 0, column = 0)
        ttk.Label(self.frame_header, text = 'Send Email !', style = 'Header.TLabel').grid(row = 0, column = 1)
        #ttk.Label(self.frame_header, wraplength = 300,text = ("https://github.com/byRo0t96\nv.0.0.1")).grid(row = 1, column = 1)
        
        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()

        ttk.Label(self.frame_content, text = 'Subject:').grid(row = 0, column = 0, padx = 5, sticky = 'sw')
        ttk.Label(self.frame_content, text = 'To:').grid(row = 0, column = 1, padx = 5, sticky = 'sw')
        ttk.Label(self.frame_content, text = 'Message:').grid(row = 2, column = 0, padx = 5, sticky = 'sw')
        
        self.entry_name = ttk.Entry(self.frame_content, width = 24, font = ('Arial', 12))
        self.entry_email = ttk.Entry(self.frame_content, width = 24, font = ('Arial', 12))
        self.text_comments = Text(self.frame_content, width = 50, height = 10, font = ('Arial', 12))
        
        self.entry_name.grid(row = 1, column = 0, padx = 5)
        self.entry_email.grid(row = 1, column = 1, padx = 5)
        self.text_comments.grid(row = 3, column = 0, columnspan = 2, padx = 5)

        ttk.Button(self.frame_content, text = 'File',
                   command = self.filedialog).grid(row = 4, column = 0, padx = 5, pady = 5, sticky = 'w')
        ttk.Button(self.frame_content, text = 'About',
                   command = self.about).grid(row = 5, column = 0, padx = 5, pady = 5, sticky = 'w')
        ttk.Button(self.frame_content, text = 'Submit',
                   command = self.submit).grid(row = 5, column = 0, padx = 5, pady = 5, sticky = 'e')
        ttk.Button(self.frame_content, text = 'Clear',
                   command = self.clear).grid(row = 5, column = 1, padx = 5, pady = 5, sticky = 'w')
        ttk.Button(self.frame_content, text = 'Exit',
                   command = master.destroy).grid(row = 5, column = 1, padx = 5, pady = 5, sticky = 'e')

    def about(self):
        messagebox.showinfo(title = 'Send Email', message = 'Programed by Ro0t96\nVersion: 0.0.1\n')

    def filedialog(self):
        self.filenameg = filedialog.askopenfilename(initialdir = "/", title = "select")
        self.labelfilenameg = ttk.Label(self.frame_content,text = "")
        self.labelfilenameg.grid(column = 1, row = 4, sticky = 'w')
        self.labelfilenameg.configure(text = self.filenameg)

    def submit(self):
        subject = self.entry_name.get()
        email_send = self.entry_email.get()
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_send
        msg['Subject'] = subject
        body = self.text_comments.get(1.0, 'end')
        msg.attach(MIMEText(body,'plain'))

        try:
            filename = self.filenameg
        except:
            var_exists = False
        else:
            var_exists = True
            attachment = open(filename,'rb')
            part = MIMEBase('application','octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',"attachment; filename= "+filename)
            msg.attach(part)


        text = msg.as_string()
        server = smtplib.SMTP(mailserver,port)
        server.starttls()
        server.login(email_user,email_password)

        server.sendmail(email_user,email_send,text)
        server.quit()

        print('subject: {}'.format(self.entry_name.get()))
        print('recipient email: {}'.format(self.entry_email.get()))
        if var_exists == False:
            print "no attachment"
        else:
            print('filename: {}'.format(self.filenameg))
        print('message: {}'.format(self.text_comments.get(1.0, 'end')))
        self.clear()
        messagebox.showinfo(title = 'Send Email', message = 'Email Submitted!')
    
    def clear(self):
        self.entry_name.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        #self.labelfilenameg.delete(0, 'end')
        self.text_comments.delete(1.0, 'end')
        #self.filenameg.delete(0, 'end')
         
def main():            
    
    root = Tk()
    sendmail = SendMail(root)
    root.mainloop()
    
if __name__ == "__main__": main()
