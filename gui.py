
import SQLborrow
import tkinter as tk


root = tk.Tk()

def eqBorrow(event):
    print('borrow')
    SQLborrow.connectDB()
    SQLborrow.checkOut()
    
def eqReturn(event):
    print('return')
    SQLborrow.connectDB()
    SQLborrow.checkIn()

topFrame = tk.Frame(root)
topFrame.pack()
bottomFrame = tk.Frame(root)
bottomFrame.pack(side='bottom')

btnBorrow = tk.Button(topFrame, text='Hent ut', fg='green')
btnReturn = tk.Button(topFrame, text='Lever tilbake', fg='red')

btnBorrow.bind("<Button-1>", eqBorrow)
btnReturn.bind("<Button-1>", eqReturn)

btnBorrow.pack()
btnReturn.pack(side='right')


# one = Label(root, text='One', bg='red', fg='white')
# one.pack()
# 
# two = Label(root, text='Two', bg='green', fg='black')
# two.pack(fill=X)
# 
# tre = Label(root, text='Tre', bg='blue', fg='white')
# tre.pack(side=LEFT, fill=Y)

# topFrame = Frame(root)
# topFrame.pack()
# bottomFrame = Frame(root)
# bottomFrame.pack(side=BOTTOM)
# 
# button1 = Button(topFrame,text='Button1', fg='red')
# button2 = Button(topFrame, text='Button2', fg='blue')
# button3 = Button(topFrame, text='Button3', fg='purple')
# button4 = Button(bottomFrame, text='Button4', fg='green')
# 
# button1.pack(side='left')
# button2.pack(side='left')
# button3.pack(side='left')
# button4.pack(side='bottom')

root.mainloop()