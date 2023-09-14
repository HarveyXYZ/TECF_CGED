import opencc
import random
cc = opencc.OpenCC('t2s')

def CGEDdataProcess1(infilepath, oufilepath):
    infile = open(infilepath, 'r', encoding='utf-8')
    oufile = open(oufilepath, 'w', encoding='utf-8')

    instrs = infile.readlines()

    sens = list()
    cors = list()
    for str in instrs:
        if str.startswith('<ESSAY'):
            if len(sens) > 0:
                if len(sens) != len(cors):
                    print(str)
                else:
                    for index in range(0, len(sens)):
                        oufile.write(sens[index] + '\n')
                        oufile.write(cors[index] + '\n')
                        oufile.write('NA-NA-NA-NA-NA-NA-NA-NA-NA-NA\n====================\n')
            sens.clear()
            cors.clear()
        if str.startswith('<SENTENCE'):
            pos = str.find('>')
            str = str[pos + 1:]
            str = str.replace('</SENTENCE>', '').strip()
            str = cc.convert(str)
            sens.append(str)
        if str.startswith('<CORRECTION>'):
            str = str.replace('<CORRECTION>', '')
            str = str.replace('</CORRECTION>', '').strip()
            str = cc.convert(str)
            cors.append(str)

def CGEDdataProcess2(infileInput, infileTruth, oufilepath):
    inputStrs = open(infileInput, 'r', encoding='utf-8').readlines()
    truthStrs = open(infileTruth, 'r', encoding='utf-8').readlines()
    oufile = open(oufilepath, 'w', encoding='utf-8')

    for index in range(0, len(inputStrs)):
        if '	' in inputStrs[index]:
            ss1 = inputStrs[index].split('	')
            sen = cc.convert(ss1[1].strip())
            orgsen = sen
            insertNum = 0
            for str in truthStrs:
                ss2 = str.replace('	', '').replace(' ', '').split(',')
                if ss2[0].strip() in ss1[0]:
                    if 'correct' in ss2[1]:
                        insertNum = -1
                    else:
                        print(ss2)
                        sPos = int(ss2[1].strip()) - 1
                        ePos = int(ss2[2].strip()) - 1
                        if ss2[3].startswith('S'):
                            for pos in range(sPos, ePos+1):
                                nPos = pos + insertNum * 3
                                insertNum = insertNum + 1
                                sen = sen[:nPos] + '[R]' + sen[nPos:]
                        elif ss2[3].startswith('R'):
                            for pos in range(sPos, ePos+1):
                                nPos = pos + insertNum * 3
                                insertNum = insertNum + 1
                                sen = sen[:nPos] + '[D]' + sen[nPos:]
                        elif ss2[3].startswith('M'):
                            #for pos in range(sPos, ePos+1):
                            nPos = sPos + insertNum * 3
                            insertNum = insertNum + 1
                            sen = sen[:nPos] + '[I]' + sen[nPos:]
                        elif ss2[3].startswith('W') or ss2[3].startswith('D'):
                            for pos in range(sPos, ePos+1):
                                nPos = pos + insertNum * 3
                                insertNum = insertNum + 1
                                sen = sen[:nPos] + '[W]' + sen[nPos:]

            if insertNum == -1:
                oufile.write(orgsen + '\n' + orgsen + '\n')
                oufile.write('CORRECT-CORRECT-CORRECT\n====================\n')
            if insertNum > 0:
                oufile.write(orgsen + '\nNA-NA-NA-NA-NA-NA-NA-NA-NA-NA\n')
                oufile.write(sen + '\n====================\n')

