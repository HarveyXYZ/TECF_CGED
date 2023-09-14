"""
This file contains the steps of generating edit tags based on parallel sentences of error-free sentence and ungrammatical sentence.
"""

#from Levenshtein import _levenshtein
from Levenshtein._levenshtein import editops

def existPunct(sen, pos1, pos2):
    maxPos = max(pos1, pos2)
    minPos = min(pos1, pos2)

    if sen.find(',', minPos, maxPos)>0 or sen.find('，', minPos, maxPos)>0 or \
            sen.find('。', minPos, maxPos)>0 or sen.find('？', minPos, maxPos)>0:
        return True
    else:
        return False

# sen1 = '你们放假前完全不一样了好像！'
# sen2 = '你们好像放假前完全不一样了是吧！'
# 返回：(3, 12, 14, 2)
# 分别是: InsPos: 插入的目标位置
#        RepPos1: 替换的起始位置
#        RepPos2: 替换的结束位置
#        InsLen: 插入的字符数
def moveReplace(sen1, sen2, ops):
    insertChars = ''
    posInsert = -1
    insertList = list()
    posInsList = list()

    for op in ops:
        if op[0] == 'insert':
            if posInsert == -1:
                posInsert = int(op[1])
                insertChars = sen2[int(op[2]):int(op[2]) + 1]
            elif posInsert == int(op[1]):
                insertChars = insertChars + sen2[int(op[2]):int(op[2])+1]
            else:
                insertList.append(insertChars)
                posInsList.append(posInsert)
                posInsert = int(op[1])
                insertChars = sen2[int(op[2]):int(op[2]) + 1]
        elif posInsert >= 0:
            insertList.append(insertChars)
            posInsList.append(posInsert)
            posInsert = -1
            insertChars = ''

    if len(insertChars) > 0:
        insertList.append(insertChars)
        posInsList.append(posInsert)

    if len(insertList) == 0:
        return False

    replaceChars = ''
    posReplace1 = -1
    posReplace2 = -1
    replaceList = list()
    posRepList1 = list()
    posRepList2 = list()

    for op in ops:
        if op[0] == 'replace':
            if posReplace1 == -1:
                posReplace1 = int(op[1])
                posReplace2 = int(op[2])
                replaceChars = sen1[int(op[1]):int(op[1]) + 1]
            elif posReplace1 == int(op[1])-1:
                posReplace1 = int(op[1])
                posReplace2 = int(op[2])
                replaceChars = replaceChars + sen1[int(op[1]):int(op[1]) + 1]
            else:
                replaceList.append(replaceChars)
                posRepList1.append(posReplace1 - len(replaceChars) + 1)
                posRepList2.append(posReplace2 - len(replaceChars) + 1)
                posReplace1 = int(op[1])
                posReplace2 = int(op[2])
                replaceChars = sen1[int(op[1]):int(op[1]) + 1]
        elif posReplace1 >= 0:
            replaceList.append(replaceChars)
            posRepList1.append(posReplace1 - len(replaceChars) + 1)
            posRepList2.append(posReplace2 - len(replaceChars) + 1)
            posReplace1 = -1
            posReplace2 = -1
            replaceChars = ''

    if len(replaceChars) > 0:
        replaceList.append(replaceChars)
        posRepList1.append(posReplace1 - len(replaceChars) + 1)
        posRepList2.append(posReplace2 - len(replaceChars) + 1)

    if len(replaceList) == 0:
        return False

    retInsPosList = list()
    retRepPosList1 = list()
    retRepPosList2 = list()
    retInsLenList = list()

    for index1 in range(0, len(insertList)):
        posInsert = posInsList[index1]
        insertChars = insertList[index1]
        for index2 in range(0, len(replaceList)):
            posReplace1 = posRepList1[index2]
            posReplace2 = posRepList2[index2]
            replaceChars = replaceList[index2]
            if insertChars in replaceChars:
                beginPos = replaceChars.find(insertChars)
                if not existPunct(sen1, posInsert, beginPos + posReplace1):
                    retInsPosList.append(posInsert)
                    retRepPosList1.append(beginPos + posReplace1)
                    retRepPosList2.append(beginPos + posReplace2)
                    retInsLenList.append(len(insertChars))

    if len(retInsPosList) > 0:
        #return retInsPosList, retRepPosList, retInsLenList
        return retInsPosList[0], retRepPosList1[0], retRepPosList2[0], retInsLenList[0]
    else:
        return False

