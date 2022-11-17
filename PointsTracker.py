from copy import deepcopy
import math
weights = {}
points = {'Red': 0, 'Yellow': 0}
strings = {'Red': [[],[]], 'Yellow': [[],[]]}
potCon4 = {'Red': [], 'Yellow': []}
activePots = {'Red': [], 'Yellow': []}
traps = {'Red': [], 'Yellow': []}
undoLog = []
undoCount = -1
undoLogReference = ['boardState', 'points', 'strings', 'potCon4', 'activePots', 'traps']
def stringCheck(stringsTemp, newStrings, color, weights):
    points = 0
    for newString in newStrings:
        for stringLen in range(len(stringsTemp[color])):
            for string in stringsTemp[color][stringLen]:
                delString = True
                for tile in string:
                    if tile not in newString:
                        delString = False
                if delString:
                    points -= int(weights[len(string) - 2])
                    stringsTemp[color][stringLen].remove(string)
        stringsTemp[color][len(newString) - 2].append(newString)
        points += int(weights[len(newString) - 2])
    stringsOut = [points, stringsTemp]
    return stringsOut
def getPoints(moveMade, color, points, stringsTemp, ai, boardState, weights, potCon4, activePots, traps):
    newStrings = getStrings(moveMade, color, boardState)
    newPotCon4 = getPotCon4(newStrings[1], color, deepcopy(boardState), deepcopy(potCon4))
    win = newStrings[0]['win']
    newStrings = newStrings[0]['other']
    stringWeights = [weights['string2'], weights['string3']]
    midWeights = [weights['mid0'], weights['mid1'], weights['mid2'], weights['mid3']]
    strings = stringCheck(stringsTemp, newStrings, color, stringWeights)
    points[color] += strings[0]
    colPoints = int(midWeights[abs(moveMade[1] - 3)])
    points[color] += colPoints
    points = getPotCon4Points(potCon4, newPotCon4, int(weights['potCon4']), points)
    activePots = getActivePots(newPotCon4, boardState, activePots, int(weights['activePot']), points, color)
    points = activePots[0]
    activePots = activePots[1]
    doubleTraps = getDoubleTraps(newPotCon4, int(weights['doubleTrap']), traps, points, color)
    points = doubleTraps[0]
    traps = doubleTraps[1]
    points = trapStack(traps, color, moveMade, int(weights['trapStack']), points)
    points['Red'] += shakeItUp(moveMade, color, boardState)
    if win != []:
        if color == 'Red':
            pointsRatio = {'Red': 1.0, 'Yellow': 0.0}
            points = {'Red': 999999, 'Yellow': 0}
        else:
            pointsRatio = {'Red': 0.0, 'Yellow': 1.0}
            points = {'Red': 0, 'Yellow': 999999}
    elif (points['Red'] == 0) or (points['Yellow'] == 0):
        pointsRatio = {'Red': 0.5, 'Yellow': 0.5}
    else:
        tempPoints = {'Red': points['Red'], 'Yellow': points['Yellow']}
        totPoints = tempPoints['Red'] + tempPoints['Yellow']
        pointsRatio = {'Red': tempPoints['Red'] / totPoints, 'Yellow': tempPoints['Yellow'] / totPoints}
    pointsTypes = [points, pointsRatio, strings[1], newPotCon4, activePots, traps]
    return pointsTypes
def getWeights():
    with open('weights.txt', 'r') as f:
        for line in f:
            pastKey = False
            key = ''
            value = ''
            for char in line:
                if (char != ':') and (pastKey == False):
                    key += char
                elif char != ':':
                    value += char
                else:
                    pastKey = True
            weights[key] = value[0:-1]
    return weights
def shakeItUp(moveMade, turn, boardState):
    redPoints = 0
    if turn == 'Red':
        if moveMade == [0, 3]:
            redPoints -= 2
    return redPoints
def trapStack(traps, color, moveMade, weight, points):
    redCols = []
    for trap in traps['Red']:
        if trap[0][1] not in redCols:
            redCols.append(trap[0][1])
    for trap in redCols:
        if moveMade[1] == trap:
            if color == 'Red':
                points[color] += weight
            else:
                points[color] -= weight
    yellowCols = []
    for trap in traps['Yellow']:
        if trap[0][1] not in yellowCols:
            yellowCols.append(trap[0][1])
    for trap in yellowCols:
        if moveMade[1] == trap:
            if color == 'Yellow':
                points[color] += weight
            else:
                points[color] -= weight
    return points
