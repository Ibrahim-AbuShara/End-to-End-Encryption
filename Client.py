# import all the required modules
import socket
import threading
from tkinter import *
from RSA import Rsa
from pathlib import Path

# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

PORT = 5000
SERVER = "192.168.1.8"
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"

# Create a new client socket
# and connect to the server
client = socket.socket(socket.AF_INET,
                    socket.SOCK_STREAM)
client.connect(ADDRESS)


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self):
        self.x = Rsa()
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
        
        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")

        self.login.geometry("441x437")
        self.login.configure(bg = "#FFFFFF")

        self.canvas = Canvas(
            self.login,
            bg = "#FFFFFF",
            height = 437,
            width = 441,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            216.0,
            143.0,
            image=self.image_image_1
        )
        # create a Label
        self.pls = self.canvas.create_text(
            82.0,
            326.0,
            anchor="nw",
            text="Name",
            fill="#000000",
            font=("Inter", 16 * -1)
        )
        
        # create a entry box for
        # tyoing the message
        self.entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(
            220.5,
            336.0,
            image=self.entry_image_1
        )

        self.entryName = Entry(
            self.login,
            bd=0,
            bg="#FFFFFF",
            highlightthickness=0
        )
        
        self.entryName.place(
            x=131.0,
            y=320.0,
            width=179.0,
            height=30.0
        )
        
        # create a Continue Button
        # along with action
        button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
        self.go = Button(
            self.login,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.goAhead(self.entryName.get()),
            relief="flat"
        )
        
        self.go.place(
            x=131.0,
            y=381.0,
            width=179.0,
            height=38.0
        )

        self.login.resizable(False, False)
        self.Window.mainloop()
        # self.msg = self.x.public
        self.sendMessage()

    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)
        
        # the thread to receive messages
        rcv = threading.Thread(target=self.receive)
        rcv.start()

    # The main layout of the chat
    def layout(self,name):
    
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width = False,
                            height = False)
        self.Window.configure(width = 470,
                            height = 550,
                            bg = "#17202A")
        self.labelHead = Label(self.Window,
                            bg = "#17202A",
                            fg = "#EAECEE",
                            text = self.name ,
                            font = "Helvetica 13 bold",
                            pady = 5)
        
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window,
                        width = 450,
                        bg = "#ABB2B9")
        
        self.line.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.012)
        
        self.textCons = Text(self.Window,
                            width = 20,
                            height = 2,
                            bg = "#17202A",
                            fg = "#EAECEE",
                            font = "Helvetica 14",
                            padx = 5,
                            pady = 5)
        
        self.textCons.place(relheight = 0.745,
                            relwidth = 1,
                            rely = 0.08)
        
        self.labelBottom = Label(self.Window,
                                bg = "#ABB2B9",
                                height = 80)
        
        self.labelBottom.place(relwidth = 1,
                            rely = 0.825)
        
        self.entryMsg = Entry(self.labelBottom,
                            bg = "#2C3E50",
                            fg = "#EAECEE",
                            font = "Helvetica 13")
        
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth = 0.74,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
        
        self.entryMsg.focus()
        
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text = "Send",
                                font = "Helvetica 10 bold",
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton(self.entryMsg.get()))
        
        self.buttonMsg.place(relx = 0.77,
                            rely = 0.008,
                            relheight = 0.06,
                            relwidth = 0.22)
        
        # self.Window.bind('<Return>',lambda : self.sendButton)

        self.textCons.config(cursor = "arrow")
        
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
        
        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight = 1,
                        relx = 0.974)
        
        scrollbar.config(command = self.textCons.yview)
        
        self.textCons.config(state = DISABLED)
        
     
    # function to basically start the thread for sending messages
    def sendButton(self,msg):
        self.textCons.config(state = DISABLED)
        self.msg=msg
        self.entryMsg.delete(0, END)
        snd= threading.Thread(target = self.sendMessage)
        snd.start()
    #function to the public_key received as string from server to a tuple     
    def convert_str_tup(self):
        char_to_replace = {'(': '',
                          ')': ''}
        for key, value in char_to_replace.items():
            self.p_key = self.p_key.replace(key, value)
        self.p_key = tuple(map(int, self.p_key.split(', ')))
        
    # function to receive messages
    def receive(self):
        while True:
            # try:
                message = client.recv(10240).decode(FORMAT)
                # if the messages from the server is NAME send the client's name
                if message == 'INFO':
                    info=self.name+'+'+str(self.x.public)
                    client.send(info.encode(FORMAT))
                    self.p_key=client.recv(10240).decode(FORMAT)
                    self.convert_str_tup()                 
                
                else:
                    # insert messages to text box
                    self.textCons.config(state = NORMAL)
                    message = self.x.decrypt(message)
                    self.textCons.insert(END,
                                        message+"\n\n")
                    
                    self.textCons.config(state = DISABLED)
                    self.textCons.see(END)
            # except:
            #     # an error will be printed on the command line or console if there's an error
            #     print("An error occured!")
            #     client.close()
            #     break
        
    # function to send messages
    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}") 
            self.textCons.config(state = NORMAL)
            self.textCons.insert(END,
                                message+"\n\n")
            
            self.msg = self.x.encrypt(message,self.p_key)
            mesg = ""
            for i in self.msg:
                mesg += str(i)
                mesg += "\/"
            client.send(mesg.encode(FORMAT))
            break

# create a GUI class object
g = GUI()