# sen1 = '你们放假前完全不一样了好像！'
# sen2 = '你们好像放假前完全不一样了！'
# 返回：(3, 12, 2)
# 分别表示: InsPos: 插入的目标位置
#         DelPos: 删除的起始位置
#         InsLen: 插入的字符数
def moveDelete(sen1, sen2, ops):
    insertChars = ''
    posInsert = -1
    insertList = list()
    posInsList = list()

    for op in ops:
        if op[0] == 'insert':
            if posInsert == -1:
                posInsert = int(op[1])
                insertChars = sen2[int(op[2]):int(op[2]) + 1]
            elif posInsert == int(op[1]):
                insertChars = insertChars + sen2[int(op[2]):int(op[2])+1]
            else:
                insertList.append(insertChars)
                posInsList.append(posInsert)
                posInsert = int(op[1])
                insertChars = sen2[int(op[2]):int(op[2]) + 1]
        elif posInsert >= 0:
            insertList.append(insertChars)
            posInsList.append(posInsert)
            posInsert = -1
            insertChars = ''

    if len(insertChars) > 0:
        insertList.append(insertChars)
        posInsList.append(posInsert)

    if len(insertList) == 0:
        return False

    deleteChars = ''
    posDelete = -1
    deleteList = list()
    posDelList = list()

    for op in ops:
        if op[0] == 'delete':
            if posDelete == -1:
                posDelete = int(op[1])
                deleteChars = sen1[int(op[1]):int(op[1]) + 1]
            elif posDelete == int(op[1])-1:
                posDelete = int(op[1])
                deleteChars = deleteChars + sen1[int(op[1]):int(op[1]) + 1]
            else:
                deleteList.append(deleteChars)
                posDelList.append(posDelete-len(deleteChars)+1)
                posDelete = int(op[1])
                deleteChars = sen1[int(op[1]):int(op[1]) + 1]
        elif posDelete >= 0:
            deleteList.append(deleteChars)
            posDelList.append(posDelete-len(deleteChars)+1)
            posDelete = -1
            deleteChars = ''

    if len(deleteChars) > 0:
        deleteList.append(deleteChars)
        posDelList.append(posDelete-len(deleteChars)+1)

    if len(deleteList) == 0:
        return False

    retInsPosList = list()
    retDelPosList = list()
    retInsLenList = list()

    for index1 in range(0, len(insertList)):
        posInsert = posInsList[index1]
        insertChars = insertList[index1]
        for index2 in range(0, len(deleteList)):
            posDelete = posDelList[index2]
            deleteChars = deleteList[index2]
            if insertChars in deleteChars:
                begPos = deleteChars.find(insertChars)
                if not existPunct(sen1, posInsert, begPos+posDelete):
                    retInsPosList.append(posInsert)
                    retDelPosList.append(begPos+posDelete)
                    retInsLenList.append(len(insertChars))

    if len(retInsPosList) > 0:
        #return retInsPosList, retDelPosList, retInsLenList
        return retInsPosList[0], retDelPosList[0], retInsLenList[0]
    else:
        return False

