import commonTools
import leven2edit as l2e

def genTaggingSeq():
    inpstrs = open('data_processed/1206-inco+corr-pairs-checked_ANUM.txt',
                   'r', encoding='utf-8').readlines()
    outfile = open('dataEnhance/ErrorTypes/TagSeq_1206-inco+corr-pairs-checked_ANUM.txt',
                   'w', encoding='utf-8')

    outfile.write('===========\n')
    for rowindex in range(len(inpstrs)):
        if inpstrs[rowindex].startswith('==========='):
            input = inpstrs[rowindex - 1].strip()
            output = inpstrs[rowindex - 2].strip()

            sen_right = ' ' + input
            sen_wrong = ' ' + output

            while not sen_right == sen_wrong:
                outfile.write(sen_right.strip() + '\n')

                ops = l2e.editops(sen_right, sen_wrong)
                labels = l2e.genLabels(sen_right, sen_wrong, ops, IRType=2)

                labelseq = l2e.T_to_W(l2e.add_space(labels.strip()))
                labelseqlist = labelseq.split(' ')

                wordlist = commonTools.postagging(sen_right)
                sen_right = l2e.genNewSen(sen_right, sen_wrong, ops)
                outfile.write(sen_right.strip() + '\n')

                index = 0
                for word, ptag in wordlist:
                    outfile.write(word+'\t'+ptag+'\t')
                    label = ''
                    aword = ''
                    while index < len(labelseqlist):
                        if labelseqlist[index].startswith('[__'):
                            label = label+labelseqlist[index]
                            index += 1
                        else:
                            if index==0 or not labelseqlist[index-1].startswith('[__'):
                                label = label + '[____]'
                            aword = aword + labelseqlist[index]
                            index += 1
                        if aword==word:
                            break
                    outfile.write(label + '\n')

                outfile.write('===========\n')

def countchars(inputstrs, rowindex):
    count = 0
    for index1 in range(rowindex-1, 0, -1):
        if not '[__' in inputstrs[index1]:
            break
        else:
            sstr = inputstrs[index1].strip().split('\t')
            count += len(sstr[0])
    return count

def isOnlyW1(sstr):
    if '[__W1' in sstr and not '[__W2' in sstr and not '[____]' in sstr and \
        not '[__D' in sstr and not '[__I' in sstr and not '[__R' in sstr:
        return True
    else:
        return False

def isOnlyW2(sstr):
    if '[__W2' in sstr and not '[__W1' in sstr and not '[____]' in sstr and \
        not '[__D' in sstr and not '[__I' in sstr and not '[__R' in sstr:
        return True
    else:
        return False

def isOnlyW1W2(sstr):
    if '[__W2' in sstr and '[__W1' in sstr and not '[____]' in sstr and \
        not '[__D' in sstr and not '[__I' in sstr and not '[__R' in sstr:
        return True
    else:
        return False

def isOnlyD(sstr):
    if '[__D' in sstr and not '[__W' in sstr and not '[__R' in sstr and \
        not '[__I' in sstr and not '[____]' in sstr:
        return True
    else:
        return False

def isOnlyD_O(sstr):
    if '[__D' in sstr and '[____]' in sstr and not '[__W' in sstr and \
        not '[__R' in sstr and not '[__I' in sstr:
        return True
    else:
        return False

