#when running the file from console, supply a -e arguemnt at the end to disable image not updating warnings
from appJar import gui
from copy import deepcopy
import random
import MoveChecker
import MoveFinder
import PointsTracker
app = gui()
turn = 'Red'
ai = False
MoveChecker.boardState = MoveChecker.reset()
def swapScreen(btn):
    if btn == 'Start Game':
        if app.getCheckBox('Enable machine learning'):
            print ('Machine learning not yet available')
        global ai
        if app.getRadioButton('gameType') == 'Play against AI':
            if random.randint(0, 1) == 0:
                ai = 'Red'
                makeMove('ai')
            else:
                ai = 'Yellow'
        else:
            if app.getCheckBox('Enable machine learning'):
                print ('Playing with machine learning enabled between two players is a beta concept. Use of this may significantly disrupt the AI.')
            ai = False
        app.prevFrame('screens')
        app.showToolbar()
    elif btn == 'Back to menu':
        app.nextFrame('screens')
        ai = False
        resetBoardImage()
        app.hideToolbar()
def makeMove(btn):
    global turn
    global ai
    if ai == turn:
        column = MoveFinder.bestMove(turn)
        moveMade = MoveChecker.moveChecker(column, turn, MoveChecker.boardState, False)
    else:
        column = int(app.getRadioButton(btn)[3:])
        moveMade = MoveChecker.moveChecker(column, turn, MoveChecker.boardState)
    if moveMade != 'none':
        if ai != turn:
            tempUndo = [deepcopy(MoveChecker.boardState), deepcopy(PointsTracker.points), deepcopy(PointsTracker.strings), deepcopy(PointsTracker.potCon4), deepcopy(PointsTracker.activePots), deepcopy(PointsTracker.traps)]
        MoveChecker.boardState[moveMade[0]][moveMade[1]] = turn
        if ai != turn:
            if PointsTracker.undoCount < -1:
                PointsTracker.undoCount += 1
                if PointsTracker.undoLog[PointsTracker.undoCount + 1][0] != MoveChecker.boardState:
                    if PointsTracker.undoCount != -1:
                        PointsTracker.undoLog = PointsTracker.undoLog[:PointsTracker.undoCount + 1]
                        PointsTracker.undoCount = -1
            else:
                PointsTracker.undoLog.append(tempUndo)
            if len(PointsTracker.undoLog) > 5:
                del PointsTracker.undoLog[0]
        app.setImage('p'+str(moveMade[0])+','+str(moveMade[1]), 'Con4'+turn+'Tile.gif')
        if ai == turn:
            ifAI = True
        else:
            ifAI = False
        points = PointsTracker.getPoints(moveMade, turn, points = PointsTracker.points, stringsTemp = PointsTracker.strings, ai = ifAI, boardState = deepcopy(MoveChecker.boardState), weights = PointsTracker.weights, potCon4 = PointsTracker.potCon4, activePots = PointsTracker.activePots, traps = PointsTracker.traps)
        PointsTracker.potCon4 = points[3]
        PointsTracker.strings = points[2]
        PointsTracker.points = points[0]
        PointsTracker.activePots = points[4]
        PointsTracker.traps = points[5]
        print (points[0])
        app.setMeter('scoreRatio', points[1]['Red'] * 100)
#        if ai != False:
#            with open('gameLog.txt', 'a') as f:
#                f.write(turn+'\n')
#                f.write('-'+ai+' ai\n')
#                f.write('-'+str(moveMade)+'\n')
#                f.write('-'+str(points[0])+'-'+str(points[1])+'\n')
        if turn == 'Red':
            turn = 'Yellow'
        else:
            turn = 'Red'
        app.setFrameBg('board', '#00a2e8')
    app.setRadioButton('selection', 'hiddenRadio', False)
    if ai == turn:
        makeMove('ai')
def redo(btn):
    global turn
    global ai
    if PointsTracker.undoCount < -2:
        if ai == False:
            if turn == 'Red':
                turn = 'Yellow'
            else:
                turn = 'Red'
        PointsTracker.undoCount += 1
        undoLog = deepcopy(PointsTracker.undoLog[PointsTracker.undoCount + 1])
        for row in range(len(MoveChecker.boardState)):
            for tile in range(len(MoveChecker.boardState[0])):
                if MoveChecker.boardState[row][tile] != PointsTracker.undoLog[PointsTracker.undoCount + 1][0][row][tile]:
                    app.setImage('p'+str(row)+','+str(tile), 'Con4'+str(PointsTracker.undoLog[PointsTracker.undoCount + 1][0][row][tile])+'Tile.gif')
        app.setFrameBg('board', '#00a2e8')
        MoveChecker.boardState = undoLog[0]
        PointsTracker.points = undoLog[1]
        PointsTracker.strings = undoLog[2]
        PointsTracker.potCon4 = undoLog[3]
        PointsTracker.activePots = undoLog[4]
        PointsTracker.traps = undoLog[5]