# sen1 = '你们跟放假前完全不一样了好像！'
# sen2 = '你们好像放假前完全不一样了！'
# 返回：(3, 13, 2, 1)
# 分别是: insRepPos: 移动的目标位置
#        deletePos: 移动的起始位置
#        insRepLen: 被移动的字符数
#        repNum:    被替换的字符数
def moveReplaceDelete(sen1, sen2, ops):
    insRepChars = ''
    insRepList = list()
    posInsRep = -1
    posInsRepList = list()
    posRepStart = 0
    repCharsNum = 0
    repCharNumList = list()

    index1 = 0
    while index1 < len(ops):
        op = ops[index1]
        if op[0] == 'insert':
            posInsRep = int(op[1])
            insRepChars = sen2[int(op[2]):(int(op[2]) + 1)]
            posRepStart = 0
            flag = False
            for index2 in range(index1+1, len(ops)):
                op1 = ops[index2]
                if op1[0]=='insert' and int(op1[1])==posInsRep:
                    insRepChars = insRepChars + sen2[int(op1[2]):(int(op1[2]) + 1)]
                if op1[0]=='replace':
                    if int(op1[1])==posInsRep:
                        flag = True
                        repCharsNum = 1
                        posRepStart = index2
                        insRepChars = insRepChars + sen2[int(op1[2]):(int(op1[2]) + 1)]
                    elif int(op1[1])-posInsRep==index2-posRepStart:
                        insRepChars = insRepChars + sen2[int(op1[2]):(int(op1[2]) + 1)]
                        repCharsNum = repCharsNum + 1

            if flag:
                index1 = posRepStart
                insRepList.append(insRepChars)
                posInsRepList.append(posInsRep)
                repCharNumList.append(repCharsNum)

        index1 = index1 + 1

    if len(insRepList) == 0:
        return False

    deleteChars = ''
    posDelete = -1
    deleteList = list()
    posDelList = list()

    for op in ops:
        if op[0] == 'delete':
            if posDelete == -1:
                posDelete = int(op[1])
                deleteChars = sen1[int(op[1]):int(op[1]) + 1]
            elif posDelete == int(op[1])-1:
                posDelete = int(op[1])
                deleteChars = deleteChars + sen1[int(op[1]):int(op[1]) + 1]
            else:
                deleteList.append(deleteChars)
                posDelList.append(posDelete-len(deleteChars)+1)
                posDelete = int(op[1])
                deleteChars = sen1[int(op[1]):int(op[1]) + 1]
        elif posDelete >= 0:
            deleteList.append(deleteChars)
            posDelList.append(posDelete-len(deleteChars)+1)
            posDelete = -1
            deleteChars = ''

    if len(deleteChars) > 0:
        deleteList.append(deleteChars)
        posDelList.append(posDelete-len(deleteChars)+1)

    if len(deleteList) == 0:
        return False

    retInsRepPosList = list()
    retDeletePosList = list()
    retInsRepLenList = list()
    retReplacNumList = list()

    for index1 in range(0, len(insRepList)):
        posInsRep = posInsRepList[index1]
        insRepChars = insRepList[index1]
        replaceNum = repCharNumList[index1]
        for index2 in range(0, len(deleteList)):
            posDelete = posDelList[index2]
            deleteChars = deleteList[index2]
            if insRepChars in deleteChars:
                begPos = deleteChars.find(insRepChars)
                if not existPunct(sen1, posInsRep, begPos+posDelete):
                    retInsRepPosList.append(posInsRep)
                    retDeletePosList.append(begPos+posDelete)
                    retInsRepLenList.append(len(insRepChars))
                    retReplacNumList.append(replaceNum)

    if len(retInsRepPosList) > 0:
        return retInsRepPosList[0], retDeletePosList[0], retInsRepLenList[0], retReplacNumList[0]
    else:
        return False

