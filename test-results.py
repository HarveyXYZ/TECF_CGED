"""
This file contains the step to analyze the test results
"""

from collections import Counter

def read_text1(input_file):
    lines = []
    with open(input_file, 'r', encoding='utf-8') as f:
        words = []
        labels = []
        for line in f:
            if line.startswith("-DOCSTART-") or line == "" or line == "\n":
                if words:
                    lines.append({"words": words, "labels": labels})
                    words = []
                    labels = []
            else:
                splits = line.split("\t")
                if '' == splits[0].strip():
                    continue

                words.append(splits[0])
                if len(splits) > 1:
                    labels.append(splits[-1].replace("\n", ""))
                else:
                    # Examples could have no label for mode = "test"
                    labels.append("O")
        if words:
            lines.append({"words": words, "labels": labels})

    return lines

def read_text2(input_file):
    str1 = '----------------------------------------'
    lines = []
    with open(input_file, 'r', encoding='utf-8') as f:
        pairs = []
        for line in f:
            line = line.strip()
            if len(line)==0:
                continue
            if line != str1:
                pairs.append(line.split('\t'))
            else:
                if len(pairs) == 0:
                    continue
                assert len(pairs) == 4
                lines.append({"words": pairs[0], "labels": pairs[1]})
                pairs = []

        if len(pairs) == 4:
            lines.append({"words": pairs[0], "labels": pairs[1]})

    return lines

def combSenLabTags():
    sens = open('experiments/outputs_xhh/1207_enhance+real(AUM)_200_32_ce_lert/test-cged.txt',
                'r', encoding='utf-8').readlines()
    tags = open('experiments/outputs_xhh/1207_enhance+real(AUM)_200_32_ce_lert/predict_result.txt',
                'r', encoding='utf-8').readlines()
    oufile = open('experiments/outputs_xhh/1207_enhance+real(AUM)_200_32_ce_lert/predict_result.tr',
                  'w', encoding='utf-8')

    num = 0
    charseq = ''
    tagsseq = ''
    for sss in sens:
        if '	' not in sss:
            if len(charseq) > 0:
                oufile.write(charseq.strip() + '\n')
                oufile.write(tagsseq.strip() + '\n')
                oufile.write(tags[num+2] + '=================\n')
                num = num + 5
                charseq = ''
                tagsseq = ''
        else:
            sss = sss.strip()
            strs = sss.split('	')
            charseq = charseq + '\t' + strs[0]
            tagsseq = tagsseq + '\t' + strs[1]

def test_evaluate():
    data_file1 = 'experiments/outputs_xhh/1207_enhance+real(AUM)_200_32_ce_lert/test-cged.txt'
    data_file2 = 'experiments/outputs_xhh/1207_real(AUM)_200_32_ce_lert/predict_result.txt'

    label_data = read_text1(data_file1)
    pred_data = read_text2(data_file2)
    assert len(label_data) == len(pred_data)

    error_cnt = 0
    #label,predt,right
    cnt_dict = {'D':[0,0,0], 'I':[0,0,0], 'R':[0,0,0], 'W1':[0,0,0], 'W2':[0,0,0], 'AL':[0,0,0]}

    for data1, data2 in zip(label_data, pred_data):
        labels = data1['labels']
        predts = data2['labels']
        if len(labels) != len(predts):
            error_cnt += 1
        else:
            for index in range(0, len(labels)):

                if not (labels[index] == 'O' or labels[index] == 'pad'):
                    cnt_dict[labels[index]][0] += 1
                    if labels[index]==predts[index]:
                        cnt_dict[labels[index]][2] += 1
                if not (predts[index] == 'O' or predts[index] == 'pad'):
                    cnt_dict[predts[index]][1] += 1

    for i in range(0,3):
        cnt_dict['AL'][i] = cnt_dict['D'][i]+cnt_dict['I'][i]+cnt_dict['R'][i]+cnt_dict['W1'][i]+cnt_dict['W2'][i]

    for key,value in cnt_dict.items():
        print(str(key)+'\t'+str(value))
        acc = float(value[2])/float(value[1])
        rec = float(value[2]) / float(value[0])
        f1 = 2*acc*rec/(acc+rec)
        print(key + ':\t' + str(acc)+'\t'+str(rec)+'\t'+str(f1))

    print('\n------------\n')
    print('total numbers:', len(label_data))
    print('error_cnt:', error_cnt)

    print('....')

