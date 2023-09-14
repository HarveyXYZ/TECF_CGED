import jieba

def combSenLab():
    sens = open('/分析/n1-test-1111.txt', 'r', encoding='utf-8').readlines()
    tags = open('/outputs_xhh/n12-200-32bz-ce-lert/predict_result.txt', 'r', encoding='utf-8').readlines()
    oufile = open('/分析/n12-200-32bz-ce-lert.tr', 'w', encoding='utf-8')

    num = -1
    for index in range(len(tags)):
        if tags[index].startswith('----------------------------------------'):
            num = num + 1
            sen = sens[num].strip()
            senseq = sen.split(' ')

            for s in senseq:
                if s.startswith('[') and s.endswith(']'):
                    oufile.write(s[1:-1])
                else:
                    oufile.write(s + '\t')

            oufile.write('\n' + tags[index+2].strip())
            oufile.write('\n' + tags[index+3].strip())
            oufile.write('\n' + tags[index+4].strip() + '\n')

def tagModifyResult(file, oufile):
    filestrs = file.readlines()

    for index in range(0, len(filestrs)):
        if filestrs[index].startswith('--------------------'):
            chars = filestrs[index + 1].strip()
            tags1 = filestrs[index + 2].strip()
            tags2 = filestrs[index + 3].strip()
            tags3 = filestrs[index + 4].strip()

            charlist = chars.split('\t')
            taglist1 = tags1.split('\t')
            taglist2 = tags2.split('\t')
            taglist3 = tags3.split('\t')

            newtaglist1 = padW1W2(charlist, taglist1)
            newtaglist1 = halfD(charlist, newtaglist1)
            newtaglist1 = redunW1W2(charlist, newtaglist1)
            #newtaglist1 = irregW1W2(charlist, newtaglist1)
                          #padW1W2byWord(charlist, taglist1)

            newtags1 = ''

            for tag in newtaglist1:
                newtags1 = newtags1 + tag + '\t'

            """
            if not newtags1.strip()==tags1.strip():
                print(chars)
                print(newtags1)
                print(tags1)"""

            oufile.write('----------------------------------------\n')
            oufile.write(chars + '\n')
            oufile.write(newtags1 + '\n')
            oufile.write(tags2 + '\n')
            oufile.write(tags3 + '\n')

    return newtags1

# W1 _ W1 W1 W2 W2
# W1 W2 _ W2
def padW1W2(chars, tags):
    assert(len(chars) == len(tags))

    index1 = 0
    while index1 < len(chars):
        if tags[index1] == 'W1':
            index2 = index1
            W2_start = 1000
            W2_end = -1

            while index2 < len(chars):
                if chars[index2] == '，' or chars[index2] == ',' or chars[index2] == '。' \
                        or chars[index2] == '！' or chars[index2] == '？':
                    break
                elif tags[index2] == 'W2':
                    W2_start = min(W2_start, index2)
                    W2_end = max(W2_end, index2)
                    index2 = index2 + 1
                elif (not tags[index2] == 'O') and W2_end > 0:
                    break
                else:
                    index2 = index2 + 1

            if W2_end > 0:
                for index in range(index1, W2_start):
                    tags[index] = 'W1'
                for index in range(W2_start, W2_end):
                    tags[index] = 'W2'

                index1 = W2_end
            else:
                index1 = index1 + 1
        else:
            index1 = index1 + 1

    return tags

# 可 是 这 种 问 题 是 肯 定 很 多 吧 。
# _  _ _  _  _ _ W1 W2 _ _ _ _ _
def padW1W2byWord(chars, tags):
    assert(len(chars) == len(tags))

    sen = ''
    for index in range(0, len(chars)):
        if chars[index]=='[UNK]':
            chars[index] = 'UNK'
        sen = sen + chars[index]

    words = jieba.cut(sen)

    charIndex = 0
    for word in words:
        #print(word)
        str = ''
        for index1 in range(charIndex, len(chars)):
            str = str + chars[index1]
            if str == word:
                break
        for index2 in range(charIndex, index1+1):
            if tags[index2]=='W1' or tags[index2]=='W2':
                flag = True
                for index3 in range(charIndex, index1+1):
                    if not index3 == index2 and not tags[index3]=='O':
                        flag = False
                if flag:
                    for index4 in range(charIndex, index1+1):
                        tags[index4] = tags[index2]
        charIndex = index1+1

    return tags

# 所以	，	有	人	一	直	吸	D烟	着	中	南	海	。
# _	_	_	_	_	_	_	_	W1	R	_	_	_	_
def irregW1W2(chars, tags):
    withW1 = False
    withW2 = False
    withIDR = False
    for tag in tags:
        if tag == 'W1':
            withW1 = True
        if tag == 'W2':
            withW2 = True
        if tag == 'I' or tag == 'D' or tag == 'R':
            withIDR = True

    if ((withW1 and withW2==False) or (withW1==False and withW2)) and withIDR:
        for index in range(0, len(tags)):
            if tags[index] == 'W1' or tags[index] == 'W2':
                tags[index] = 'O'

    return tags