# sen1 = '好像你们放假前完全不一样了！'
# sen2 = '你们好像放假前完全不一样了！'
# 返回：(1, 4)
# 分别是: SwapPos: 交换的起始位置
#        SwapLen: 交换的字符数量
def swapchars(sen1, sen2, ops):
    replaceList1 = list()
    repPosList = list()
    replaceList2 = list()
    repChars1 = ''
    repChars2 = ''
    repPos = -1

    for index in range(0, len(ops)):
        if ops[index][0] == 'replace':
            if repPos == -1:
                repPos = int(ops[index][1])
                repChars1 = sen1[int(ops[index][1]) : int(ops[index][1]) + 1]
                repChars2 = sen2[int(ops[index][2]) : int(ops[index][2]) + 1]
            elif repPos == int(ops[index][1]) - 1:
                repPos = int(ops[index][1])
                repChars1 = repChars1 + sen1[int(ops[index][1]): int(ops[index][1]) + 1]
                repChars2 = repChars2 + sen2[int(ops[index][2]): int(ops[index][2]) + 1]
            else:
                replaceList1.append(repChars1)
                replaceList2.append(repChars2)
                repPosList.append(repPos - len(repChars1) + 1)
                repPos = int(ops[index][1])
                repChars1 = sen1[int(ops[index][1]): int(ops[index][1]) + 1]
                repChars2 = sen2[int(ops[index][2]): int(ops[index][2]) + 1]

        elif len(repChars1) > 0:
            replaceList1.append(repChars1)
            replaceList2.append(repChars2)
            repPosList.append(repPos - len(repChars1) + 1)
            repChars1 = ''
            repChars2 = ''
            repPos = -1

        else:
            repChars1 = ''
            repChars2 = ''
            repPos = -1

    if len(repChars1) > 0:
        replaceList1.append(repChars1)
        replaceList2.append(repChars2)
        repPosList.append(repPos - len(repChars1) + 1)

    if len(replaceList1) == 0:
        return False

    retSwapPosList = list()
    retSwapLenList = list()
    for index in range(0, len(replaceList1)):
        repChars1 = replaceList1[index]
        repChars2 = replaceList2[index]
        repPos = int(repPosList[index])

        index1 = -1
        while index1 < len(repChars1):
            index1 = index1 + 1
            for index2 in range(index1+1, len(repChars1)):
                repStr1 = repChars1[index1:index2+1]
                repStr2 = repChars2[index1:index2+1]
                midPos = int((index2+1+index1)/2)
                swapStr = repStr1[midPos:index2+1] + repStr1[index1:midPos]
                if swapStr == repStr2:
                    retSwapPosList.append(repPos)
                    retSwapLenList.append(len(repStr1))
                    index1 = index2

    if len(retSwapPosList) == 0:
        return False
    else:
        return retSwapPosList, retSwapLenList

# 获取插入/替换的词语
def get_IRword(I_or_R, insPos, ops, sen2):
    IRword = ''

    for op in ops:
        if op[0]==I_or_R and op[1]==insPos:
            IRword = IRword + sen2[op[2]:(op[2]+1)]

    return IRword