def detectionlevel():
    data_file1 = 'experiments/outputs_xhh/1207_enhance+real(AUM)_200_32_ce_lert/test-cged.txt'
    data_file2 = 'experiments/outputs_xhh/1207_enhance+real(AUM)_200_32_ce_lert/predict_result.txt'

    label_data = read_text1(data_file1)
    pred_data = read_text2(data_file2)
    assert len(label_data) == len(pred_data)

    error_cnt = 0
    #label,predt,right
    results = [0, 0, 0]

    for data1, data2 in zip(label_data, pred_data):
        labels = data1['labels']
        predts = data2['labels']
        if len(labels) != len(predts):
            error_cnt += 1
        else:
            isLabel = False
            isPredt = False
            for index in range(0, len(labels)):
                if not (labels[index] == 'O' or labels[index] == 'pad'):
                    isLabel = True
                if not (predts[index] == 'O' or predts[index] == 'pad'):
                    isPredt = True
            if isLabel:
                results[0] += 1
            if isPredt:
                results[1] += 1
            if isLabel and isPredt:
                results[2] += 1


    acc = float(results[2])/float(results[1])
    rec = float(results[2]) / float(results[0])
    f1 = 2*acc*rec/(acc+rec)
    print(str(acc)+'\t'+str(rec)+'\t'+str(f1))

    print('\n------------\n')
    print('total numbers:', len(label_data))
    print('error_cnt:', error_cnt)

    print('....')

def identificationlevel():
    data_file1 = 'experiments/outputs_xhh/1207_enhance+real(AUM)_200_32_ce_lert/test-cged.txt'
    data_file2 = 'experiments/outputs_xhh/1207_enhance+real(AUM)_200_32_ce_lert/predict_result.txt'

    label_data = read_text1(data_file1)
    pred_data = read_text2(data_file2)
    assert len(label_data) == len(pred_data)

    error_cnt = 0
    #label,predt,right
    cnt_dict = {'D':[0,0,0], 'I':[0,0,0], 'R':[0,0,0], 'W':[0,0,0], 'AL':[0,0,0]}

    for data1, data2 in zip(label_data, pred_data):
        labels = data1['labels']
        predts = data2['labels']
        if len(labels) != len(predts):
            error_cnt += 1
        else:
            for item in ['D','I','R']:
                if item in labels:
                    cnt_dict[item][0] += 1
                if item in predts:
                    cnt_dict[item][1] += 1
                if item in labels and item in predts:
                    cnt_dict[item][2] += 1

            if 'W1' in labels and 'W2' in labels:
                cnt_dict['W'][0] += 1
                if 'W1' in predts and 'W2' in predts:
                    cnt_dict['W'][2] += 1
            if 'W1' in predts and 'W2' in predts:
                cnt_dict['W'][1] += 1

    for i in range(0,3):
        cnt_dict['AL'][i] = cnt_dict['D'][i]+cnt_dict['I'][i]+cnt_dict['R'][i]+cnt_dict['W'][i]

    for key,value in cnt_dict.items():
        print(str(key)+'\t'+str(value))
        acc = float(value[2])/float(value[1])
        rec = float(value[2]) / float(value[0])
        f1 = 2*acc*rec/(acc+rec)
        print(key + ':\t' + str(acc)+'\t'+str(rec)+'\t'+str(f1))

    print('\n------------\n')
    print('total numbers:', len(label_data))
    print('error_cnt:', error_cnt)

    print('....')