# 我一	有	时	间	就	给	你	你	打	电	话	吧	。
# _	_	_	_	_	_	_	W1	W2	_	_	_	_	_
def redunW1W2(chars, tags):
    assert(len(chars)==len(tags))

    W1Str = ''
    W2Str = ''
    for index in range(len(tags)):
        if tags[index]=='W1':
            W1Str = W1Str + chars[index]
        if tags[index]=='W2':
            W2Str = W2Str + chars[index]

    if W1Str==W2Str:
        for index in range(len(tags)):
            if tags[index] == 'W1':
                tags[index] = 'O'
            if tags[index] == 'W2':
                tags[index] = 'D'

    return tags

def halfD(chars, tags):
    assert(len(chars)==len(tags))

    for index1 in range(len(chars)):
        if chars[index1]=='“':
            for index2 in range(index1+1, len(chars)):
                if chars[index2]=='”' and \
                        ((tags[index1]=='D' and tags[index2]=='O') or (tags[index1]=='O' and tags[index2]=='D')):
                    tags[index1] = 'O'
                    tags[index2] = 'O'
        if chars[index1] == '[UNK]':
            for index2 in range(index1+1, len(chars)):
                if chars[index2] == '[UNK]' and \
                        ((tags[index1]=='D' and tags[index2]=='O') or (tags[index1]=='O' and tags[index2]=='D')):
                    tags[index1] = 'O'
                    tags[index2] = 'O'
        if chars[index1] == '《':
            for index2 in range(index1+1, len(chars)):
                if chars[index2] == '》' and \
                        ((tags[index1]=='D' and tags[index2]=='O') or (tags[index1]=='O' and tags[index2]=='D')):
                    tags[index1] = 'O'
                    tags[index2] = 'O'
        if chars[index1] == '(':
            for index2 in range(index1+1, len(chars)):
                if chars[index2] == ')' and \
                        ((tags[index1]=='D' and tags[index2]=='O') or (tags[index1]=='O' and tags[index2]=='D')):
                    tags[index1] = 'O'
                    tags[index2] = 'O'
        if chars[index1] == '[':
            for index2 in range(index1+1, len(chars)):
                if chars[index2] == ']' and \
                        ((tags[index1]=='D' and tags[index2]=='O') or (tags[index1]=='O' and tags[index2]=='D')):
                    tags[index1] = 'O'
                    tags[index2] = 'O'
        if chars[index1] == '{':
            for index2 in range(index1+1, len(chars)):
                if chars[index2] == '}' and \
                        ((tags[index1] == 'D' and (tags[index2] == 'O')) or (tags[index1] == 'O' and (tags[index2] == 'D'))):
                    tags[index1] = 'O'
                    tags[index2] = 'O'

    return tags

# 你   们    都    在   哪    啊
# W1   W1   D     W2  W2    W2
# 在   哪    啊    都   你   们
# W2   W2   W2    D   W1   W1
def swapW1W2(chars, tags):
    assert (len(chars) == len(tags))

    newchars = ''
    newtags = ''
    index = 0
    while index < len(chars):
        if tags[index] == 'W1':
            W1Start = index
            W1Endng = index
            W2Start = 50000
            W2Endng = 50000
            index = index + 1
            while W2Endng > len(chars) and index < len(chars):
                if tags[index] == 'W1':
                    W1Endng = max(index, W1Endng)
                elif tags[index] == 'W2':
                    W2Start = min(index, W2Start)
                elif not W2Start == 50000:
                    W2Endng = index-1

                index = index + 1

            if not W2Start == 50000:
                if W2Endng == 50000:
                    W2Endng = len(chars) - 1

                for index1 in range(W2Start, W2Endng + 1):
                    newchars = newchars + chars[index1] + '\t'
                    newtags = newtags + tags[index1] + '\t'
                for index2 in range(W1Endng+1, W2Start):
                    newchars = newchars + chars[index2] + '\t'
                    newtags = newtags + tags[index2] + '\t'
                for index3 in range(W1Start, W1Endng + 1):
                    newchars = newchars + chars[index3] + '\t'
                    newtags = newtags + tags[index3] + '\t'

                index = W2Endng + 1

            else:
                for index1 in range(W1Start, W1Endng + 1):
                    newchars = newchars + chars[index1] + '\t'
                    newtags = newtags + tags[index1] + '\t'

                index = W1Endng + 1
        else:
            newchars = newchars + chars[index] + '\t'
            newtags = newtags + tags[index] + '\t'
            index = index + 1

    chars = newchars.strip().split('\t')
    tags = newtags.strip().split('\t')

    return chars, tags

def editByTags(chars, tags):
    assert(len(chars) == len(tags))

    chars, tags = swapW1W2(chars, tags)

    newchars = ''
    index = 0
    while index < len(chars):
        if tags[index] == 'O':
            newchars = newchars + chars[index] + '\t'
        elif tags[index] == 'I':
            newchars = newchars + '[I]\t' + chars[index] + '\t'
        elif tags[index] == 'R':
            newchars = newchars + '[R]\t' + chars[index] + '\t'
        elif tags[index] == 'D':
            newchars = newchars
        else:
            newchars = newchars + chars[index] + '\t'

        index = index + 1

    return newchars.strip()

if __name__ == '__main__':
    chars = '医	院	又	给	我	们	家	里	打	电	话	过	来	了	。'
    tags  = 'W1	W1	D	W2	W2	D	O	I	O	R	O	O	O	O	O'
    newsen = editByTags(chars.split('\t'), tags.split('\t'))
    print(newsen)