def analyzeErrorType_D(wordposwant='[word]'):
    import matplotlib.pyplot as plt
    import pandas as pd

    # genTaggingSeq()
    inpstrs = open(
        'dataEnhance/ErrorTypes/TagSeq_1206-inco+corr-pairs-checked_ANUM.txt.txt', 'r', encoding='utf-8').readlines()

    totalnum = 0
    rowindex = 0
    senindex = 0
    positionlist = list()  ### 删除词语某字的情况
    wordpos_count_dict = dict()

    ### 参数设置 ###
    before_tks = 2                       # 记录前面第几个词/词性，<1表示0个，=1表示1个，>1表示2个
    after_tks  = 1                       # 记录后面第几个词/词性，<1表示0个，=1表示1个，>1表示2个
    check_around_pos  = True            # 是否计算相关词性序列
    check_around_word = True             # 是否计算相关词语序列
    # 要计算的词性/词语；
    # - 检查所有词性情况，设置为[pos]，
    # - 检查词语情况，设置为[word]
    # - 检查删除某字情况，设置为[half]
    wordpos_want = wordposwant
    ##############
    while rowindex < len(inpstrs):
        if inpstrs[rowindex].startswith('======='):
            senindex = rowindex + 1
            rowindex += 1
        ### 删除词语某个字的情况 ###
        elif isOnlyD_O(inpstrs[rowindex]) and wordpos_want == '[half]':
            totalnum += 1
            charcount = countchars(inpstrs, rowindex)
            positionlist.append(float(charcount)/float(len(inpstrs[senindex])-1))

            slist = inpstrs[rowindex].strip().split('\t')
            word_arword = '[' + slist[0] + ']'
            word_arpos  = '[' + slist[0] + ']'

            a_word = ''
            a_pos  = ''
            if before_tks >= 1:
                if '[__' in inpstrs[rowindex - 1]:
                    a_word = inpstrs[rowindex - 1].strip().split('\t')[0]
                    a_pos  = inpstrs[rowindex - 1].strip().split('\t')[1]
                else:
                    a_word = '[句首]'
                    a_pos  = '[句首]'
                word_arword = a_word + '_' + word_arword
                word_arpos  = a_pos  + '_' + word_arpos
            if after_tks >= 1:
                if '[__' in inpstrs[rowindex + 1]:
                    a_word = inpstrs[rowindex + 1].strip().split('\t')[0]
                    a_pos = inpstrs[rowindex + 1].strip().split('\t')[1]
                else:
                    a_word = '[句尾]'
                    a_pos  = '[句尾]'
                word_arword = word_arword + '_' + a_word
                word_arpos  = word_arpos  + '_' + a_pos

            if check_around_pos:
                if word_arpos in wordpos_count_dict:
                    wordpos_count_dict[word_arpos] += 1
                else:
                    wordpos_count_dict[word_arpos] = 1
            elif check_around_word:
                if word_arword in wordpos_count_dict:
                    wordpos_count_dict[word_arword] += 1
                else:
                    wordpos_count_dict[word_arword] = 1

            rowindex += 1
        ### 整词被删除的情况 ###
        elif isOnlyD(inpstrs[rowindex]) and not isOnlyD(inpstrs[rowindex-1]) and (wordpos_want=='[pos]' or wordpos_want=='[word]'):
            totalnum += 1
            charcount = countchars(inpstrs, rowindex)
            positionlist.append(float(charcount)/float(len(inpstrs[senindex])-1))

            slist = inpstrs[rowindex].strip().split('\t')
            word_arword = slist[0]
            word_arpos  = slist[0]
            pos_arword  = slist[1]
            pos_arpos   = slist[1]

            indextmp = rowindex
            rowindex += 1
            while isOnlyD(inpstrs[rowindex]):
                slist = inpstrs[rowindex].strip().split('\t')
                word_arpos  = word_arpos  + '+' + slist[0]
                word_arword = word_arword + '+' + slist[0]
                pos_arpos   = pos_arpos   + '+' + slist[1]
                pos_arword  = pos_arword  + '+' + slist[1]
                rowindex += 1

            word_arpos  = '[' + word_arpos + ']'
            word_arword = '[' + word_arword + ']'
            pos_arpos   = '[' + pos_arpos + ']'
            pos_arword  = '[' + pos_arword + ']'

            a_word = ''
            a_pos = ''
            if before_tks >= 1:
                if '[__' in inpstrs[indextmp - 1]:
                    a_word = inpstrs[indextmp - 1].strip().split('\t')[0]
                    a_pos = inpstrs[indextmp - 1].strip().split('\t')[1]
                else:
                    a_word = '[句首]'
                    a_pos = '[句首]'
                word_arword = a_word + '_' + word_arword
                pos_arpos   = a_pos + '_' + pos_arpos
                word_arpos  = a_pos + '_' + word_arpos
                pos_arword  = a_word + '_' + pos_arword
            if before_tks > 1:
                if '[__' in inpstrs[indextmp - 2]:
                    a_word = inpstrs[indextmp - 2].strip().split('\t')[0]
                    a_pos = inpstrs[indextmp - 2].strip().split('\t')[1]
                else:
                    a_word = '[句首]'
                    a_pos = '[句首]'
                word_arword = a_word + '_' + word_arword
                pos_arpos   = a_pos + '_' + pos_arpos
                word_arpos  = a_pos + '_' + word_arpos
                pos_arword  = a_word + '_' + pos_arword
            if after_tks >= 1:
                if '[__' in inpstrs[rowindex]:
                    a_word = inpstrs[rowindex].strip().split('\t')[0]
                    a_pos = inpstrs[rowindex].strip().split('\t')[1]
                else:
                    a_word = '[句尾]'
                    a_pos = '[句尾]'
                word_arword = word_arword + '_' + a_word
                pos_arpos   = pos_arpos + '_' + a_pos
                word_arpos  = word_arpos + '_' + a_pos
                pos_arword  = pos_arword + '_' + a_word
            if after_tks > 1:
                if '[__' in inpstrs[rowindex + 1]:
                    a_word = inpstrs[rowindex + 1].strip().split('\t')[0]
                    a_pos = inpstrs[rowindex + 1].strip().split('\t')[1]
                else:
                    a_word = '[句尾]'
                    a_pos = '[句尾]'
                word_arword = word_arword + '_' + a_word
                pos_arpos   = pos_arpos + '_' + a_pos
                word_arpos  = word_arpos + '_' + a_pos
                pos_arword  = pos_arword + '_' + a_word

            if check_around_pos:
                if wordpos_want=='[pos]':
                    if pos_arpos in wordpos_count_dict:
                        wordpos_count_dict[pos_arpos] += 1
                    else:
                        wordpos_count_dict[pos_arpos] = 1
                elif wordpos_want=='[word]':
                    if word_arpos in wordpos_count_dict:
                        wordpos_count_dict[word_arpos] += 1
                    else:
                        wordpos_count_dict[word_arpos] = 1
            elif check_around_word:
                if wordpos_want=='[pos]':
                    if pos_arword in wordpos_count_dict:
                        wordpos_count_dict[pos_arword] += 1
                    else:
                        wordpos_count_dict[pos_arword] = 1
                elif wordpos_want=='[word]':
                    if word_arword in wordpos_count_dict:
                        wordpos_count_dict[word_arword] += 1
                    else:
                        wordpos_count_dict[word_arword] = 1

        else:
            rowindex += 1

    print('Total Number: ' + str(totalnum))
    sortdict = sorted(wordpos_count_dict.items(), key=lambda s: s[1], reverse=True)
    for key, value in sortdict:
        if value >= 10:
            print(key + '\t' + str(value))

    """绘制错误位置分布图
    plt.ylabel('Frequency')
    plt.xlabel('Relative Position')
    #plt.title('Missing char(s) in one word')
    plt.title('Missing word(s) in a sentence')
    plt.hist(positionlist, bins=100, color='blue', edgecolor='w')
    plt.savefig('分布图-Enhance类型D（纠正类型为I）-删除一个字.jpg')"""

