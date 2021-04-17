from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Chess")

board=ttk.Frame(root, padding="5 5 5 5")

BoardGrid=[]
for i in range(8):
    row=[]
    for j in range(8):
        cell=Button(root, bg='#fff',  activebackground='blue')
        cell.grid(column=j, row=i, sticky=(N,W,E,S))
        if i%2==0 and j%2!=0 or i%2!=0 and j%2==0:
            cell["bg"]='#000'
        row.append(cell)
        
    BoardGrid.append(row)

root.mainloop()