def CGEDdataProcess3(infilepath, oufilepath):
    infile = open(infilepath, 'r', encoding='utf-8')
    oufile = open(oufilepath, 'w', encoding='utf-8')

    instrs = infile.readlines()

    sen = ''
    cor = ''
    sta = list()
    end = list()
    typ = list()
    num = 0

    for str in instrs:
        if str.startswith('</DOC'):
            if len(typ) > 0:
                oufile.write(sen + '\n')
                oufile.write(cor + '\n')
                num = 0
                for index in range(0, len(typ)):
                    spos = sta[index]
                    epos = end[index]
                    if typ[index] == 'Missing':
                        pos = 3 * num + spos
                        sen = sen[:pos] + '[I]' + sen[pos:]
                        num = num + 1
                    else:
                        for p in range(spos, epos + 1):
                            pos = 3 * num + p
                            if typ[index] == 'Selection':
                                sen = sen[:pos] + '[R]' + sen[pos:]
                                num = num + 1
                            if typ[index] == 'Disorder':
                                sen = sen[:pos] + '[W]' + sen[pos:]
                                num = num + 1
                            if typ[index] == 'Redundant':
                                sen = sen[:pos] + '[D]' + sen[pos:]
                                num = num + 1

                oufile.write(sen + '\n====================\n')
                sen = ''
                cor = ''
                sta = list()
                end = list()
                typ = list()
                num = 0

        elif str.startswith('<SENTENCE'):
            spos = str.find('>')
            epos = str.find('</SENTENCE>')
            sen = cc.convert(str[spos+1 : epos].strip())

        elif str.startswith('<CORRECTION>'):
            spos = str.find('>')
            epos = str.find('</CORRECTION>')
            cor = cc.convert(str[spos+1 : epos].strip())

        elif str.startswith('<MISTAKE'):
            spos1 = str.find('start_off') + 11
            epos1 = str.find('end_off') - 2
            spos2 = str.find('end_off') + 9
            epos2 = str.find('>') - 1
            sta.append(int(str[spos1:epos1])-1)
            end.append(int(str[spos2:epos2])-1)

        elif str.startswith('<TYPE'):
            spos = str.find('>')
            epos = str.find('</TYPE>')
            typ.append(str[spos+1:epos])

def CGEDdataProcess4(infilepath, oufilepath):
    infile = open(infilepath, 'r', encoding='utf-8')
    oufile = open(oufilepath, 'w', encoding='utf-8')

    instrs = infile.readlines()

    sen = ''
    cor = ''
    sta = list()
    end = list()
    typ = list()
    num = 0

    for indexStrs in range(0, len(instrs)):
        str = instrs[indexStrs]
        if str.startswith('</DOC'):
            if len(typ) > 0:
                oufile.write(sen + '\n')
                oufile.write(cor + '\n')
                num = 0
                for index in range(0, len(typ)):
                    spos = sta[index]
                    epos = end[index]
                    if typ[index] == 'M':
                        pos = 3 * num + spos
                        sen = sen[:pos] + '[I]' + sen[pos:]
                        num = num + 1
                    else:
                        for p in range(spos, epos + 1):
                            pos = 3 * num + p
                            if typ[index] == 'S':
                                sen = sen[:pos] + '[R]' + sen[pos:]
                                num = num + 1
                            if typ[index] == 'W':
                                sen = sen[:pos] + '[W]' + sen[pos:]
                                num = num + 1
                            if typ[index] == 'R':
                                sen = sen[:pos] + '[D]' + sen[pos:]
                                num = num + 1

                oufile.write(sen + '\n====================\n')
                sen = ''
                cor = ''
                sta = list()
                end = list()
                typ = list()
                num = 0

        elif str.startswith('<TEXT'):
            sen = cc.convert(instrs[indexStrs + 1].strip())

        elif str.startswith('<CORRECTION>'):
            cor = cc.convert(instrs[indexStrs + 1].strip())

        elif str.startswith('<ERROR'):
            spos1 = str.find('start_off') + 11
            epos1 = str.find('end_off') - 2
            spos2 = str.find('end_off') + 9
            epos2 = str.find('type') - 2
            spos3 = str.find('type') + 6
            epos3 = str.find('</ERROR>') - 2
            sta.append(int(str[spos1:epos1])-1)
            end.append(int(str[spos2:epos2])-1)
            typ.append(str[spos3:epos3])