def analyzeErrorType_W_oneword(wordposwant='[pos]'):
    import matplotlib.pyplot as plt
    import pandas as pd

    # genTaggingSeq()
    inpstrs = open(
        'dataEnhance/ErrorTypes/TagSeq_1206-inco+corr-pairs-checked_ANUM.txt.txt', 'r', encoding='utf-8').readlines()

    totalnum = 0
    rowindex = 0
    senindex = 0
    positionlist = list()
    wordpos_count_dict = dict()

    ### 参数设置 ###
    before_tks = 1                 # 记录前面第几个词/词性，<1表示0个，>=1表示1个
    after_tks  = 1                 # 记录后面第几个词/词性，<1表示0个，>=1表示1个
    check_around_pos  = True       # 是否计算相关词性序列
    check_around_word = False      # 是否计算相关词语序列
    # 要计算的词性/词语；
    # - 检查所有词性情况，设置为[pos]
    # - 检查词语情况，设置为[word]
    wordpos_want = wordposwant
    ##############
    while rowindex < len(inpstrs):
        if inpstrs[rowindex].startswith('======='):
            senindex = rowindex+1
            rowindex += 1
        elif isOnlyW1W2(inpstrs[rowindex]) and not '[__W' in inpstrs[rowindex-1] and not '[__W' in inpstrs[rowindex+1] \
              and (wordpos_want=='[pos]' or wordpos_want=='[word]'):
            totalnum += 1
            charcount = countchars(inpstrs, rowindex)
            positionlist.append(float(charcount)/float(len(inpstrs[senindex])-1))

            sstr = inpstrs[rowindex].split('\t')
            word_arword = '[' + sstr[0] + ']'
            word_arpos  = '[' + sstr[0] + ']'
            pos_arpos   = '[' + sstr[1] + ']'
            pos_arword  = '[' + sstr[1] + ']'

            a_word = ''
            a_pos  = ''
            if before_tks >= 1:
                if '[__' in inpstrs[rowindex - 1]:
                    a_word = inpstrs[rowindex - 1].strip().split('\t')[0]
                    a_pos  = inpstrs[rowindex - 1].strip().split('\t')[1]
                else:
                    a_word = '[句首]'
                    a_pos  = '[句首]'
                word_arword = a_word + '_' + word_arword
                pos_arpos   = a_pos  + '_' + pos_arpos
                word_arpos  = a_pos  + '_' + word_arpos
                pos_arword  = a_word + '_' + pos_arword
            if after_tks >= 1:
                if '[__' in inpstrs[rowindex + 1]:
                    a_word = inpstrs[rowindex + 1].strip().split('\t')[0]
                    a_pos = inpstrs[rowindex + 1].strip().split('\t')[1]
                else:
                    a_word = '[句尾]'
                    a_pos = '[句尾]'
                word_arword = word_arword + '_' + a_word
                pos_arpos   = pos_arpos + '_' + a_pos
                word_arpos  = word_arpos + '_' + a_pos
                pos_arword  = pos_arword + '_' + a_word

            if check_around_pos:
                if wordpos_want=='[pos]':
                    if pos_arpos in wordpos_count_dict:
                        wordpos_count_dict[pos_arpos] += 1
                    else:
                        wordpos_count_dict[pos_arpos] = 1
                elif wordpos_want=='[word]':
                    if word_arpos in wordpos_count_dict:
                        wordpos_count_dict[word_arpos] += 1
                    else:
                        wordpos_count_dict[word_arpos] = 1
            elif check_around_word:
                if wordpos_want=='[pos]':
                    if pos_arword in wordpos_count_dict:
                        wordpos_count_dict[pos_arword] += 1
                    else:
                        wordpos_count_dict[pos_arword] = 1
                elif wordpos_want=='[word]':
                    if word_arword in wordpos_count_dict:
                        wordpos_count_dict[word_arword] += 1
                    else:
                        wordpos_count_dict[word_arword] = 1

            rowindex += 1
        else:
            rowindex += 1

    print('Total Number: ' + str(totalnum))
    sortdict = sorted(wordpos_count_dict.items(), key=lambda s: s[1], reverse=True)
    for key, value in sortdict:
        if value >= 5:
            print(key + '\t' + str(value))

    """绘制错误位置分布图
    plt.ylabel('Frequency')
    plt.xlabel('Relative Position')
    plt.title('Swap chars within one word')
    plt.hist(positionlist, bins=100, color='blue', edgecolor='w')
    plt.savefig('分布图-Enhance类型W-单个词.jpg')"""

