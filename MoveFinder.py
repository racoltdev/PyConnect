from copy import deepcopy
import MoveChecker
import PointsTracker
def nextTurnPoints(color, col, board, pointsT, stringsT, potCon4, activePots, traps):
    points = []
    moveMade = MoveChecker.moveChecker(col, color, board, False)
    if moveMade != 'none':
        boardTemp = deepcopy(board)
        boardTemp[moveMade[0]][moveMade[1]] = color
        getPoints = PointsTracker.getPoints(moveMade, color, points = pointsT, stringsTemp = stringsT, ai = True, boardState = deepcopy(boardTemp), weights = PointsTracker.weights, potCon4 = potCon4, activePots = activePots, traps = traps)
        points.append(getPoints[0])
        points.append(boardTemp)
        points.append(getPoints[2])
        points.append(getPoints[1])
        points.append(getPoints[3])
        points.append(getPoints[4])
        points.append(getPoints[5])
    else:
        points = 'none'
    return points
def bestMove(color):
    if MoveChecker.boardState[5][3] == 0:
        return 3
    board = deepcopy(MoveChecker.boardState)
    if color == 'Red':
        oppColor = 'Yellow'
    else:
        oppColor = 'Red'
    mins = []
    maxm = [-1, -1]
    for col in range(7):
        tempPoints = nextTurnPoints(color, col, board, deepcopy(PointsTracker.points), deepcopy(PointsTracker.strings), deepcopy(PointsTracker.potCon4), deepcopy(PointsTracker.activePots), deepcopy(PointsTracker.traps))
        if tempPoints != 'none':
            if tempPoints[0][color] == 999999:
                mins.append([0, col, 0, 999999])
            else:
                minm = [0, 0, 100, 0]
                for nextCol in range(7):
                    oppPoints = nextTurnPoints(oppColor, nextCol, deepcopy(tempPoints[1]), deepcopy(tempPoints[0]), deepcopy(tempPoints[2]), deepcopy(tempPoints[4]), deepcopy(tempPoints[5]), deepcopy(tempPoints[6]))
                    if oppPoints != 'none':
                        if oppPoints[0][color] == 0:
                            if oppPoints[0][oppColor] > minm[0]: 
                                minm[0] = oppPoints[0][oppColor]
                                minm[1] = col
                                minm[2] = int(oppPoints[3][color] * 100)
                                minm[3] = oppPoints[0][color]
                        elif int(oppPoints[3][color] * 100) <= minm[2]:
                            minm[0] = oppPoints[0][oppColor]
                            minm[1] = col
                            minm[2] = int(oppPoints[3][color] * 100)
                            minm[3] = oppPoints[0][color]
                mins.append(minm)
    for ratio in mins:
        if ratio[3] == 999999:
            maxm = [0, ratio[1]]
            break
        if (ratio[2] >= maxm[0]) and (ratio[3] != 0):
            maxm = [ratio[2], ratio[1]]
    if maxm[1] == -1:
        print ('Stale game')
        return 'none'
    else:
        return maxm[1]