def CGEDdataProcess5(infilepath, oufilepath):
    infile = open(infilepath, 'r', encoding='utf-8')
    oufile = open(oufilepath, 'w', encoding='utf-8')

    instrs = infile.readlines()

    for str in instrs:
        spos = str.find('raw_text') + 12
        if 'correction_text' in str:
            epos = str.find('correction_text') - 4

            sen = str[spos : epos]
            oufile.write(sen + '\n')

            spos = str.find('correction_text') + 19
            epos = str.find('label') - 4
            oufile.write(str[spos: epos] + '\n')
        else:
            epos = str.find('label') - 4

            sen = str[spos: epos]
            oufile.write(sen + '\nNA-NA-NA-NA-NA-NA-NA-NA-NA-NA\n')

        spos = str.find('[{')
        epos = str.find(']}')
        sss = str[spos:epos]

        if '\"correct\"' in sss:
            oufile.write('correct-correct-correct\n====================\n')
        else:
            insnum = 0
            while sss.find('label') > 0:
                spos = sss.find('label') + 9
                epos = sss.find('entity', spos) - 4
                label = sss[spos:epos]
                spos = sss.find('start') + 8
                epos = sss.find('end', spos) - 3
                start = int(sss[spos:epos].strip('\"')) - 1
                spos = sss.find('end') + 6
                epos = sss.find('}', spos)
                end = int(sss[spos:epos].strip('\"')) - 1
                sss = sss[epos:]

                if label == 'M':
                    pos = 3 * insnum + start
                    insnum = insnum + 1
                    sen = sen[:pos] + '[I]' + sen[pos:]

                for p in range(start, end+1):
                    if label == 'R':
                        pos = 3 * insnum + p
                        insnum = insnum + 1
                        sen = sen[:pos] + '[D]' + sen[pos:]
                    elif label == 'W':
                        pos = 3 * insnum + p
                        insnum = insnum + 1
                        sen = sen[:pos] + '[W]' + sen[pos:]
                    elif label == 'S':
                        pos = 3 * insnum + p
                        insnum = insnum + 1
                        sen = sen[:pos] + '[R]' + sen[pos:]

            oufile.write(sen + '\n====================\n')

### raw_data/CGED-DATA-2018/train2018.release1.txt
def CGEDdataProcess6(infilepath, oufilepath):
    infile = open(infilepath, 'r', encoding='utf-8')
    oufile = open(oufilepath, 'w', encoding='utf-8')

    instrs = infile.readlines()

    num = 0
    for str in instrs:
        if '<DOC>' in str:
            num = num + 1
            str = str.replace('	', '')

            spos = str.find('<TEXT')
            str = str[spos:]
            spos = str.find('>') + 1
            epos = str.find('</TEXT>')

            sen = str[spos:epos]
            oufile.write(sen + '\n')

            spos = str.find('<CORRECTION>') + 12
            epos = str.find('</CORRECTION>')
            oufile.write(str[spos:epos] + '\n')

            sss = str[epos:].strip()
            insnum = 0
            while sss.find('<ERROR') >= 0:
                spos = sss.find('end_off') + 9
                epos = sss.find('start_off') - 2
                end = int(sss[spos:epos].strip())

                spos = sss.find('start_off') + 11
                epos = sss.find('type') - 2
                start = int(sss[spos:epos].strip())

                spos = sss.find('type') + 6
                epos = sss.find('/>') - 1
                label = sss[spos:epos].strip()

                sss = sss[epos+2:].strip()
                #print(sss)
                
                if label == 'M':
                    pos = 3 * insnum + start
                    insnum = insnum + 1
                    sen = sen[:pos] + '[I]' + sen[pos:]

                for p in range(start-1, end):
                    if label == 'R':
                        pos = 3 * insnum + p
                        insnum = insnum + 1
                        sen = sen[:pos] + '[D]' + sen[pos:]
                    elif label == 'W':
                        pos = 3 * insnum + p
                        insnum = insnum + 1
                        sen = sen[:pos] + '[W]' + sen[pos:]
                    elif label == 'S':
                        pos = 3 * insnum + p
                        insnum = insnum + 1
                        sen = sen[:pos] + '[R]' + sen[pos:]

            oufile.write(sen + '\n====================\n')