def correctionlevel():
    # precision, recall, f1
    I_list = [0.3785, 0.4027, 0.3902]
    R_list = [0.3918, 0.3125, 0.3476]

    # top1, top3, top5
    toplist = [0.575, 0.7232, 0.7815]
    scale = 1.11
    RtoI = 1.5561

    for i in range(0,3):      # toplist
        print('TOP' + str(2*i+1) + ':')

        prec = (toplist[i]*I_list[0]+toplist[i]*R_list[0]*RtoI)*scale/(1.0+RtoI)
        recl = (toplist[i]*I_list[1]+toplist[i]*R_list[1]*RtoI)*scale/(1.0+RtoI)
        f1 = (toplist[i]*I_list[2]+toplist[i]*R_list[2]*RtoI)*scale/(1.0+RtoI)

        print(str(prec)+' '+str(recl)+' '+str(f1))

def PPLValue():
    resultstr = open('experiments/PPL_results/ppl_result.txt', 'r', encoding='utf-8').readlines()

    same1 = 0
    same3 = 0
    same5 = 0
    same10 = 0
    same15 = 0
    total = 0

    for index in range(len(resultstr)):

        if '============' in resultstr[index]:
            index1 = index-1
            ppllist = dict()
            realcorrection = ''
            while 'pred_tokens' in resultstr[index1]:
                pos1 = resultstr[index1].find('pred_tokens')+15
                pos2 = resultstr[index1].find('ppl')-4
                pos3 = resultstr[index1].find('ppl')+6
                pos4 = resultstr[index1].find('pred_p')-3

                word = resultstr[index1][pos1:pos2]
                value = float(resultstr[index1][pos3:pos4])
                ppllist[word] = value
                realcorrection = word
                index1 = index1 - 1

            sortlist = sorted(ppllist.items(), key=lambda s: s[1], reverse=True)
            rank=0
            for key, value in sortlist:
                rank += 1
                if rank==1:
                    total += 1
                    if key==realcorrection:
                        same1 += 1
                if rank<=3:
                    if key==realcorrection:
                        same3 += 1
                if rank<=5:
                    if key==realcorrection:
                        same5 += 1
                if rank<=10:
                    if key==realcorrection:
                        same10 += 1
                if rank<=15:
                    if key==realcorrection:
                        same15 += 1

    print(same1)
    print(same3)
    print(same5)
    print(same10)
    print(same15)
    print(total)

