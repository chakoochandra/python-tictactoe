import random

#just a simple tictactoe game with calculated move
# by chandra [perdana1cell@gmail.com]

def DisplayBoard(board):
#
# the function accepts one parameter containing the board's current status
# and prints it out to the console
#
    count = len(board)
    print('+', '---------+' * count, sep='', end='\n')
    for i in range(count):
        print('|', '         |' * count, sep='', end='\n')
        print('|', '         |' * count, sep='', end='\n')
        print('|', end='')
        for j in range(count):
            #print('   ', board[i][j], '   |', sep='', end='')
            print('    ', '{message:{fill}<{width}}'.format(message=board[i][j], width=2, fill=' '), '   |', sep='', end='')
        print('', end='\n')
        print('|', '         |' * count, sep='', end='\n')
        print('|', '         |' * count, sep='', end='\n')
        print('+', '---------+' * count, sep='', end='\n')   

def EnterMove(board, sign = 'O'):
#
# the function accepts the board current status, asks the user about their move, 
# checks the input and updates the board according to the user's decision
#
    choose = 0;
    while GetCoordinates(board)[choose-1] not in MakeListOfFreeFields(board) or choose == 0:
        inp = input('\n\nGiliran Anda. Pilih kotak yang tersedia : ')
        if inp == '': continue
        try:
           choose = int(inp);
        except ValueError:
           choose = 0
    SetMove(board, sign, choose)
    
def MakeListOfFreeFields(board):
#
# the function browses the board and builds a list of all the free squares; 
# the list consists of tuples, while each tuple is a pair of row and column numbers
#
    free = []
    for coordinate in GetCoordinates(board):
        if isinstance(board[coordinate[0]][coordinate[1]], int):
            free.insert(len(free), (coordinate[0], coordinate[1]))
    return free
                
def VictoryFor(board, sign):
#
# the function analyzes the board status in order to check if 
# the player using 'O's or 'X's has won the game
#
    win = False
    coordinates = GetCoordinates(board);
    for w in MakeListOfWinPaths(board) :
        if [board[coordinates[w[j]-1][0]][coordinates[w[j]-1][1]] for j in range(len(board))].count(sign) == len(board) :
            win = True
            break
    return win

def DrawMove(board):
#
# the function draws the computer's move and updates the board
#   
    choose = GetCoordinates(board).index(CalculateComputerMove(board, 'X')) + 1    
    print('\n\nKomputer memilih kotak : ', choose)
    SetMove(board, 'X', choose)

def MakeListOfDiagonalPaths(board):
    count = len(board)
    diag = []
    diag.insert(len(diag), [i*count+i+1 for i in range(count)])
    diag.insert(len(diag), [(i+1)*count-i for i in range(count)])
    return diag
    
def MakeListOfWinPaths(board):
    count = len(board)
    wins = []
    for i in range(count):
        wins.insert(i, [count*i+j+1 for j in range(count)])
        wins.insert(len(wins), [count*j+i+1 for j in range(count)])	
    wins = wins + MakeListOfDiagonalPaths(board)
    random.shuffle(wins)
    return wins

def CalculateComputerMove(board, sign = 'X'):
    if sign == 'X': inverseSign = 'O'
    else: inverseSign = 'X'
    
    coordinates = GetCoordinates(board)
    diags = MakeListOfDiagonalPaths(board)
    wins = MakeListOfWinPaths(board)
    poolX, poolO, maxX, maxO = {}, {}, {}, {}
    for i in range(len(wins)):        
        path = [board[coordinates[wins[i][j]-1][0]][coordinates[wins[i][j]-1][1]] for j in range(len(board))]
        countX = path.count(sign)
        countO = path.count(inverseSign)

        #remove diagobal yang sudah ada piece(s) lawan
        if countO > 0 and wins[i] in diags:
            diags.remove(wins[i])
        #lanjut iterasi kalau path sudah mati
        if countX > 0 and countO > 0: continue
        #kumpulkan path yang berpeluang ditempati
        if countX > 0:
            poolX[i] = countX
            maxX[countX] = list(wins[i])
        #kumpulkan path lawan
        if countO > 0:
            poolO[i] = countO
            maxO[countO] = list(wins[i])
    
    fields = []
    #kalau pieces imbang atau menang, tambahkan piece di path sendiri
    if len(poolX)>0 and len(poolO)>0 and max(maxX) >= max(maxO):    
        fields = maxX[max(maxX)]        

        #optional : supaya komputer memilih path diagonal bila piece sedang seimbang
        for diag in diags:
            diagPath = [board[coordinates[diag[j]-1][0]][coordinates[diag[j]-1][1]] for j in range(len(board))]
            if diagPath.count(inverseSign) == 0 :
                fields = diag
    #kalau pieces lawan lebih baik, tambahkan piece di path lawan
    elif len(poolO)>0:
        fields = maxO[max(maxO)]
    
    target = []
    if len(fields)>0:
        #tempatkan piece di ujung minimal
        if isinstance(board[coordinates[min(fields)-1][0]][coordinates[min(fields)-1][1]], int):
            target.insert(0, min(fields))
        #atau boleh juga di ujung maksimal
        if isinstance(board[coordinates[max(fields)-1][0]][coordinates[max(fields)-1][1]], int):
            target.insert(0, max(fields))
        #kalau ujung2 sudah ditempati, tempatkan piece di antaranya
        if len(target) == 0:
            temp = []
            for field in fields:
                if isinstance(board[coordinates[field-1][0]][coordinates[field-1][1]], int):
                    temp.insert(0, field)
            target.insert(0, random.choice(temp))
    
    random.shuffle(target)
    if len(target) > 0: return coordinates[target[0] - 1]    
    return random.choice(MakeListOfFreeFields(board))
        
def GetCoordinates(board):
    coordinate = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            coordinate.insert(len(coordinate), (i, j))
    return coordinate

def SetMove(board, sign, pos):
    coordinates = GetCoordinates(board)
    board[coordinates[pos-1][0]][coordinates[pos-1][1]] = sign               
    DisplayBoard(board)
    
    if VictoryFor(board, sign) :
        if sign == 'X' : print('\n\nKamu kalah coyy!')
        else : print('\n\nMantabbb bro!')
        
        if input('\n\nMain lagi? (y/n) : ') == 'y' : play()
        else : print('\n\nKamu cupu deh!')
    elif len(MakeListOfFreeFields(board)) == 0 :
        print('\n\nTidak ada kotak tersedia. DRAW!')
        if input('\n\nMain lagi? (y/n) : ') == 'y' : play()
        else : print('\n\nKamu cupu deh!')
    elif sign == 'O' : DrawMove(board)
    else : EnterMove(board)
    
    
def play():
    count = 0
    while count < 3 or count > 9 or count % 2 == 0 :
        inp = input('Mau main berapa kotak? (3 / 5 / 7 / 9) ')
        if inp == '': continue
        try:
           count = int(inp)
        except ValueError:
           count = 0
        
    board = [[j+i*count for j in range(1, 1+count)] for i in range(count)];
    
    #computer 1st move
    init = count*count // 2 + 1
    print('\n\nKomputer memilih kotak : ', init)
    SetMove(board, 'X', init)

#HAVE FUN!
play()