# 分段纠正，多次迭代
# 1. 检查swap，标为T1
# 2. 检查insert，区分insert+delete, insert+replace(换成delete + insert)，单独的insert
# 3. 再检查 delete，replace
# IRType: 0-输出[I]/[R], 1-输出[In]/[Rn], 2-输出[I())]/[R()]
def genLabels(sen1, sen2, ops, IRType=0):
    tagsen = sen1

    if swapchars(sen1, sen2, ops):
        #print('swap_chars')
        posList, lenList = swapchars(sen1, sen2, ops)

        for index in range(len(posList), 0, -1):
            post = posList[index-1]
            leng = lenList[index-1]
            for index1 in range(leng, 0, -1):
                pos = post + index1 - 1
                tagsen = tagsen[:pos] + '[__T1__]' + tagsen[pos:]

    elif moveReplaceDelete(sen1, sen2, ops):
        #print('move_replace_delete')
        # insRepPos: 移动的目标位置
        # deletePos: 移动的起始位置
        # insRepLen: 被移动的字符数
        # repNum:    被替换的字符数
        insRepPos, deletePos, insRepLen, repNum = moveReplaceDelete(sen1, sen2, ops)
        if deletePos < insRepPos:
            for index in range(insRepPos+repNum, insRepPos, -1):
                pos = index - 1
                tagsen = tagsen[:pos] + '[__D__]' + tagsen[pos:]
            pos = insRepPos + (len('[__D__]')+1) * repNum
            tagsen = tagsen[:pos] + '[__IT__]' + tagsen[pos:]
            for index in range(deletePos+insRepLen, deletePos, -1):
                pos = index - 1
                tagsen = tagsen[:pos] + '[__T2__]' + tagsen[pos:]
        else:
            for index in range(deletePos+insRepLen, deletePos, -1):
                pos = index - 1
                tagsen = tagsen[:pos] + '[__T2__]' + tagsen[pos:]
            for index in range(insRepPos+repNum, insRepPos, -1):
                pos = index - 1
                tagsen = tagsen[:pos] + '[__D__]' + tagsen[pos:]
            pos = insRepPos + (len('[__D__]')+1) * repNum
            tagsen = tagsen[:pos] + '[__IT__]' + tagsen[pos:]

    elif moveDelete(sen1, sen2, ops):
        #print('insert_delete')
        # InsPos: 插入的目标位置
        # DelPos: 删除的起始位置
        # InsLen: 插入的字符数
        insPos, delPos, insLen = moveDelete(sen1, sen2, ops)
        tagsen = sen1[:insPos] + '[__IT__]' + sen1[insPos:]
        if insPos<delPos: shift = len('[__IT__]')
        else: shift = 0
        for index in range(insLen+delPos, delPos, -1):
            pos = index + shift - 1
            tagsen = tagsen[:pos] + '[__T2__]' + tagsen[pos:]

    elif moveReplace(sen1, sen2, ops):
        #print('insert_replace')
        # InsPos:  插入的目标位置
        # RepPos:  替换的起始位置
        # RepPos2: 替换的结束位置
        # InsLen:  插入的字符数
        insPos, repPos1, repPos2, insLen = moveReplace(sen1, sen2, ops)

        #print(insertReplace(sen1, sen2, ops))

        if repPos1 < insPos:
            tagsen = sen1[:insPos] + '[__IT__]' + sen1[insPos:]
            for index in range(repPos1+insLen, repPos1, -1):
                pos = index - 1
                tagsen = tagsen[:pos] + '[__T2__]' + tagsen[pos:]
            pos = repPos1 + (len('[__T2__]')+1) * insLen
            #tagsen = tagsen[:pos] + '[__I__]' + tagsen[pos:]
        else:
            for index in range(repPos1+insLen, repPos1, -1):
                pos = index - 1
                tagsen = tagsen[:pos] + '[__T2__]' + tagsen[pos:]
            pos = repPos1 + (len('[__T2__]')+1) * insLen
            #tagsen = tagsen[:pos] + '[__I__]' + tagsen[pos:]
            tagsen = tagsen[:insPos] + '[__IT__]' + tagsen[insPos:]

    else:
        insPos = -1
        posshift = 0
        for op in ops:
            if op[0] == 'insert':
                if int(op[1]) > insPos:
                    insPos = int(op[1])
                    word = ''
                    if IRType==2: # 显示插入/替换的词语
                        word = '('+get_IRword(op[0], insPos, ops, sen2)+')'
                    tagsen = tagsen[:(insPos+posshift)] + '[__I'+word+'__]' + tagsen[(insPos+posshift):]
                    posshift += len('[__I'+word+'__]')
                elif IRType==1 and int(op[1]) == insPos:
                    tagsen = tagsen[:(insPos+posshift)] + '[__I__]' + tagsen[(insPos+posshift):]
                    posshift += len('[__I__]')
            if op[0] == 'delete':
                delPos = int(op[1])
                tagsen = tagsen[:(delPos+posshift)] + '[__D__]' + tagsen[(delPos+posshift):]
                posshift += len('[__D__]')
            if op[0] == 'replace':
                repPos = int(op[1])
                word = ''
                if IRType==2: # 显示插入/替换的词语
                    word = '('+get_IRword(op[0], repPos, ops, sen2)+')'
                tagsen = tagsen[:(repPos+posshift)] + '[__R'+word+'__]' + tagsen[(repPos+posshift):]
                posshift += len('[__R'+word+'__]')

    if IRType==1: # 显示插入/替换的字符数量
        for num1 in range(20, 1, -1):
            istr = '[__I__]'
            for num2 in range(1, num1):
                istr = istr + '[__I__]'
            tagsen = tagsen.replace(istr, '[__I' + str(num1) + '__]')

        tagsen = tagsen.replace('[__I__][__R__]', '[__R2__]')
        for num1 in range(2, 20):
            tagsen = tagsen.replace('[__I' + str(num1) + '__][__R__]', '[__R' + str(num1 + 1) + '__]')

    elif IRType == 2:  # 显示插入/替换的词语
        # 例如：将[__I(我们)__][__R(是)__]替换为[__R(我们是)__]
        while ')__][__R(' in tagsen:
            pos1 = tagsen.find(')__][__R(')
            pos2 = tagsen.find('(', pos1)
            for index in range(pos1, 0, -1):
                if tagsen[index] == '(':
                    break
            pos3 = index
            word = tagsen[pos3+1 : pos1]
            tagsen = tagsen[:(pos3-1)] + 'R(' + word + tagsen[(pos2+1):]

    else:
        tagsen = tagsen.replace('[__I__][__R__]', '[__R__]')

    return tagsen