def analyzeErrorType_W_mulword(wordposwant='[pos]'):
    import matplotlib.pyplot as plt
    import pandas as pd

    # genTaggingSeq()
    inpstrs = open(
        'dataEnhance/ErrorTypes/TagSeq_1206-inco+corr-pairs-checked_ANUM.txt','r', encoding='utf-8').readlines()

    totalnum = 0
    rowindex = 0
    senindex = 0
    positionlist = list()
    wordpos_count_dict = dict()

    ### 参数设置 ###
    before_tks = 1                 # 记录前面第几个词/词性，<1表示0个，>=1表示1个
    after_tks  = 1                 # 记录后面第几个词/词性，<1表示0个，>=1表示1个
    check_around_pos  = True      # 是否计算相关词性序列
    check_around_word = True       # 是否计算相关词语序列
    # 要计算的词性/词语:
    # - 检查所有词性情况，设置为[pos]
    # - 检查词语情况，设置为[word]
    wordpos_want = wordposwant
    ##############
    while rowindex < len(inpstrs):
        if inpstrs[rowindex].startswith('======='):
            senindex = rowindex+1
            rowindex += 1
        elif isOnlyW1(inpstrs[rowindex]) and not isOnlyW1(inpstrs[rowindex-1]) and \
                (wordpos_want=='[word]' or wordpos_want=='[pos]'):
            sstr = inpstrs[rowindex].split('\t')
            word_arword = sstr[0]
            word_arpos  = sstr[0]
            pos_arpos   = sstr[1]
            pos_arword  = sstr[1]

            swapflag = False
            indextmp = rowindex
            rowindex += 1
            while (isOnlyW1(inpstrs[rowindex]) and swapflag==False) or isOnlyW2(inpstrs[rowindex]):
                if isOnlyW1(inpstrs[rowindex]):
                    sstr = inpstrs[rowindex].split('\t')
                    word_arword = word_arword + '+' + sstr[0]
                    word_arpos  = word_arpos + '+' + sstr[0]
                    pos_arpos   = pos_arpos + '+' + sstr[1]
                    pos_arword  = pos_arword + '+' + sstr[1]
                if isOnlyW2(inpstrs[rowindex]):
                    swapflag = True
                    sstr = inpstrs[rowindex].split('\t')
                    arrow = '<->'
                    if arrow in word_arword:
                        arrow = '+'
                    word_arword = word_arword + arrow + sstr[0]
                    word_arpos  = word_arpos + arrow + sstr[0]
                    pos_arpos   = pos_arpos + arrow + sstr[1]
                    pos_arword  = pos_arword + arrow + sstr[1]

                rowindex += 1

            if swapflag == False:
                rowindex = indextmp+1
                continue
            else:
                totalnum += 1
                charcount = countchars(inpstrs, indextmp)
                positionlist.append(float(charcount) / float(len(inpstrs[senindex]) - 1))

                word_arword = '[' + word_arword + ']'
                word_arpos  = '[' + word_arpos + ']'
                pos_arpos   = '[' + pos_arpos + ']'
                pos_arword  = '[' + pos_arword + ']'

                a_word = ''
                a_pos  = ''
                if before_tks >= 1:
                    if '[__' in inpstrs[indextmp - 1]:
                        a_word = inpstrs[indextmp - 1].strip().split('\t')[0]
                        a_pos  = inpstrs[indextmp - 1].strip().split('\t')[1]
                    else:
                        a_word = '[句首]'
                        a_pos  = '[句首]'
                    word_arword = a_word + '_' + word_arword
                    pos_arpos   = a_pos  + '_' + pos_arpos
                    word_arpos  = a_pos  + '_' + word_arpos
                    pos_arword  = a_word + '_' + pos_arword
                if after_tks >= 1:
                    if '[__' in inpstrs[rowindex]:
                        a_word = inpstrs[rowindex].strip().split('\t')[0]
                        a_pos = inpstrs[rowindex].strip().split('\t')[1]
                    else:
                        a_word = '[句尾]'
                        a_pos = '[句尾]'
                    word_arword = word_arword + '_' + a_word
                    pos_arpos   = pos_arpos + '_' + a_pos
                    word_arpos  = word_arpos + '_' + a_pos
                    pos_arword  = pos_arword + '_' + a_word

                if check_around_pos:
                    if wordpos_want=='[pos]':
                        if pos_arpos in wordpos_count_dict:
                            wordpos_count_dict[pos_arpos] += 1
                        else:
                            wordpos_count_dict[pos_arpos] = 1
                    elif wordpos_want=='[word]':
                        if word_arpos in wordpos_count_dict:
                            wordpos_count_dict[word_arpos] += 1
                        else:
                            wordpos_count_dict[word_arpos] = 1
                elif check_around_word:
                    if wordpos_want=='[pos]':
                        if pos_arword in wordpos_count_dict:
                            wordpos_count_dict[pos_arword] += 1
                        else:
                            wordpos_count_dict[pos_arword] = 1
                    elif wordpos_want=='[word]':
                        if word_arword in wordpos_count_dict:
                            wordpos_count_dict[word_arword] += 1
                        else:
                            wordpos_count_dict[word_arword] = 1
        else:
            rowindex += 1

    print('Total Number: ' + str(totalnum))
    sortdict = sorted(wordpos_count_dict.items(), key=lambda s: s[1], reverse=True)
    for key, value in sortdict:
        if value >= 5:
            print(key + '\t' + str(value))

    """绘制错误位置分布图
    plt.ylabel('Frequency')
    plt.xlabel('Relative Position')
    plt.title('Swap multiple words')
    plt.hist(positionlist, bins=100, color='blue', edgecolor='w')
    plt.savefig('分布图-Enhance类型W-多个词.jpg')"""

