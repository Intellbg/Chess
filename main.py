from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Chess")
board=ttk.Frame(root, padding="5 5 5 5")
def reset():
    for i in range(8):
        for j in range(8):
            BoardGrid[i][j].tile['bg']='#fff'
            if BoardGrid[i][j].piece==None:
                BoardGrid[i][j].tile["command"]=reset
            else:
                BoardGrid[i][j].tile["command"]=BoardGrid[i][j].piece.move

            if i%2==0 and j%2!=0 or i%2!=0 and j%2==0:
                BoardGrid[i][j].tile["bg"]='#000'
            
class BoardTile:
    def coord(self):
        return self.tile.grid_info()['row'] ,self.tile.grid_info()['column']
    
    def create_button(self,i,j):    
        x=Button(root, bg='#fff',  activebackground='blue', fg='red')
        x.grid(column=j, row=i, sticky=(N,W,E,S))
        x['command']=reset
        if i%2==0 and j%2!=0 or i%2!=0 and j%2==0:
            x["bg"]='#000'
        return x

    def __init__(self, i, j):
        self.tile=self.create_button(i,j)
        self.piece=None
    
#board button layer 
BoardGrid=[]
for i in range(8):
    row=[]
    for j in range(8):
        row.append(BoardTile(i,j))
    BoardGrid.append(row)

def imprimir_grid():
    for i in range(8):
        for j in range(8):
            try:
                print(BoardGrid[i][j].piece.name+" ", end='')
            except:
                print("NONE ", end='')        
        print('\n')
    print("----------------------")
#Pieces 
class Piece():
    def __init__(self,i,j,name,active,player):
        self.column=j
        self.row=i 
        self.name=name
        self.threat=False
        self.active=active  
        self.player=player #True: Black, Flase=White

    def print_piece(self):
        BoardGrid[self.row][self.column].tile['text']=self.name
        BoardGrid[self.row][self.column].tile['command']=self.move

    def remove_piece(self):
        BoardGrid[self.row][self.column].tile['text']=""
        BoardGrid[self.row][self.column].tile['command']=reset

    def confirm_move(self,i,j):
        BoardGrid[i][j].piece=BoardGrid[self.row][self.column].piece
        BoardGrid[self.row][self.column].piece.remove_piece()
        BoardGrid[self.row][self.column].piece=None
        self.row=i
        self.column=j
        BoardGrid[i][j].piece.print_piece()
        reset()
        imprimir_grid()

class Pawn(Piece):
    def move(self):
        reset()
        #Normal Move
        if self.player:
            nc=self.row+1
        else: 
            nc=self.row-1

        if BoardGrid[nc][self.column].piece==None:
            BoardGrid[nc][self.column].tile['bg']="green"
            BoardGrid[nc][self.column].tile['command']=lambda: self.confirm_move(nc,self.column)
        #1st Move
            if self.player and self.row==1:
                n1=self.row+2
                BoardGrid[n1][self.column].tile['bg']="green"
                BoardGrid[n1][self.column].tile['command']=lambda: self.confirm_move(n1,self.column)
            elif self.row==6: 
                n1=self.row-2
                BoardGrid[n1][self.column].tile['bg']="green"
                BoardGrid[n1][self.column].tile['command']=lambda: self.confirm_move(n1,self.column)
        #eat 
        col1=self.column+1
        col2=self.column-1
        try:
            if BoardGrid[nc][col1].piece.player!=BoardGrid[self.row][self.column].piece.player:
                BoardGrid[nc][col1].tile['bg']="red"
                BoardGrid[nc][col1].tile['command']=lambda: self.confirm_move(nc,col1)
            if BoardGrid[nc][col2].piece.player!=BoardGrid[self.row][self.column].piece.player:
                BoardGrid[nc][col2].tile['bg']="red"
                BoardGrid[nc][col2].tile['command']=lambda: self.confirm_move(nc,col2)    
        except:
            pass
    
for i in range(8):
    # Black Pawns
    BoardGrid[1][i].piece=Pawn(1,i,"pawn",True,True)
    BoardGrid[1][i].piece.print_piece()
    # White Pawns
    BoardGrid[6][i].piece=Pawn(6,i,"pawn",True,False)
    BoardGrid[6][i].piece.print_piece()

root.mainloop()