def getDoubleTraps(pots, weight, traps, points, color):
    points['Red'] -= len(traps['Red']) * weight
    points['Yellow'] -= len(traps['Yellow']) * weight
    traps = {'Red': [], 'Yellow': []}
    for tile in pots['Red']:
        for otherTile in pots['Red'][pots['Red'].index(tile):]:
            if ((tile[0] == otherTile[0] + 1) or (tile[0] + 1 == otherTile[0])) and (tile[1] == otherTile[1]):
                traps['Red'].append([tile, otherTile])
                points['Red'] += weight
    for tile in pots['Yellow']:
        for otherTile in pots['Yellow'][pots['Yellow'].index(tile):]:
            if ((tile[0] == otherTile[0] + 1) or (tile[0] + 1 == otherTile[0])) and (tile[1] == otherTile[1]):
                traps['Yellow'].append([tile, otherTile])
                points['Yellow'] += weight
    return [points, traps]
def getActivePots(pots, board, activePots, weight, points, turn):
    if len(activePots['Red']) > 1:
        points['Red'] -= weight
    if len(activePots['Yellow']) > 1:
        points['Yellow'] -= weight
    activePots = {'Red': [], 'Yellow': []}
    for pot in pots['Red']:
        if pot[0] == 5:
            activePots['Red'].append(pot)
        elif board[pot[0] + 1][pot[1]] != 0:
            activePots['Red'].append(pot)
    for pot in pots['Yellow']:
        if pot[0] == 5:
            activePots['Yellow'].append(pot)
        elif board[pot[0] + 1][pot[1]] != 0:
            activePots['Yellow'].append(pot)
    if len(activePots['Red']) > 1:
        points['Red'] += weight
    if (len(activePots['Red']) == 1) and (turn == 'Red'):
        points['Red'] -= 5
    if len(activePots['Yellow']) > 1:
        points['Yellow'] += weight
    if (len(activePots['Yellow']) == 1) and (turn == 'Yellow'):
        points['Yellow'] -= 5
    return [points, activePots]
def getStrings(moveMade, color, boardState):
    win = False
    highLightWin = []
    emptyPot = []
    #NS Check
    rowCheck = moveMade[0]
    if moveMade[0] > 0:
        emptyPot.append([moveMade[0]-1, moveMade[1]])
    SFail = False
    NSString = 0
    highLightNS = []
    while (rowCheck < 6) and (not SFail) and (not win):
        if boardState[rowCheck][moveMade[1]] == color:
            NSString += 1
            checkHist = (rowCheck, moveMade[1])
            highLightNS.append(checkHist)
            rowCheck += 1
        else:
            SFail = True
        if NSString == 4:
            win = True
            highLightWin = highLightNS
    #EW Check
    colCheck = moveMade[1]
    WFail = False
    EWString = 0
    highLightEW = []
    while (colCheck >= 0) and (not WFail) and (not win):
        if boardState[moveMade[0]][colCheck] == color:
            colCheck -= 1
        else:
            if boardState[moveMade[0]][colCheck] == 0:
                emptyPot.append([moveMade[0], colCheck])
            WFail = True
    colCheck += 1
    EFail = False
    while (colCheck < 7) and (not EFail) and (not win):
        if boardState[moveMade[0]][colCheck] == color:
            checkHist = (moveMade[0], colCheck)
            highLightEW.append(checkHist)
            EWString += 1
            colCheck += 1
        else:
            if boardState[moveMade[0]][colCheck] == 0:
                emptyPot.append([moveMade[0], colCheck])
            EFail = True
        if EWString == 4:
            win = True
            highLightWin = highLightEW
    #posX Check
    rowCheck = moveMade[0]
    colCheck = moveMade[1]
    posXString = 0
    posXFail = False
    highLightPosX = []
    while (rowCheck < 6) and (colCheck >= 0) and (not posXFail) and (not win):
        if boardState[rowCheck][colCheck] == color:
            rowCheck += 1
            colCheck -= 1
        else:
            if boardState[rowCheck][colCheck] == 0:
                emptyPot.append([rowCheck, colCheck])
            posXFail = True
    rowCheck -= 1
    colCheck += 1
    posXFail = False
    while (rowCheck >= 0) and (colCheck < 7) and (not posXFail) and (not win):
        if boardState[rowCheck][colCheck] == color:
            checkHist = (rowCheck, colCheck)
            highLightPosX.append(checkHist)
            posXString += 1
            rowCheck -= 1
            colCheck += 1
        else:
            if boardState[rowCheck][colCheck] == 0:
                emptyPot.append([rowCheck, colCheck])
            posXFail = True
        if posXString == 4:
            win = True
            highLightWin = highLightPosX
    #negX Check
    rowCheck = moveMade[0]
    colCheck = moveMade[1]
    negXFail = False
    negXString = 0
    highLightNegX = []
    while (rowCheck >= 0) and (colCheck >= 0) and (not negXFail) and (not win):
        if boardState[rowCheck][colCheck] == color:
            rowCheck -= 1
            colCheck -= 1
        else:
            if boardState[rowCheck][colCheck] == 0:
                emptyPot.append([rowCheck, colCheck])
            negXFail = True
    rowCheck += 1
    colCheck += 1
    negXFail = False
    while (rowCheck < 6) and (colCheck < 7) and (not negXFail) and (not win):
        if boardState[rowCheck][colCheck] == color:
            checkHist = (rowCheck, colCheck)
            highLightNegX.append(checkHist)
            rowCheck += 1
            colCheck += 1
            negXString += 1
        else:
            if boardState[rowCheck][colCheck] == 0:
                emptyPot.append([rowCheck, colCheck])
            negXFail = True
        if negXString == 4:
            win = True
            highLightWin = highLightNegX
    otherTemp = [highLightNS, highLightEW, highLightPosX, highLightNegX]
    other = otherTemp.copy()
    for highLight in otherTemp:
        if (len(highLight) < 2) or (len(highLight) > 3):
            other.remove(highLight)
    stringList = {'win': highLightWin, 'other': other}
    return stringList, emptyPot