def undo(btn):
    global turn
    global ai
    if abs(PointsTracker.undoCount) <= len(PointsTracker.undoLog):
        if ai == False:
            if turn == 'Red':
                turn = 'Yellow'
            else:
                turn = 'Red'
        for row in range(len(MoveChecker.boardState)):
            for tile in range(len(MoveChecker.boardState[0])):
                if MoveChecker.boardState[row][tile] != PointsTracker.undoLog[PointsTracker.undoCount][0][row][tile]:
                    app.setImage('p'+str(row)+','+str(tile), 'Con4EmptyTile.gif')
        app.setFrameBg('board', '#00a2e8')
        undoLog = deepcopy(PointsTracker.undoLog[PointsTracker.undoCount])
        MoveChecker.boardState = undoLog[0]
        PointsTracker.points = undoLog[1]
        PointsTracker.strings = undoLog[2]
        PointsTracker.potCon4 = undoLog[3]
        PointsTracker.activePots = undoLog[4]
        PointsTracker.traps = undoLog[5]
        PointsTracker.undoCount -= 1
def resetBoardImage():
    for row in range(6):
        for col in range(7):
            app.setImage('p'+str(row)+','+str(col), 'Con4EmptyTile.gif')
    app.setFrameBg('board', '#00a2e8')
    app.setMeter('scoreRatio', 0.0)
    MoveChecker.boardState = MoveChecker.reset()
    PointsTracker.weights = PointsTracker.getWeights()
    PointsTracker.points = {'Red': 0, 'Yellow': 0}
    PointsTracker.strings = {'Red': [[],[]], 'Yellow': [[],[]]}
    PointsTracker.potCon4 = {'Red': [], 'Yellow': []}
    PointsTracker.activePots = {'Red': [], 'Yellow': []}
    PointsTracker.traps = {'Red': [], 'Yellow': []}
    PointsTracker.undoLog = []
    PointsTracker.undoCount = -1
    global ai
    global turn
    turn = 'Red'
    if ai:
        if random.randint(0, 1) == 0:
            ai = 'Red'
            makeMove('ai')
        else:
            ai = 'Yellow'
def init():
    PointsTracker.weights = PointsTracker.getWeights()
    app.startFrameStack('screens')
    #>
    app.startFrame('stackFiller')
    #>>
    app.startFrameStack('gameFrames')
    #>>>
    app.startFrame('hiddenFrame')
    #>>>>
    app.addRadioButton('selection','hiddenRadio')
    app.stopFrame() #hiddenFrame
    #<<<<
    app.startFrame('gameScreen')
    app.addToolbarButton('Back to menu', swapScreen)
    app.addToolbarButton('Reset board', resetBoardImage)
    app.addToolbarButton('Undo', undo)
    app.addToolbarButton('Redo', redo)
    app.hideToolbar()
    #>>>>
    app.startFrame('board', rowspan=6, colspan=7)
    #>>>>>
    app.setBg('#00a2e8')
    for col in range(7):
        for row in range(6):
            app.addImage('p'+str(row)+','+str(col), 'Con4EmptyTile.gif', row, col)
    app.stopFrame() #board
    #<<<<<
    app.setStretch('column')
    app.startFrame('buttonRow', 7, rowspan = 1)
    #>>>>>
    for col in range(7):
        app.startFrame('button'+str(col), 1, col)
        #>>>>>>
        app.addRadioButton('selection', 'col'+str(col))
        app.stopFrame() #button
        #<<<<<<
    app.setRadioButtonChangeFunction('selection', makeMove)
    app.stopFrame() #buttonRow
    #<<<<<
    app.startFrame('meter', row = 8, colspan = 7)
    #>>>>>
    app.addSplitMeter('scoreRatio')
    app.setMeterFill('scoreRatio', ['#FF0000','#FFFF00'])
    app.stopFrame() #meter
    app.stopFrame() #gameScreen
    #<<<<
    app.stopFrameStack() #gameFrames
    #<<<
    app.stopFrame() #stackFiller
    #<<
    app.startFrame('Game type')
    #>>
    app.addRadioButton('gameType','Play against AI')
    app.addRadioButton('gameType','Play against another player')
    app.addCheckBox('Enable machine learning')
    app.addButton('Start Game', swapScreen)
    app.setButtonBg('Start Game', 'green')
    app.setButtonFg('Start Game', 'white')
    app.stopFrame() #game type
    #<<
    app.stopFrameStack() #screens
    #<
init()
app.go()