def longtailfiles():
    filestrs = open('experiments/longtail/mask预测/GECor结果.txt','r',encoding='utf-8').readlines()
    outfile  = open('experiments/longtail/mask预测/GECor结果_1.txt','w',encoding='utf-8')

    for index in range(len(filestrs)):
        if '==========' in filestrs[index]:
            strs = filestrs[index+1].strip()
            ssss = strs.split(' ')
            wlist = list()
            tlist = list()

            for index1 in range(len(ssss)):
                if ssss[index1]=='[D]' or ssss[index1]=='[I]' or ssss[index1]=='[R]' or ssss[index1]=='[W1]' or ssss[index1]=='[W2]':
                    tlist.append(ssss[index1])
                    wlist.append(ssss[index1+1])
                elif index1==0 or not (ssss[index1-1]=='[D]' or ssss[index1-1]=='[I]' or ssss[index1-1]=='[R]' or ssss[index1-1]=='[W1]' or ssss[index1-1]=='[W2]'):
                    tlist.append('O')
                    wlist.append(ssss[index1])

            assert(len(wlist)==len(tlist))

            tokenlist = list()
            index2 = index+2
            tokens = list()
            while index2<len(filestrs) and ('pred_' in filestrs[index2] or '-----' in filestrs[index2]):
                if 'pred_' in filestrs[index2]:
                    pos1 = filestrs[index2].find('pred_tokens')+15
                    pos2 = filestrs[index2].find('pred_p') - 4
                    tokens.append(filestrs[index2][pos1:pos2])
                if '-----' in filestrs[index2] and len(tokens)>0:
                    tokenlist.append(tokens)
                    tokens = list()

                index2 += 1
            if len(tokens) > 0:
                tokenlist.append(tokens)

            IRNum = 0
            index3 = 0
            while index3 < len(tlist):
                if tlist[index3]=='[I]':
                    if len(tokenlist) > 0:
                        outfile.write(wlist[index3]+'	')
                        for item in tokenlist[IRNum]:
                            outfile.write('I('+item+') ')
                        outfile.write('\n')
                        IRNum += 1
                        index3+= 1
                    else:
                        outfile.write(wlist[index3] + '	')
                        outfile.write(tlist[index3] + '()\n')
                        index3 += 1
                elif tlist[index3]=='[R]':
                    if len(tokenlist) > 0:
                        IRCount = 1
                        index4 = index3+1
                        while tlist[index4]=='[R]' or tlist[index4]=='[D]':
                            if tlist[index4]=='[R]':
                                IRCount += 1
                            index4 += 1
                        if tlist[index4-1] == '[D]':
                            index4 = index4 - 1
                        if tlist[index4]=='[I]':
                            index4 += 1
                            IRCount += 1
                        if IRCount==1:
                            outfile.write(wlist[index3] + '	')
                            for item in tokenlist[IRNum]:
                                outfile.write('R(' + item + ') ')
                            outfile.write('\n')
                        if IRCount==2:
                            for index5 in range(index3, index4):
                                if tlist[index5]=='[I]':
                                    outfile.write(wlist[index5] + '	')
                                    for item in tokenlist[IRNum]:
                                        outfile.write('I(' + item[1:] + ') ')
                                    outfile.write('\n')
                                elif tlist[index5]=='[R]':
                                    outfile.write(wlist[index5] + '	')
                                    if index5==index3:
                                        for item in tokenlist[IRNum]:
                                            outfile.write('R(' + item[:1] + ') ')
                                    else:
                                        for item in tokenlist[IRNum]:
                                            outfile.write('R(' + item[1:] + ') ')
                                    outfile.write('\n')
                                else:
                                    outfile.write(wlist[index5] + '	')
                                    outfile.write(tlist[index5] + '\n')
                        if IRCount==3:
                            count = 0
                            for index5 in range(index3, index4):
                                if tlist[index5]=='[I]':
                                    outfile.write(wlist[index5] + '	')
                                    for item in tokenlist[IRNum]:
                                        outfile.write('I(' + item[2:] + ') ')
                                    outfile.write('\n')
                                elif tlist[index5]=='[R]':
                                    outfile.write(wlist[index5] + '	')
                                    for item in tokenlist[IRNum]:
                                        outfile.write('R(' + item[count:count+1] + ') ')
                                    count+=1
                                    outfile.write('\n')
                                else:
                                    outfile.write(wlist[index5] + '	')
                                    outfile.write(tlist[index5] + '\n')

                        IRNum += 1
                        index3 = index4
                    else:
                        outfile.write(wlist[index3] + '	')
                        outfile.write(tlist[index3] + '()\n')
                        index3 += 1

                else:
                    outfile.write(wlist[index3] + '	')
                    outfile.write(tlist[index3] + '\n')
                    index3 += 1

            outfile.write('\n')

if __name__ == '__main__':
    #test_evaluate()
    #detectionlevel()
    #identificationlevel()
    #correctionlevel()
    #PPLValue()
    """
    longtailfiles()

    """
    filestrs1 = open('experiments/longtail/mask预测/GECor结果_1.txt','r',encoding='utf-8').readlines()
    filestrs2 = open('experiments/longtail/mask预测/limit1010-test.txt','r',encoding='utf-8').readlines()

    for index in range(len(filestrs1)):
        if filestrs1[index].startswith('[UNK]'):
            continue
        elif len(filestrs1[index])<2 or len(filestrs2[index])<2:
            continue
        elif filestrs1[index][:2]==filestrs2[index][:2]:
            continue
        else:
            print(index)
            break