def analyzeErrorType_R(wordposaround='[pos]'):
    import matplotlib.pyplot as plt
    import pandas as pd

    # genLevenSeq()
    inpstrs = open(
        'dataEnhance/ErrorTypes/TagSeq_1206-inco+corr-pairs-checked_ANUM.txt','r', encoding='utf-8').readlines()

    totalnum = 0
    rowindex = 0
    senindex = 0
    positionlist = list()
    wordpos_count_dict = dict()

    before_tks = 0                # 记录前面的几个词/词性，>=1表示1个，<1表示0个
    after_tks = 1                 # 记录后面的几个词/词性，>=1表示1个，<1表示0个
    # 要计算的词性/词语:
    # - 检查词语情况，设置为[word]
    # - 检查所有词性情况，设置为[pos]
    wordpos_around = wordposaround

    while rowindex < len(inpstrs):
        if inpstrs[rowindex].startswith('======='):
            senindex = rowindex+1
            rowindex += 1
        elif '[__R' in inpstrs[rowindex]:
            totalnum += 1
            charcount = countchars(inpstrs, rowindex)
            positionlist.append(float(charcount)/float(len(inpstrs[senindex])-1))

            sstr = inpstrs[rowindex].strip().split('\t')
            word_rpword_arword = '[' + sstr[0] + ']'
            word_rpword_arpos  = '[' + sstr[0] + ']'

            # 检查词语替换情况
            labels = sstr[2].strip().split('][')
            oldword = sstr[0]
            newword = ''
            for index in range(len(labels)):
                label = labels[index].replace('[__','').replace('__]','').replace('__','')
                if label=='':
                    newword = newword+oldword[index:index+1]
                elif label=='D':
                    newword = newword
                elif label.startswith('R('):
                    newword = newword + label.replace('R(','').replace(')','')
                elif label.startswith('I('):
                    newword = newword + label.replace('I(','').replace(')','') + oldword[index:index+1]
            word_rpword_arword = word_rpword_arword + '->' + newword
            word_rpword_arpos  = word_rpword_arpos + '->' + newword

            if before_tks >= 1:  # 检查前一个词语/词性
                a_word = ''
                a_pos  = ''
                if '[__' in inpstrs[rowindex - 1]:
                    a_word = inpstrs[rowindex - 1].strip().split('\t')[0]
                    a_pos  = inpstrs[rowindex - 1].strip().split('\t')[1]
                else:
                    a_word = '[句首]'
                    a_pos  = '[句首]'
                word_rpword_arword = a_word + '_' + word_rpword_arword
                word_rpword_arpos  = a_pos + '_' + word_rpword_arpos

            if after_tks >= 1:  # 检查后一个词语/词性
                a_word = ''
                a_pos  = ''
                if '[__' in inpstrs[rowindex + 1]:
                    a_word = inpstrs[rowindex + 1].strip().split('\t')[0]
                    a_pos  = inpstrs[rowindex + 1].strip().split('\t')[1]
                else:
                    a_word = '[句尾]'
                    a_pos  = '[句尾]'
                word_rpword_arword = word_rpword_arword + '_' + a_word
                word_rpword_arpos  = word_rpword_arpos + '_' + a_pos

            if wordpos_around=='[word]':
                if word_rpword_arword in wordpos_count_dict:
                    wordpos_count_dict[word_rpword_arword] += 1
                else:
                    wordpos_count_dict[word_rpword_arword] = 1
            else:
                if word_rpword_arpos in wordpos_count_dict:
                    wordpos_count_dict[word_rpword_arpos] += 1
                else:
                    wordpos_count_dict[word_rpword_arpos] = 1

            rowindex += 1
        else:
            rowindex += 1

    print('Total Number: ' + str(totalnum))
    sortdict = sorted(wordpos_count_dict.items(), key=lambda s: s[1], reverse=True)
    for key, value in sortdict:
        if value >= 7:
            print(key + '\t' + str(value))

    """绘制错误位置分布图
    plt.ylabel('Frequency')
    plt.xlabel('Relative Position')
    plt.title('Statistics of word replace')
    plt.hist(positionlist, bins=100, color='blue', edgecolor='w')
    plt.savefig('分布图-Enhance类型R.jpg')"""