def genNewSen(sen1, sen2, ops):
    newsen = sen1

    if swapchars(sen1, sen2, ops):
        #print('swap_chars')
        posList, lenList = swapchars(sen1, sen2, ops)

        for index in range(0, len(posList)):
            post = posList[index]
            leng = lenList[index]
            midpos = int((post+post+leng)/2)
            swapstr = sen1[midpos:(post+leng)] + sen1[post:midpos]
            newsen = newsen[:post] + swapstr + newsen[(post+leng):]

    elif moveReplaceDelete(sen1, sen2, ops):
        #print('insert_replace_delete')
        insRepPos, deletePos, insRepLen, repNum = moveReplaceDelete(sen1, sen2, ops)
        newsen = sen1
        insStr = sen1[deletePos:(deletePos+insRepLen)]
        if insRepPos < deletePos:
            newsen = newsen[:insRepPos] + insStr + newsen[insRepPos+repNum:deletePos] + newsen[(deletePos+insRepLen):]
            #newsen = newsen[:insRepPos] + insStr + newsen[insRepPos+repNum:deletePos] + newsen[deletePos:]
        else:
            newsen = newsen[:deletePos] + newsen[(deletePos + insRepLen):insRepPos] + insStr + newsen[insRepPos+repNum:]
            #newsen = newsen[:deletePos] + newsen[(deletePos + insRepLen):insRepPos] + insStr + newsen[insRepPos:]

    elif moveDelete(sen1, sen2, ops):
        #print('insert_delete')
        insPos, delPos, insLen = moveDelete(sen1, sen2, ops)
        newsen = sen1
        insStr = sen1[delPos:(delPos+insLen)]
        if insPos < delPos:
            newsen = newsen[:insPos] + insStr + newsen[insPos:delPos] + newsen[(delPos+insLen):]
        else:
            newsen = newsen[:delPos] + newsen[(delPos + insLen):insPos] + insStr + newsen[insPos:]

    elif moveReplace(sen1, sen2, ops):
        #print('insert_replace')
        insPos, repPos1, repPos2, insLen = moveReplace(sen1, sen2, ops)
        newsen = sen1
        insStr = sen1[repPos1:(repPos1 + insLen)]
        repStr = sen2[repPos2:(repPos2 + insLen)]
        if insPos < repPos1:
            #newsen = newsen[:insPos] + insStr + newsen[insPos:repPos1] + repStr + newsen[(repPos1 + insLen):]
            newsen = newsen[:insPos] + insStr + newsen[insPos:repPos1] + newsen[(repPos1 + insLen):]
        else:
            #newsen = newsen[:repPos1] + repStr + newsen[(repPos1 + insLen):insPos] + insStr + newsen[insPos:]
            newsen = newsen[:repPos1] + newsen[(repPos1 + insLen):insPos] + insStr + newsen[insPos:]

    else:
        posChange = 0
        for op in ops:
            if op[0] == 'insert':
                insPos = int(op[1]) + posChange
                insChar = sen2[int(op[2]) : int(op[2])+1]
                newsen = newsen[:insPos] + insChar + newsen[insPos:]
                posChange = posChange + 1
            if op[0] == 'delete':
                delPos = int(op[1]) + posChange
                newsen = newsen[:delPos] + newsen[delPos+1:]
                posChange = posChange - 1
            if op[0] == 'replace':
                repPos = int(op[1]) + posChange
                repChar = sen2[int(op[2]) : int(op[2])+1]
                newsen = newsen[:repPos] + repChar + newsen[repPos+1:]

    return newsen