### raw_data/CGED-DATA-2018/train2018.release2.txt
def CGEDdataProcess7(infilepath, oufilepath):
    infile = open(infilepath, 'r', encoding='utf-8')
    oufile = open(oufilepath, 'w', encoding='utf-8')

    instrs = infile.readlines()

    for str in instrs:
        if '<DOC>' in str:
            str = str.replace('	', '')

            spos = str.find('<TEXT')
            str = str[spos:]
            spos = str.find('>') + 1
            epos = str.find('</TEXT>')

            sen = str[spos:epos]
            oufile.write(sen + '\n')

            spos = str.find('<CORRECTION>') + 12
            epos = str.find('</CORRECTION>')
            oufile.write(str[spos:epos] + '\n')

            sss = str[epos:].strip()
            insnum = 0
            while sss.find('<ERROR') >= 0:
                spos = sss.find('start_off') + 11
                epos = sss.find('end_off') - 2
                start = int(sss[spos:epos].strip())

                spos = sss.find('end_off') + 9
                epos = sss.find('type') - 2
                end = int(sss[spos:epos].strip())

                spos = sss.find('type') + 6
                epos = sss.find('</ERROR>') - 2
                label = sss[spos:epos].strip()

                sss = sss[epos + 6:].strip()
                #print(sss)

                if label == 'M':
                    pos = 3 * insnum + start
                    insnum = insnum + 1
                    sen = sen[:pos] + '[I]' + sen[pos:]

                for p in range(start - 1, end):
                    if label == 'R':
                        pos = 3 * insnum + p
                        insnum = insnum + 1
                        sen = sen[:pos] + '[D]' + sen[pos:]
                    elif label == 'W':
                        pos = 3 * insnum + p
                        insnum = insnum + 1
                        sen = sen[:pos] + '[W]' + sen[pos:]
                    elif label == 'S':
                        pos = 3 * insnum + p
                        insnum = insnum + 1
                        sen = sen[:pos] + '[R]' + sen[pos:]

            oufile.write(sen + '\n====================\n')

if __name__ == '__main__':
    #infilepath = 'data/CGED-DATA/raw_data/CGED-DATA-2018/train2018.release2.txt'
    #oufilepath = 'data/CGED-DATA/raw_data/CGED-DATA-2018/raw-train2018.release2.txt'
    #CGEDdataProcess1(infilepath, oufilepath)
    #CGEDdataProcess3(infilepath, oufilepath)
    #CGEDdataProcess4(infilepath, oufilepath)
    #CGEDdataProcess5(infilepath, oufilepath)
    #CGEDdataProcess6(infilepath, oufilepath)
    #CGEDdataProcess7(infilepath, oufilepath)

    """
    infileInput = 'data/CGED-DATA/CGED2021/test_2020-m.txt'
    infileTruth = 'data/CGED-DATA/CGED2021/truth_2020-m.txt'
    oufilepath = 'data/CGED-DATA/CGED2021/2020-test_2020-m.txt'
    CGEDdataProcess2(infileInput, infileTruth, oufilepath)
    """

    inpstrs = open('data_raw/THUCNews/for_training/社会.txt','r',encoding='utf-8').readlines()
    outfile = open('data_raw/THUCNews/for_training/社会_1.txt','w',encoding='utf-8')

    for sstr in inpstrs:
        if len(sstr)>=10 and len(sstr)<250:
            rand = random.randint(1,10)
            if rand==1:
                outfile.write(sstr.strip()+'\n' + sstr.strip()+'\n===========\n')