def searchPOSTag(inpstrs, str_check):
    # 简单的方法：直接用分词工具获取词性
    seglist = commonTools.postagging(str_check)
    pos = ''
    for w,p in seglist:
        pos = pos+'+'+p

    if pos.startswith('+'):
        return pos[1:]
    else:
        return pos

    """
    # 复杂的方法，从文件里面搜索    
    outfile = open('dataEnhance/ErrorTypes/posfound.txt', 'a+', encoding='utf-8')
    pos_dict = dict()
    for index in range(len(inpstrs)):
        if '[__' not in inpstrs[index]:
            continue
        else:
            slist = inpstrs[index].split('\t')
            if slist[0] == str_check:
                if slist[1] in pos_dict:
                    pos_dict[slist[1]] += 1
                else:
                    pos_dict[slist[1]] = 1
            elif str_check.startswith(slist[0]):
                tmpstr = slist[0]
                tmppos = slist[1]
                for index1 in range(index+1, len(inpstrs)):
                    slist1 = inpstrs[index1].split('\t')
                    if len(slist1)>2 and tmpstr+slist1[0] == str_check:
                        if tmppos+'+'+slist1[1] in pos_dict:
                            pos_dict[tmppos+'+'+slist1[1]] += 1
                        else:
                            pos_dict[tmppos+'+'+slist1[1]] = 1
                    elif str_check.startswith(tmpstr+slist1[0]):
                        tmpstr = tmpstr+slist1[0]
                        tmppos = tmppos+'+'+slist[1]
                    else:
                        break
        if sum(pos_dict.values()) >= 20:
            break

    outfile.write(str_check+'\n')
    outfile.write(str(pos_dict))
    outfile.write('\n')

    if len(pos_dict) == 0:
        seglist = commonTools.postagging(str_check)
        pos = ''
        for w, p in seglist:
            pos = pos + '+' + p
        if pos.startswith('+'):
            return pos[1:]
        else:
            return pos
    else:
        return max(pos_dict, key=pos_dict.get)"""

def getPOSTags(oldword, insertword, inpstrs, senindex):
    """
    # 简单的方法：直接用分词工具获取词性
    seglist = commonTools.postagging(insertword)
    pos = ''
    for w,p in seglist:
        pos = pos+'+'+p

    if pos.startswith('+'):
        return pos[1:]
    else:
        return pos
    """

    # 复杂的方法，从文件里面搜索词性
    newsen = inpstrs[senindex+1]
    seglist = commonTools.postagging(newsen)

    charindex1 = -1
    charindex2 = -1
    while charindex1 < 0:
        charindex2 = newsen.find(oldword, charindex2+1)
        if charindex2<0:
            return searchPOSTag(inpstrs, insertword)
        if newsen[(charindex2-len(insertword)):charindex2] == insertword:
            charindex1 = charindex2-len(insertword)

    charindex = 0
    for listindex in range(len(seglist)):
        word = seglist[listindex][0]
        charindex += len(word)
        if charindex == charindex2:
            listindex1 = listindex
            wordtmp = ''
            posseq = ''
            while not insertword in wordtmp and listindex1>=0:
                wordtmp = seglist[listindex1][0] + wordtmp
                posseq = seglist[listindex1][1] + '+' + posseq
                listindex1 = listindex1 - 1
            if wordtmp==insertword:
                return posseq[:-1]
            else:
                return searchPOSTag(inpstrs, insertword)

    return searchPOSTag(inpstrs, insertword)