def getPotCon4(emptyPots, color, boardState, potCon4):
    for tile in emptyPots:
        board = deepcopy(boardState)
        board[tile[0]][tile[1]] = color
        strings = getStrings(tile, color, board)[0]
        if (strings['win'] != []) and (tile not in potCon4[color]):
            potCon4[color].append(tile) 
    newPotCon4 = {'Red': [], 'Yellow': []}
    for tile in potCon4['Red']:
        if boardState[tile[0]][tile[1]] == 0:
            newPotCon4['Red'].append(tile)
    for tile in potCon4['Yellow']:
        if boardState[tile[0]][tile[1]] == 0:
            newPotCon4['Yellow'].append(tile)
    return newPotCon4
def getPotCon4Points(old, new, weight, points):
    oddRows = [0, 2, 4]
    for newTile in new['Red']:
        points['Red'] += weight + math.ceil(newTile[0] / 2)
        if newTile[0] not in oddRows:
            lowestTile = True
            for tile in new['Red']:
                if (tile[1] == newTile[1]) and (newTile[0] < tile[0]):
                    lowestTile = False
            if lowestTile:
                for tile in new['Yellow']:
                    if (newTile[1] == tile[1]) and (tile[0] in oddRows) and (tile[0] >= newTile[0]):
                        lowestTile = False
            if lowestTile:
                points['Red'] += 7
    for oldTile in old['Red']:
        points['Red'] -= weight + math.ceil(oldTile[0] / 2)
        if oldTile[0] not in oddRows:
            lowestTile = True
            for tile in old['Red']:
                if (oldTile[1] == tile[1]) and (oldTile[0] < tile[0]):
                    lowestTile = False
            if lowestTile:
                for tile in old['Yellow']:
                    if (oldTile[1] == tile[1]) and (tile[0] in oddRows) and (tile[0] >= oldTile[0]):
                        lowestTile = False
            if lowestTile:
                points['Red'] -= 7
    for newTile in new['Yellow']:
        points['Yellow'] += weight + math.ceil(newTile[0] / 2)
        if newTile[0] in oddRows:
            lowestTile = True
            for tile in new['Yellow']:
                if (newTile[1] == tile[1]) and (newTile[0] < tile[0]):
                    lowestTile = False
            if lowestTile:
                for tile in new['Red']:
                    if (newTile[1] == tile[1]) and (tile[0] not in oddRows) and (tile[0] >= newTile[0]):
                        lowestTile = False
            if lowestTile:
                points['Yellow'] += 7
    for oldTile in old['Yellow']:
        points['Yellow'] -= weight + math.ceil(oldTile[0] / 2)
        if oldTile[0] in oddRows:
            lowestTile = True
            for tile in old['Yellow']:
                if (oldTile[1] == tile[1]) and (oldTile[0] < tile[0]):
                    lowestTile = False
            if lowestTile:
                for tile in old['Red']:
                    if (oldTile[1] == tile[1]) and (tile[0] not in oddRows) and (tile[0] >= oldTile[0]):
                        lowestTile = False
            if lowestTile:
                points['Yellow'] -= 7
    return points