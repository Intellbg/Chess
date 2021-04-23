from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
path=os.path.dirname(os.path.abspath(__file__))

turn=1
playerMove=-1

root = Tk()
root.title("Chess")
#board=ttk.Frame(root, padding="5 5 5 5")



playerMoveToBoolean={
    1:True,
    -1:False
}

def reset():
    for i in range(8):
        for j in range(8):
            BoardGrid[i][j].tile['bg']='#fff'
            if i%2==0 and j%2!=0 or i%2!=0 and j%2==0:
                BoardGrid[i][j].tile["bg"]='#000'
            if BoardGrid[i][j].piece==None:
                BoardGrid[i][j].tile["command"]=reset
            elif  playerMoveToBoolean[playerMove]==BoardGrid[i][j].piece.player:
                BoardGrid[i][j].tile["command"]=BoardGrid[i][j].piece.move
            else:
                BoardGrid[i][j].tile["command"]=reset

def changeTurn():
    global turn
    global playerMove
    turn+=1
    playerMove*=-1
    reset()            
pixelVirtual = PhotoImage(width=1, height=1)       
class BoardTile:
    def coord(self):
        return self.tile.grid_info()['row'] ,self.tile.grid_info()['column']
    
    def create_button(self,i,j):    
        x=Button(root, bg='#fff',  activebackground='blue',width=100, height=100, image=pixelVirtual)
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
    def __init__(self,i,j,active,player,image):
        self.column=j
        self.row=i 
        self.name=self.setName()
        self.original =Image.open(image)
        resized = self.original.resize((100, 100),Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized)
        self.threat=False
        self.active=active  
        self.player=player #True: Black, Flase=White

    def print_piece(self):
        BoardGrid[self.row][self.column].tile['image']=self.image
        BoardGrid[self.row][self.column].tile['command']=self.move
       

    def remove_piece(self):
        BoardGrid[self.row][self.column].tile['image']=pixelVirtual
        BoardGrid[self.row][self.column].tile['command']=reset

    def confirm_move(self,i,j):
        BoardGrid[i][j].piece=BoardGrid[self.row][self.column].piece
        BoardGrid[self.row][self.column].piece.remove_piece()
        BoardGrid[self.row][self.column].piece=None
        self.row=i
        self.column=j
        BoardGrid[i][j].piece.print_piece()
        reset()
        changeTurn()
        imprimir_grid()

    def formatTile(self, i,j,color='green'):
        BoardGrid[i][j].tile['bg']=color
        BoardGrid[i][j].tile['command']= lambda i=i, j=j: self.confirm_move(i,j)
    
    def diagonal(self,pieceThreatList, leftToRight=False, limit=8):
        coef=1
        for x in range(2):
            newColumn=self.column
            newRow=self.row
            for i in range(limit):
                if leftToRight:
                    newColumn+=1*coef
                    newRow+=1*-coef
                else:
                    newColumn+=1*coef
                    newRow+=1*coef
                if (newColumn>=0 and newColumn<8) and (newRow>=0 and newRow<8):
                    try: 
                        tilePiece=BoardGrid[newRow][newColumn].piece
                        if tilePiece==None:
                            self.formatTile(newRow,newColumn)
                        else:
                            pieceThreatList.append([newRow,newColumn])
                            break
                    except: 
                        break
            coef=-1
        return pieceThreatList

    def cross(self,pieceThreatList, horizontal=False, limit=8):
        coef=1
        for x in range(2):
            newColumn=self.column
            newRow=self.row
            for i in range(limit):
                if horizontal:
                    newColumn+=1*coef
                else:
                    newRow+=1*coef
                if (newColumn>=0 and newColumn<8) and (newRow>=0 and newRow<8):
                    try: 
                        tilePiece=BoardGrid[newRow][newColumn].piece
                        if tilePiece==None:
                            self.formatTile(newRow,newColumn)
                        else:
                            pieceThreatList.append([newRow,newColumn])
                            break
                    except: 
                        break
            coef=-1
        return pieceThreatList

class Pawn(Piece):
    def setName(self):
        return"pawn"

    def move(self):
        reset()
        #Normal Move
        newRow=self.row+playerMove*1
        if BoardGrid[newRow][self.column].piece==None:
            self.formatTile(newRow,self.column)
        #capture 
        self.tilethreat()
        #1st Move
        if self.player and self.row==1:
            newRow=self.row+playerMove*2
        elif self.row==6: 
            newRow=self.row+playerMove*2
        else:
            pass
        
        if BoardGrid[newRow][self.column].piece==None:
            self.formatTile(newRow,self.column)

    def tilethreat(self):
        newRow=self.row+playerMove*1
        cols=[self.column+1,self.column-1]
        for newColumn in cols:
            if (newColumn>=0 and newColumn<8) and (newRow>=0 and newRow<8):
                try:
                    if BoardGrid[newRow][newColumn].piece.player!=BoardGrid[self.row][self.column].piece.player:
                        self.formatTile(newRow,newColumn,'red')
                except:
                    pass
    
class Rook(Piece):
    def setName(self):
        return"rook"

    def move(self):
        reset()
        pieceThreat=[]
        pieceThreat=self.cross(pieceThreat)
        pieceThreat=self.cross(pieceThreat,True)
        self.tilethreat(pieceThreat)

    def tilethreat(self, coords):
        for coord in coords:
            print(coord)
            try:
                if BoardGrid[coord[0]][coord[1]].piece.player!=BoardGrid[self.row][self.column].piece.player:
                    self.formatTile(coord[0],coord[1],'red')
            except:
                pass