def analyzeErrorType_I(wordposwant='[pos]'):
    import matplotlib.pyplot as plt
    import pandas as pd

    # genTaggingSeq()
    inpstrs = open(
        'dataEnhance/ErrorTypes/TagSeq_1206-inco+corr-pairs-checked_ANUM.txt','r', encoding='utf-8').readlines()

    totalnum = 0
    rowindex = 0
    senindex = 0
    positionlist = list()
    wordpos_count_dict = dict()

    ### 参数设置 ###
    check_around_wordpos = 1         # 检查周围的词语/词性，=0表示词语，>0表示词性，<0表示不检查
    check_insert_wordpos = 1          # 检查插入的词语/词性，=0表示词语，其他表示词性
    # 要计算的词性/词语:
    # - 检查词语情况，设置为[word]
    # - 检查所有词性情况，设置为[pos]
    wordpos_want = wordposwant

    while rowindex < len(inpstrs):
        if inpstrs[rowindex].startswith('======='):
            senindex = rowindex+1
            rowindex += 1
        elif '\t[__I(' in inpstrs[rowindex] and not ')__][__I' in inpstrs[rowindex] and \
                (wordpos_want=='[word]' or wordpos_want=='[pos]'):
            totalnum += 1
            charcount = countchars(inpstrs, rowindex)
            positionlist.append(float(charcount)/float(len(inpstrs[senindex])-1))

            sstr = inpstrs[rowindex].strip().split('\t')
            arword_irword_word = '[' + sstr[0] + ']'
            arword_irpos_word  = '[' + sstr[0] + ']'
            arpos_irpos_word   = '[' + sstr[0] + ']'
            arpos_irword_word  = '[' + sstr[0] + ']'
            arword_irword_pos  = '[' + sstr[1] + ']'
            arword_irpos_pos   = '[' + sstr[1] + ']'
            arpos_irpos_pos    = '[' + sstr[1] + ']'
            arpos_irword_pos   = '[' + sstr[1] + ']'

            if check_insert_wordpos >= 0:
                label = sstr[2].strip()
                wordpos1 = label.find('I(') + 2
                wordpos2 = label.find(')', wordpos1)
                insertword = label[wordpos1:wordpos2]
                insertpos = getPOSTags(sstr[0], insertword, inpstrs, senindex)
                arword_irword_word = '{' + insertword + '}' + arword_irword_word
                arword_irpos_word  = '{' + insertpos + '}' + arword_irpos_word
                arpos_irpos_word   = '{' + insertpos + '}' + arpos_irpos_word
                arpos_irword_word  = '{' + insertword + '}' + arpos_irword_word
                arword_irword_pos  = '{' + insertword + '}' + arword_irword_pos
                arword_irpos_pos   = '{' + insertpos + '}' + arword_irpos_pos
                arpos_irpos_pos    = '{' + insertpos + '}' + arpos_irpos_pos
                arpos_irword_pos   = '{' + insertword + '}' + arpos_irword_pos

            if check_around_wordpos >= 0:
                if '[__' in inpstrs[rowindex - 1]:
                    a_word = inpstrs[rowindex - 1].strip().split('\t')[0]
                    a_pos  = inpstrs[rowindex - 1].strip().split('\t')[1]
                else:
                    a_word = '[句首]'
                    a_pos  = '[句首]'
                arword_irword_word = a_word + '_' + arword_irword_word
                arword_irpos_word  = a_word + '_' + arword_irpos_word
                arpos_irpos_word   = a_pos + '_' + arpos_irpos_word
                arpos_irword_word  = a_pos + '_' + arpos_irword_word
                arword_irword_pos  = a_word + '_' + arword_irword_pos
                arword_irpos_pos   = a_word + '_' + arword_irpos_pos
                arpos_irpos_pos    = a_pos + '_' + arpos_irpos_pos
                arpos_irword_pos   = a_pos + '_' + arpos_irword_pos

            if wordpos_want=='[word]':
                if check_insert_wordpos==0:
                    if check_around_wordpos==0:
                        if arword_irword_word in wordpos_count_dict:
                            wordpos_count_dict[arword_irword_word] += 1
                        else:
                            wordpos_count_dict[arword_irword_word] = 1
                    else:
                        if arpos_irword_word in wordpos_count_dict:
                            wordpos_count_dict[arpos_irword_word] += 1
                        else:
                            wordpos_count_dict[arpos_irword_word] = 1
                else:
                    if check_around_wordpos==0:
                        if arword_irpos_word in wordpos_count_dict:
                            wordpos_count_dict[arword_irpos_word] += 1
                        else:
                            wordpos_count_dict[arword_irpos_word] = 1
                    else:
                        if arpos_irpos_word in wordpos_count_dict:
                            wordpos_count_dict[arpos_irpos_word] += 1
                        else:
                            wordpos_count_dict[arpos_irpos_word] = 1
            else:
                if check_insert_wordpos==0:
                    if check_around_wordpos==0:
                        if arword_irword_pos in wordpos_count_dict:
                            wordpos_count_dict[arword_irword_pos] += 1
                        else:
                            wordpos_count_dict[arword_irword_pos] = 1
                    else:
                        if arpos_irword_pos in wordpos_count_dict:
                            wordpos_count_dict[arpos_irword_pos] += 1
                        else:
                            wordpos_count_dict[arpos_irword_pos] = 1
                else:
                    if check_around_wordpos==0:
                        if arword_irpos_pos in wordpos_count_dict:
                            wordpos_count_dict[arword_irpos_pos] += 1
                        else:
                            wordpos_count_dict[arword_irpos_pos] = 1
                    else:
                        if arpos_irpos_pos in wordpos_count_dict:
                            wordpos_count_dict[arpos_irpos_pos] += 1
                        else:
                            wordpos_count_dict[arpos_irpos_pos] = 1

            rowindex += 1
        else:
            rowindex += 1

    print('Total Number: ' + str(totalnum))
    sortdict = sorted(wordpos_count_dict.items(), key=lambda s: s[1], reverse=True)
    for key, value in sortdict:
        if value >= 7:
            print(key + '\t' + str(value))

    """绘制错误位置分布图
    plt.ylabel('Frequency')
    plt.xlabel('Relative Position')
    plt.title('Statistics of word insertion')
    plt.hist(positionlist, bins=100, color='blue', edgecolor='w')
    plt.savefig('分布图-Enhance类型I.jpg')"""