def add_space(text):
    rstr = ''
    flag = True
    for index in range(0, len(text)):
        if text[index:].startswith('[__'):
            flag = False
        if index>=2 and text[(index-2):].startswith('__]'):
            flag = True

        if flag:
            rstr = rstr + text[index] + ' '
        else:
            rstr = rstr + text[index]

    return rstr

def T1_to_W(instr):
    # [T1] 她 [T1] 开 玩 笑 地 说 ， 她 [T1] 为 [T1] 我 [T1] 可 [T1] 以 当 免 费 的 [T1] 导 [T1] 游 [T1] 。
    str1 = instr.replace('[__T1__]', '[__W1__]').strip()
    str2 = str1.split(' ')
    oustr = ''

    index = 0
    while index < len(str2):
        if str2[index] == '[__W1__]':
            tmpindex = index
            while index < len(str2) and str2[index] == '[__W1__]':
                index = index + 2
            half = int((index+tmpindex)/2)

            for newindex in range(tmpindex, half):
                oustr = oustr + str2[newindex] + ' '
            for newindex in range(half, index):
                oustr = oustr + str2[newindex].replace('[__W1__]', '[__W2__]') + ' '
        else:
            oustr = oustr + str2[index] + ' '
            index = index + 1

    return oustr.strip()

def T2_to_W(instr):
    # 她 开 玩 笑 地 说 ， 她 [T2] 为 [T2] 我 可 以 [IT] 当 免 费 的 导 游 。
    # 为 了 [T2] 不 [T2] 发 [T2] 生 自 己 身 边 [D] 有 [IT] 这 件 事 。
    # 她 开 玩 笑 地 说 ， 她 [IT] 为 我 [T2] 可 [T2] 以 当 免 费 的 导 游 。
    str1 = instr.strip().split(' ')
    oustr = ''

    index = 0
    while index < len(str1):
        if str1[index] == '[__T2__]':
            tmpindex1 = index
            while index < len(str1) and str1[index] == '[__T2__]':
                index = index + 2
            tmpindex2 = index
            while index < len(str1) and not (str1[index] == '[__IT__]'):
                index = index + 1

            for newindex in range(tmpindex1, tmpindex2):
                if str1[newindex] == '[__T2__]':
                    oustr = oustr + '[__W1__] '
                else:
                    oustr = oustr + str1[newindex] + ' '

            endW2 = False
            for newindex in range(tmpindex2, index):
                if str1[newindex]=='[__D__]':
                    endW2 = True
                    oustr = oustr + '[__D__] '
                elif endW2:
                    oustr = oustr + str1[newindex] + ' '
                else:
                    oustr = oustr + '[__W2__] ' + str1[newindex] + ' '

            index = index + 1
        elif str1[index] == '[__IT__]':
            tmpindex1 = index
            while index < len(str1) and not str1[index] == '[__T2__]':
                index = index + 1
            tmpindex2 = index
            while index < len(str1) and str1[index] == '[__T2__]':
                index = index + 2

            for newindex in range(tmpindex1+1, tmpindex2):
                oustr = oustr + '[__W1__] ' + str1[newindex] + ' '
            for newindex in range(tmpindex2, index):
                if str1[newindex] == '[__T2__]':
                    oustr = oustr + '[__W2__] '
                else:
                    oustr = oustr + str1[newindex] + ' '
        else:
            oustr = oustr + str1[index] + ' '
            index = index + 1

    return oustr.strip()

def T_to_W(instr):
    oustr = instr
    if '[__T1__]' in instr:
        oustr = T1_to_W(instr)
    if '[__T2__]' in instr:
        oustr = T2_to_W(instr)

    return oustr

if __name__ == '__main__':
    sen1 = '它为了却自己身边不发生这件事情。'
    sen2 = '它为让阿萨给自己身边不发生这件事吧。'
    sen1 = ' ' + sen1
    sen2 = ' ' + sen2

    while not sen1==sen2:
        ops = editops(sen1, sen2)
        print(ops)

        labels = T_to_W(add_space(genLabels(sen1, sen2, ops, IRType=2)))
        sen1 = genNewSen(sen1, sen2, ops)
        print(labels)
        print(sen1)