class Bishop(Piece):
    def setName(self):
        return"bishop"

    def move(self):
        reset()
        pieceThreat=[]
        pieceThreat=self.diagonal(pieceThreat)
        pieceThreat=self.diagonal(pieceThreat,True)
        self.tilethreat(pieceThreat)

    def tilethreat(self, coords):
        for coord in coords:
            print(coord)
            try:
                if BoardGrid[coord[0]][coord[1]].piece.player!=BoardGrid[self.row][self.column].piece.player:
                    self.formatTile(coord[0],coord[1],'red')
            except:
                pass

class Knight(Piece):
    def setName(self):
        return"knight"

    def move(self):
        reset()
        pieceThreat=[]
        pieceThreat=self.l(pieceThreat)
        pieceThreat=self.l(pieceThreat,True)
        self.tilethreat(pieceThreat)

    def l(self,pieceThreatList, horizontal=False):      
        coef=1
        for x in range(2):
            if horizontal:
                newColumn=self.column+2*coef
            else:
                newRow=self.row+2*coef
            coef2=1
            for i in range(2):
                if horizontal:
                    newRow=self.row+coef2*1
                else:
                    newColumn=self.column+coef2*1
                if (newColumn>=0 and newColumn<8) and (newRow>=0 and newRow<8):
                    try: 
                        tilePiece=BoardGrid[newRow][newColumn].piece
                        if tilePiece==None:
                            self.formatTile(newRow,newColumn)
                        else:
                            pieceThreatList.append([newRow,newColumn])
                    except: 
                        pass
                coef2=-1
            coef=-1
        return pieceThreatList
    
    def tilethreat(self, coords):
        for coord in coords:
            print(coord)
            try:
                if BoardGrid[coord[0]][coord[1]].piece.player!=BoardGrid[self.row][self.column].piece.player:
                    self.formatTile(coord[0],coord[1],'red')
            except:
                pass

class Queen(Piece):
    def setName(self):
        return"queen"

    def move(self):
        reset()
        pieceThreat=[]
        pieceThreat=self.diagonal(pieceThreat)
        pieceThreat=self.diagonal(pieceThreat,True)
        pieceThreat=self.cross(pieceThreat)
        pieceThreat=self.cross(pieceThreat,True)
        self.tilethreat(pieceThreat)

    def tilethreat(self, coords):
        for coord in coords:
            print(coord)
            try:
                if BoardGrid[coord[0]][coord[1]].piece.player!=BoardGrid[self.row][self.column].piece.player:
                    self.formatTile(coord[0],coord[1],'red')
            except:
                pass

class King(Piece):
    def setName(self):
        return"King"

    def move(self):
        reset()
        pieceThreat=[]
        pieceThreat=self.diagonal(pieceThreat, limit=1)
        pieceThreat=self.diagonal(pieceThreat,True,limit=1)
        pieceThreat=self.cross(pieceThreat,limit=1)
        pieceThreat=self.cross(pieceThreat,True,limit=1)
        self.tilethreat(pieceThreat)

    def tilethreat(self, coords):
        for coord in coords:
            print(coord)
            try:
                if BoardGrid[coord[0]][coord[1]].piece.player!=BoardGrid[self.row][self.column].piece.player:
                    self.formatTile(coord[0],coord[1],'red')
            except:
                pass
for i in range(8):
    # Black Pawns
    BoardGrid[1][i].piece=Pawn(1,i,True,True,path+'/img/bpawn.png')
    # White Pawns
    BoardGrid[6][i].piece=Pawn(6,i,True,False,path+'/img/pawn.png')
 
BoardGrid[0][0].piece=Rook(0,0,True,True,path+'/img/brook.png')
BoardGrid[0][1].piece=Knight(0,1,True,True,path+'/img/bknight.png')
BoardGrid[0][2].piece=Bishop(0,2,True,True,path+'/img/bbishop.png')
BoardGrid[0][3].piece=Queen(0,3,True,True,path+'/img/bqueen.png')
BoardGrid[0][4].piece=King(0,4,True,True,path+'/img/bking.png')
BoardGrid[0][5].piece=Bishop(0,5,True,True,path+'/img/bbishop.png')
BoardGrid[0][6].piece=Knight(0,6,True,True,path+'/img/bknight.png')
BoardGrid[0][7].piece=Rook(0,7,True,True,path+'/img/brook.png')


BoardGrid[7][0].piece=Rook(7,0,True,False,path+'/img/rook.png')
BoardGrid[7][1].piece=Knight(7,1,True,False,path+'/img/knight.png')
BoardGrid[7][2].piece=Bishop(7,2,True,False,path+'/img/bishop.png')
BoardGrid[7][3].piece=Queen(7,3,True,False,path+'/img/queen.png')
BoardGrid[7][4].piece=King(7,4,True,False,path+'/img/king.png')
BoardGrid[7][5].piece=Bishop(7,5,True,False,path+'/img/bishop.png')
BoardGrid[7][6].piece=Knight(7,6,True,False,path+'/img/knight.png')
BoardGrid[7][7].piece=Rook(7,7,True,False,path+'/img/rook.png')

for i in range(8):
    for j in range(8):
        try:
            BoardGrid[i][j].piece.print_piece()
        except:
            pass
reset()
root.mainloop()