def countNumFreq():
    inpstrs = open(
        'dataEnhance/ErrorTypes/TagSeq_1206-inco+corr-pairs-checked_ANUM.txt', 'r', encoding='utf-8').readlines()
    checklist = open('dataEnhance/ErrorTypes/checklist.txt', 'r', encoding='utf-8').readlines()

    for item in checklist:
        pos_word = item.split('\t')
        senhead = False
        sentail = False
        if len(pos_word) > 1:
            if '[句首]_' in pos_word[0]:
                senhead = True
            if '_[句尾]' in pos_word[0]:   #d_v_[y]_w_[句尾]    102
                sentail = True

            pws = pos_word[0]

            bracketPos1 = pws.find('{')
            bracketPos2 = pws.find('}')
            if bracketPos1>=0 and bracketPos2>bracketPos1:
                pws = pws[0:bracketPos1] + pws[bracketPos2+1:]

            arrowbegin = pws.find(']->')
            if arrowbegin>=0:
                arrowend = pws.find('_', arrowbegin)
                if arrowend < 0:
                    arrowend = len(pws)
                pws = pws[0:arrowbegin] + pws[arrowend:]

            pws = pws.replace('_[句尾]','').replace('[句首]_','').replace('[','').replace(']','')
            pws = pws.replace('+','_').replace('<->','_').split('_')
            num = pos_word[1]
            allnum = 0

            for rowindex in range(3, len(inpstrs)):
                # [句首]_[句首]_[r]_v ==> [r]_v
                if senhead and not inpstrs[rowindex-3].startswith('=========='):
                    continue
                # d_v_[y]_w_[句尾] ==> d_v_[y]_w
                if sentail and (rowindex+len(pws)>=len(inpstrs) or \
                    (rowindex+len(pws)<len(inpstrs) and not inpstrs[rowindex+len(pws)].startswith('=========='))):
                    continue

                if '[__' in inpstrs[rowindex]:
                    sss = inpstrs[rowindex].split('\t')
                    if (sss[0]==pws[0] or sss[1]==pws[0]):
                        flag = True
                        for index1 in range(1, len(pws)):
                            if rowindex+index1<len(inpstrs) and '[__' in inpstrs[rowindex+index1]:
                                sss = inpstrs[rowindex+index1].split('\t')
                                if not (sss[0]==pws[index1] or sss[1]==pws[index1]):
                                    flag = False
                            else:
                                flag=False
                        if flag==True:
                            allnum += 1

            print(item.strip() + '\t' + str(allnum) + '\t' + str(round(float(num) / float(allnum), 6)))
            #outfile.write(posword.strip() + '\t' + str(allnum) + '\t' + str(round(float(num)/float(allnum),6)) + '\n')

if __name__ == '__main__':
    #genTaggingSeq()
    #analyzeErrorType_D()
    #analyzeErrorType_W_oneword()
    #analyzeErrorType_W_mulword()
    #analyzeErrorType_R()
    #analyzeErrorType_I()
    countNumFreq()
