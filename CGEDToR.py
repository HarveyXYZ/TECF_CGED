"""
This file contains the model description, data analysis and experimental analysis of CGEDToR
"""


import random

def typestatis():
    inputstrs = open('experiments/CGEDToR/labels-nolimit.txt','r',encoding='utf-8').readlines()

    D_num = 0
    W1_num = 0
    W2_num = 0
    I_total = 0
    R_total = 0
    I_dict = dict()
    R_dict = dict()

    for index in range(len(inputstrs)):
        if inputstrs[index].startswith('======='):
            sss = inputstrs[index-1].strip()
            slist = sss.split(' ')
            for s in slist:
                if '__D' in s:
                    D_num += 1
                if '__W1' in s:
                    W1_num += 1
                if '__W2' in s:
                    W2_num += 1
                if '__I' in s:
                    I_total += 1
                    s = s.replace('[__','').replace('__]','')
                    if s in I_dict:
                        I_dict[s] += 1
                    else:
                        I_dict[s] = 1
                if '__R' in s:
                    R_total += 1
                    s = s.replace('[__','').replace('__]','')
                    if s in R_dict:
                        R_dict[s] += 1
                    else:
                        R_dict[s] = 1

    print(D_num)
    print(W1_num)
    print(W2_num)
    """
    sortdict = sorted(R_dict.items(), key=lambda s: s[1], reverse=True)
    for key, value in sortdict:
        print(key + '\t' + str(value))"""

def genLabelData():
    inputstrs = open('experiments/CGEDToR/labels-nolimit.txt','r',encoding='utf-8').readlines()
    typescount = open('experiments/CGEDToR/类型统计.txt','r',encoding='utf-8').readlines()
    outputfile = open('experiments/CGEDToR/labels-limit1010.txt','w',encoding='utf-8')

    R_dict_match = dict()
    R_dict_occur = dict()
    I_dict_match = dict()
    I_dict_occur = dict()
    R_limit = 10
    I_limit = 10

    for tc in typescount:
        if '	I(' in tc:
            tcc = tc.split('	')
            I_dict_occur['[__'+tcc[1]+'__]'] = int(tcc[2])
            I_dict_match['[__'+tcc[1]+'__]'] = tcc[0]
        if '	R(' in tc:
            tcc = tc.split('	')
            R_dict_occur['[__'+tcc[1]+'__]'] = int(tcc[2])
            R_dict_match['[__'+tcc[1]+'__]'] = tcc[0]

    for index in range(len(inputstrs)):
        if inputstrs[index].startswith('==========='):
            labelseq = inputstrs[index-1].strip()
            seqs = labelseq.split(' ')
            newseq = ''
            for index1 in range(len(seqs)):
                if seqs[index1].startswith('[__'):
                    if seqs[index1].startswith('[__I'):
                        if I_dict_occur[seqs[index1]] >= I_limit:
                            newseq = newseq + ' ' + I_dict_match[seqs[index1]] + ' ' + seqs[index1+1]
                        else:
                            newseq = newseq + ' I0000 ' + seqs[index1+1]
                    elif seqs[index1].startswith('[__R'):
                        if R_dict_occur[seqs[index1]] >= R_limit:
                            newseq = newseq + ' ' + R_dict_match[seqs[index1]] + ' ' + seqs[index1+1]
                        else:
                            newseq = newseq + ' R0000 ' + seqs[index1+1]
                    else:
                        newseq = newseq + ' ' + seqs[index1] + ' ' + seqs[index1+1]
                elif index1==0 or (index1>0 and not seqs[index1-1].startswith('[__')):
                    newseq = newseq + ' [__O__] ' + seqs[index1]

            outputfile.write(inputstrs[index-3])
            outputfile.write(inputstrs[index-2])
            outputfile.write(newseq.strip()+'\n===========\n')

def traindevtest():
    typescount = open('experiments/CGEDToR/类型统计.txt', 'r', encoding='utf-8').readlines()
    R_list = list()
    I_list = list()
    for tc in typescount:
        if '	I(' in tc:
            tcc = tc.strip().split('	')
            I_list.append(tcc[0])
        if '	R(' in tc:
            tcc = tc.strip().split('	')
            R_list.append(tcc[0])

    inputstrs = open('experiments/CGEDToR/labels-limit1010.txt','r',encoding='utf-8').readlines()
    trainfile = open('experiments/CGEDToR/limit1010-train.txt',  'w',encoding='utf-8')
    devfile = open('experiments/CGEDToR/limit1010-dev.txt',    'w',encoding='utf-8')
    testfile = open('experiments/CGEDToR/limit1010-test.txt',   'w',encoding='utf-8')
    train_list = list()
    test_list = list()

    for index in range(len(inputstrs)):
        if inputstrs[index].startswith('======='):
            sss = inputstrs[index-1].strip()
            rand = random.randint(1, 21)
            if rand <= 14:
                train_list.append(sss)
            else:
                test_list.append(sss)

    for r in R_list:
        flag = False
        for tr in train_list:
            if r in tr:
                flag=True
                break
        if flag==False:
            for te in test_list:
                if r in te:
                    train_list.append(te)
                    test_list.remove(te)
                    break

    for i in I_list:
        flag = False
        for tr in train_list:
            if i in tr:
                flag=True
                break
        if flag==False:
            for te in test_list:
                if i in te:
                    train_list.append(te)
                    test_list.remove(te)
                    break

    for tr in train_list:
        ttr = tr.split(' ')
        for index in range(0,len(ttr),2):
            trainfile.write(ttr[index+1]+'\t'+ttr[index].replace('[__','').replace('__]','')+'\n')
        trainfile.write('\n')
    for te in test_list:
        tte = te.split(' ')
        rand=random.randint(1,2)
        if rand==1:
            for index in range(0,len(tte),2):
                devfile.write(tte[index+1]+'\t'+tte[index].replace('[__','').replace('__]','')+'\n')
            devfile.write('\n')
        else:
            for index in range(0, len(tte), 2):
                testfile.write(tte[index + 1] + '\t' + tte[index].replace('[__', '').replace('__]', '') + '\n')
            testfile.write('\n')

def readlabeldata(filepath):
    filestrs = open(filepath, 'r', encoding='utf-8').readlines()
    labellist = list()

    labels = list()
    for index in range(len(filestrs)):
        sss = filestrs[index].strip()
        if '	' in sss:
            ss = sss.split('	')
            labels.append(ss[1])
        elif labels:
            labellist.append(labels)
            labels = list()

    if labels:
        labellist.append(labels)

    return labellist

def readpredtdata(filepath):
    filestrs = open(filepath, 'r', encoding='utf-8').readlines()
    labellist = list()

    for index in range(len(filestrs)):
        sss = filestrs[index].strip()
        if 'tag_seq' in sss:
            pos1 = sss.find('tag_seq') + 11
            pos2 = sss.find('entities') - 4
            ss = sss[pos1:pos2].split(' ')
            labellist.append(ss)

    return labellist

def readpredtdata_TECF(filepath):
    filestrs = open(filepath, 'r', encoding='utf-8').readlines()
    labellist = list()

    for index in range(len(filestrs)):
        if '-----------' in filestrs[index]:
            sss = filestrs[index+2].strip()
            ss = sss.split('	')
            labellist.append(ss)

    return labellist

def test_evaluate():
    label_data = readlabeldata('experiments/CGEDToR/limit1010-test.txt')
    predt_data = readpredtdata('experiments/CGEDToR/test_prediction.json')
    assert len(label_data) == len(predt_data)

    Label_R_list = list()
    Label_I_list = list()
    Predt_R_list = list()
    Predt_I_list = list()
    for ld in label_data:
        for l in ld:
            if l.startswith('I') and not l in Label_I_list:
                Label_I_list.append(l)
            if l.startswith('R') and not l in Label_R_list:
                Label_R_list.append(l)
    for pd in predt_data:
        for p in pd:
            if p.startswith('I') and not p in Predt_I_list:
                Predt_I_list.append(p)
            if p.startswith('R') and not p in Predt_R_list:
                Predt_R_list.append(p)

    error_cnt = 0
    #label,predt,right
    cnt_dict = dict()
    cnt_dict['D'] = [0, 0, 0]
    cnt_dict['W1'] = [0, 0, 0]
    cnt_dict['W2'] = [0, 0, 0]
    for il in Label_I_list:
        cnt_dict[il] = [0, 0, 0]
    for rl in Label_R_list:
        cnt_dict[rl] = [0, 0, 0]
    for il in Predt_I_list:
        cnt_dict[il] = [0, 0, 0]
    for rl in Predt_R_list:
        cnt_dict[rl] = [0, 0, 0]

    for labels, predts in zip(label_data, predt_data):
        if len(labels) != len(predts):
            error_cnt += 1
            print(predts)
            #print(len(predts))
        else:
            for index in range(0, len(labels)):
                if not (labels[index] == 'O' or labels[index] == 'pad'):
                    cnt_dict[labels[index]][0] += 1
                    if labels[index]==predts[index]:
                        cnt_dict[labels[index]][2] += 1
                if not (predts[index] == 'O' or predts[index] == 'pad'):
                    cnt_dict[predts[index]][1] += 1

    AL_labels = 0
    AL_predts = 0
    AL_rights = 0
    for key, value in cnt_dict.items():
        AL_labels += value[0]
        AL_predts += value[1]
        AL_rights += value[2]
    acc = float(AL_rights) / float(AL_predts)
    rec = float(AL_rights) / float(AL_labels)
    f1 = 2 * acc * rec / (acc + rec)
    print(str(AL_labels) + '\t' + str(AL_predts) + '\t' + str(AL_rights))
    print('ALL: ' + str(acc) + '\t' + str(rec) + '\t' + str(f1))


    for key,value in cnt_dict.items():
        #print(str(key)+'\t'+str(value))
        if value[1]==0 or value[0]==0:
            acc=0.0
            rec=0.0
            f1=0.0
        else:
            acc = float(value[2]) / float(value[1])
            rec = float(value[2]) / float(value[0])
            if acc+rec==0.0:
                f1=0.0
            else:
                f1 = 2 * acc * rec / (acc + rec)
        print(key + ':\t' + str(acc)+'\t'+str(rec)+'\t'+str(f1))

    print('\n------------\n')
    print('total numbers:', len(label_data))
    print('error_cnt:', error_cnt)

    print('....')

def test_evaluate_TECF():
    label_data = readlabeldata('experiments/longtail/makedata-IRnotinreal-test.txt')
    #predt_data = readpredtdata_TECF('experiments/CGEDToR/predict_result_TECF.txt')
    predt_data = readpredtdata_TECF('experiments/longtail/predict_result.txt')
    label_data == label_data[0 : len(predt_data)]

    Label_R_list = list()
    Label_I_list = list()
    for ld in label_data:
        for l in ld:
            if l.startswith('I') and not l in Label_I_list:
                Label_I_list.append(l)
            if l.startswith('R') and not l in Label_R_list:
                Label_R_list.append(l)

    error_cnt = 0
    #label,predt,right
    cnt_dict = dict()
    cnt_dict['D'] = [0, 0, 0]
    cnt_dict['W1'] = [0, 0, 0]
    cnt_dict['W2'] = [0, 0, 0]
    totalI = 0
    totalI_right = 0
    totalR = 0
    totalR_right = 0
    for il in Label_I_list:
        cnt_dict[il] = [0, 0, 0]
    for rl in Label_R_list:
        cnt_dict[rl] = [0, 0, 0]

    for labels, predts in zip(label_data, predt_data):
        if len(labels) != len(predts):
            error_cnt += 1
            #print(predts)
            #print(len(predts))
        else:
            for index in range(0, len(labels)):
                if labels[index] == 'D' or labels[index].startswith('W'):
                    cnt_dict[labels[index]][0] += 1
                    if labels[index]==predts[index]:
                        cnt_dict[labels[index]][2] += 1
                if predts[index] == 'D' or predts[index].startswith('W'):
                    cnt_dict[predts[index]][1] += 1

                if labels[index].startswith('I'):
                    cnt_dict[labels[index]][0] += 1
                    if predts[index].startswith('I'):
                        cnt_dict[labels[index]][2] += 1
                        totalI_right += 1
                if predts[index].startswith('I'):
                    totalI += 1

                if labels[index].startswith('R'):
                    cnt_dict[labels[index]][0] += 1
                    if predts[index].startswith('R'):
                        cnt_dict[labels[index]][2] += 1
                        totalR_right += 1
                if predts[index].startswith('R'):
                    totalR += 1

    """
    AL_labels = 0
    AL_predts = 0
    AL_rights = 0
    for key, value in cnt_dict.items():
        AL_labels += value[0]
        AL_predts += value[1]
        AL_rights += value[2]
    acc = float(AL_rights) / float(AL_predts)
    rec = float(AL_rights) / float(AL_labels)
    f1 = 2 * acc * rec / (acc + rec)
    print(str(AL_labels) + '\t' + str(AL_predts) + '\t' + str(AL_rights))
    print('ALL: ' + str(acc) + '\t' + str(rec) + '\t' + str(f1))"""

    print(float(totalI))
    print(float(totalR))
    print(float(totalI_right) / float(totalI))
    print(float(totalR_right) / float(totalR))

    for key,value in cnt_dict.items():
        #print(str(key)+'\t'+str(value))
        if key.startswith('I') or key.startswith('R'):
            acc = 0.0
        else:
            acc = float(value[2]) / float(value[1])
        rec = float(value[2]) / float(value[0])
        if acc+rec==0.0:
            f1=0.0
        else:
            f1 = 2 * acc * rec / (acc + rec)
        print(key + ':\t' + str(acc)+'\t'+str(rec)+'\t'+str(f1))

    print('\n------------\n')
    print('total numbers:', len(label_data))
    print('error_cnt:', error_cnt)

    print('....')


def detection_level():
    label_data = readlabeldata('experiments/CGEDToR/limit1010-test.txt')
    predt_data = readpredtdata('experiments/CGEDToR/test_prediction.json')
    assert len(label_data) == len(predt_data)

    error_cnt = 0
    results = [0, 0, 0]
    for labels, predts in zip(label_data, predt_data):
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

    acc = float(results[2]) / float(results[1])
    rec = float(results[2]) / float(results[0])
    f1 = 2 * acc * rec / (acc + rec)
    print(str(results[0]) + '\t' + str(results[1]) + '\t' + str(results[2]))
    print('ALL: ' + str(acc) + '\t' + str(rec) + '\t' + str(f1))

    print('\n------------\n')
    print('total numbers:', len(label_data))
    print('error_cnt:', error_cnt)

    print('....')

def identification_level():
    label_data = readlabeldata('experiments/CGEDToR/limit1010-test.txt')
    predt_data = readpredtdata('experiments/CGEDToR/test_prediction.json')
    assert len(label_data) == len(predt_data)

    error_cnt = 0
    #label,predt,right
    cnt_dict = dict()
    cnt_dict['D'] = [0, 0, 0]
    cnt_dict['W'] = [0, 0, 0]
    cnt_dict['I'] = [0, 0, 0]
    cnt_dict['R'] = [0, 0, 0]

    for labels, predts in zip(label_data, predt_data):
        if len(labels) != len(predts):
            error_cnt += 1
        else:
            for index in range(len(labels)):
                if labels[index].startswith('I'):
                    labels[index] = 'I'
                if labels[index].startswith('R'):
                    labels[index] = 'R'
            for index in range(len(predts)):
                if predts[index].startswith('I'):
                    predts[index] = 'I'
                if predts[index].startswith('R'):
                    predts[index] = 'R'

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

    AL_labels = 0
    AL_predts = 0
    AL_rights = 0
    for key, value in cnt_dict.items():
        AL_labels += value[0]
        AL_predts += value[1]
        AL_rights += value[2]
    acc = float(AL_rights) / float(AL_predts)
    rec = float(AL_rights) / float(AL_labels)
    f1 = 2 * acc * rec / (acc + rec)
    print(str(AL_labels) + '\t' + str(AL_predts) + '\t' + str(AL_rights))
    print('ALL: ' + str(acc) + '\t' + str(rec) + '\t' + str(f1))

    for key,value in cnt_dict.items():
        #print(str(key)+'\t'+str(value))
        if value[1]==0 or value[0]==0:
            acc = 0.0
            rec = 0.0
            f1  = 0.0
        else:
            acc = float(value[2]) / float(value[1])
            rec = float(value[2]) / float(value[0])
            if acc+rec==0.0:
                f1=0.0
            else:
                f1 = 2 * acc * rec / (acc + rec)
        print(key + ':\t' + str(acc)+'\t'+str(rec)+'\t'+str(f1))

    print('\n------------\n')
    print('total numbers:', len(label_data))
    print('error_cnt:', error_cnt)

    print('....')

def position_level():
    label_data = readlabeldata('experiments/CGEDToR/limit1010-dev.txt')
    predt_data = readpredtdata('experiments/CGEDToR/dev_prediction.json')
    #eval_data = readpredtdata('experiments/CGEDToR/test_prediction.json')
    assert len(label_data) == len(predt_data)

    error_cnt = 0
    #label,predt,right
    cnt_dict = dict()
    cnt_dict['D'] = [0, 0, 0]
    cnt_dict['W'] = [0, 0, 0]
    cnt_dict['I'] = [0, 0, 0]
    cnt_dict['R'] = [0, 0, 0]

    for labels, predts in zip(label_data, predt_data):
        if len(labels) != len(predts):
            error_cnt += 1
        else:
            for index in range(len(labels)):
                if labels[index].startswith('I'):
                    labels[index] = 'I'
                if labels[index].startswith('R'):
                    labels[index] = 'R'
                if labels[index].startswith('W'):
                    labels[index] = 'W'
            for index in range(len(predts)):
                if predts[index].startswith('I'):
                    predts[index] = 'I'
                if predts[index].startswith('R'):
                    predts[index] = 'R'
                if predts[index].startswith('W'):
                    predts[index] = 'W'

            for index in range(0, len(labels)):
                if not (labels[index] == 'O' or labels[index] == 'pad'):
                    cnt_dict[labels[index]][0] += 1
                    if labels[index]==predts[index]:
                        cnt_dict[labels[index]][2] += 1
                if not (predts[index] == 'O' or predts[index] == 'pad'):
                    cnt_dict[predts[index]][1] += 1

    AL_labels = 0
    AL_predts = 0
    AL_rights = 0
    for key, value in cnt_dict.items():
        AL_labels += value[0]
        AL_predts += value[1]
        AL_rights += value[2]
    acc = float(AL_rights) / float(AL_predts)
    rec = float(AL_rights) / float(AL_labels)
    f1 = 2 * acc * rec / (acc + rec)
    print(str(AL_labels) + '\t' + str(AL_predts) + '\t' + str(AL_rights))
    print('ALL: ' + str(acc) + '\t' + str(rec) + '\t' + str(f1))

    for key,value in cnt_dict.items():
        #print(str(key)+'\t'+str(value))
        if value[1]==0 or value[0]==0:
            acc = 0.0
            rec = 0.0
            f1  = 0.0
        else:
            print(key)
            print(value)
            acc = float(value[2]) / float(value[1])
            rec = float(value[2]) / float(value[0])
            if acc+rec==0.0:
                f1=0.0
            else:
                f1 = 2 * acc * rec / (acc + rec)
        print(key + ':\t' + str(acc)+'\t'+str(rec)+'\t'+str(f1))

    print('\n------------\n')
    print('total numbers:', len(label_data))
    print('error_cnt:', error_cnt)

    print('....')

# Only I and R type
def correction_level():
    typescount = open('experiments/CGEDToR/类型统计.txt', 'r', encoding='utf-8').readlines()
    R_list = dict()
    I_list = dict()
    R_list['R0000'] = 0
    I_list['I0000'] = 0
    for tc in typescount:
        if '	I(' in tc:
            tcc = tc.strip().split('	')
            if int(tcc[2]) < 10:
                I_list['I0000'] += int(tcc[2])
            else:
                I_list[tcc[0]] = int(tcc[2])
        if '	R(' in tc:
            tcc = tc.strip().split('	')
            if int(tcc[2]) < 10:
                R_list['R0000'] += int(tcc[2])
            else:
                R_list[tcc[0]] = int(tcc[2])

    I_count = 0.0
    I0000_count = 0.0
    I_precount = 0.0
    I_reccount = 0.0
    R_count = 0.0
    R0000_count = 0.0
    R_precount = 0.0
    R_reccount = 0.0
    results = open('experiments/CGEDToR/实验数据-r10i10/final_correction.txt','r',encoding='utf-8').readlines()
    #results = open('experiments/CGEDToR/实验数据-r10i10/evalresults.log', 'r', encoding='utf-8').readlines()
    for pr in results:
        pr = pr.strip()
        if pr.startswith('I'):
            prr = pr.split('	')
            I_count += I_list[prr[0].replace(':', '')]
            if (float(prr[1])==0.0 and float(prr[2])==0.0 and float(prr[3])==0.0) or prr[0]=='I0000:':
                continue
            else:
                I_precount += float(prr[1])*I_list[prr[0].replace(':','')]
                I_reccount += float(prr[2])*I_list[prr[0].replace(':','')]
            """
            elif prr[0]=='I0000:':
                I0000_count += I_list[prr[0].replace(':', '')]
                continue
                #I_precount += float(prr[1]) * I_list[prr[0].replace(':', '')]*0.7232
                #I_reccount += float(prr[2]) * I_list[prr[0].replace(':', '')]*0.7232
                #I_f1count += float(prr[3]) * I_list[prr[0].replace(':', '')]*0.7232 
                """
        if pr.startswith('R'):
            prr = pr.split('	')
            R_count += R_list[prr[0].replace(':', '')]
            if (float(prr[1])==0.0 and float(prr[2])==0.0 and float(prr[3])==0.0) or prr[0]=='R0000:':
                print(pr)
                continue
            else:
                R_precount += float(prr[1])*R_list[prr[0].replace(':','')]
                R_reccount += float(prr[2])*R_list[prr[0].replace(':','')]
            """
            elif prr[0]=='R0000:':
                R0000_count += R_list[prr[0].replace(':', '')]
                continue
                
                #R_precount += float(prr[1])*R_list[prr[0].replace(':','')]*0.7232
                #R_reccount += float(prr[2])*R_list[prr[0].replace(':','')]*0.7232
                #R_f1count  += float(prr[3])*R_list[prr[0].replace(':','')]*0.7232"""

    """
    print(I_count)
    print(I0000_count)
    print(R_count)
    print(R0000_count)
    """

    IR_pre = (I_precount+R_precount)/(I_count+R_count)
    IR_rec = (I_reccount+R_reccount)/(I_count+R_count)
    print(str(IR_pre))
    print(str(IR_rec))
    print(str(2 * IR_pre * IR_rec / (IR_pre+IR_rec)))

    """
    print(str(I_precount / I_count))
    print(str(I_reccount / I_count))
    print(str(2*(I_precount / I_count)*(I_reccount / I_count) / ((I_reccount / I_count)+(I_precount / I_count))))

    print(str(R_precount / R_count))
    print(str(R_reccount / R_count))
    print(str(2 * (R_precount / R_count) * (R_reccount / R_count) / ((R_reccount / R_count) + (R_precount / R_count))))
    """

def longtail():
    typescount = open('experiments/CGEDToR/类型统计.txt', 'r', encoding='utf-8').readlines()
    R_list = dict()
    I_list = dict()
    R_list['R0000'] = 0
    I_list['I0000'] = 0
    for tc in typescount:
        if '	I(' in tc:
            tcc = tc.strip().split('	')
            I_list[tcc[0]] = int(tcc[2])
        if '	R(' in tc:
            tcc = tc.strip().split('	')
            R_list[tcc[0]] = int(tcc[2])

    I500count = [0.0, 0.0, 0.0]  #precount,reccount,totalnum
    I300count = [0.0, 0.0, 0.0]
    I100count = [0.0, 0.0, 0.0]
    I070count = [0.0, 0.0, 0.0]
    I050count = [0.0, 0.0, 0.0]
    I030count = [0.0, 0.0, 0.0]
    I020count = [0.0, 0.0, 0.0]
    I010count = [0.0, 0.0, 0.0]
    I000count = [0.0, 0.0, 0.0]

    R500count = [0.0, 0.0, 0.0]  #precount,reccount,totalnum
    R300count = [0.0, 0.0, 0.0]
    R100count = [0.0, 0.0, 0.0]
    R070count = [0.0, 0.0, 0.0]
    R050count = [0.0, 0.0, 0.0]
    R030count = [0.0, 0.0, 0.0]
    R020count = [0.0, 0.0, 0.0]
    R010count = [0.0, 0.0, 0.0]
    R000count = [0.0, 0.0, 0.0]

    results = open('experiments/CGEDToR/实验数据-r10i10/test_prediction_CGEDToR.txt', 'r', encoding='utf-8').readlines()
    #results = open('experiments/CGEDToR/实验数据-r10i10/position_details_CGEDToR.txt', 'r', encoding='utf-8').readlines()
    # results = open('experiments/CGEDToR/实验数据-r10i10/evalresults.log', 'r', encoding='utf-8').readlines()
    for pr in results:
        pr = pr.strip()
        if pr.startswith('I'):
            prr = pr.split('	')
            Itype = prr[0].replace(':', '')
            if Itype == 'I0000':
                I000count[0] = float(prr[1])
                I000count[1] = float(prr[2])
                I000count[2] = float(prr[3])
            elif I_list[Itype] >=500:
                I500count[0] += I_list[Itype] * float(prr[1])
                I500count[1] += I_list[Itype] * float(prr[2])
                I500count[2] += I_list[Itype]
            elif I_list[Itype] >=300:
                I300count[0] += I_list[Itype] * float(prr[1])
                I300count[1] += I_list[Itype] * float(prr[2])
                I300count[2] += I_list[Itype]
            elif I_list[Itype] >=100:
                I100count[0] += I_list[Itype] * float(prr[1])
                I100count[1] += I_list[Itype] * float(prr[2])
                I100count[2] += I_list[Itype]
            elif I_list[Itype] >=70:
                I070count[0] += I_list[Itype] * float(prr[1])
                I070count[1] += I_list[Itype] * float(prr[2])
                I070count[2] += I_list[Itype]
            elif I_list[Itype] >=50:
                I050count[0] += I_list[Itype] * float(prr[1])
                I050count[1] += I_list[Itype] * float(prr[2])
                I050count[2] += I_list[Itype]
            elif I_list[Itype] >=30:
                I030count[0] += I_list[Itype] * float(prr[1])
                I030count[1] += I_list[Itype] * float(prr[2])
                I030count[2] += I_list[Itype]
            elif I_list[Itype] >=20:
                I020count[0] += I_list[Itype] * float(prr[1])
                I020count[1] += I_list[Itype] * float(prr[2])
                I020count[2] += I_list[Itype]
            elif I_list[Itype] >=10:
                I010count[0] += I_list[Itype] * float(prr[1])
                I010count[1] += I_list[Itype] * float(prr[2])
                I010count[2] += I_list[Itype]

        if pr.startswith('R'):
            prr = pr.split('	')
            Rtype = prr[0].replace(':', '')
            if Rtype == 'R0000':
                R000count[0] = float(prr[1])
                R000count[1] = float(prr[2])
                R000count[2] = float(prr[3])
            elif R_list[Rtype] >=500:
                R500count[0] += R_list[Rtype] * float(prr[1])
                R500count[1] += R_list[Rtype] * float(prr[2])
                R500count[2] += R_list[Rtype]
            elif R_list[Rtype] >=300:
                R300count[0] += R_list[Rtype] * float(prr[1])
                R300count[1] += R_list[Rtype] * float(prr[2])
                R300count[2] += R_list[Rtype]
            elif R_list[Rtype] >=100:
                R100count[0] += R_list[Rtype] * float(prr[1])
                R100count[1] += R_list[Rtype] * float(prr[2])
                R100count[2] += R_list[Rtype]
            elif R_list[Rtype] >=70:
                R070count[0] += R_list[Rtype] * float(prr[1])
                R070count[1] += R_list[Rtype] * float(prr[2])
                R070count[2] += R_list[Rtype]
            elif R_list[Rtype] >=50:
                R050count[0] += R_list[Rtype] * float(prr[1])
                R050count[1] += R_list[Rtype] * float(prr[2])
                R050count[2] += R_list[Rtype]
            elif R_list[Rtype] >=30:
                R030count[0] += R_list[Rtype] * float(prr[1])
                R030count[1] += R_list[Rtype] * float(prr[2])
                R030count[2] += R_list[Rtype]
            elif R_list[Rtype] >=20:
                R020count[0] += R_list[Rtype] * float(prr[1])
                R020count[1] += R_list[Rtype] * float(prr[2])
                R020count[2] += R_list[Rtype]
            elif R_list[Rtype] >=10:
                R010count[0] += R_list[Rtype] * float(prr[1])
                R010count[1] += R_list[Rtype] * float(prr[2])
                R010count[2] += R_list[Rtype]

    """
    print(I_count)
    print(I0000_count)
    print(R_count)
    print(R0000_count)
    """
    print('I500:', end = "")
    #print(str(I500count[0] / I500count[2]))
    print(str(I500count[1])+' '+str(I500count[2]))
    print(str(I500count[1] / I500count[2]))
    #print(str(2 * I500count[0] * I500count[1] / (I500count[2] * (I500count[0] + I500count[1]))))
    print('I300:', end = "")
    #print(str(I300count[0] / I300count[2]))
    print(str(I300count[1] / I300count[2]))
    #print(str(2 * I300count[0] * I300count[1] / (I300count[2] * (I300count[0] + I300count[1]))))
    print('I100:', end = "")
    #print(str(I100count[0] / I100count[2]))
    print(str(I100count[1] / I100count[2]))
    #print(str(2 * I100count[0] * I100count[1] / (I100count[2] * (I100count[0] + I100count[1]))))
    print('I070:', end = "")
    #print(str(I070count[0] / I070count[2]))
    print(str(I070count[1] / I070count[2]))
    #print(str(2 * I070count[0] * I070count[1] / (I070count[2] * (I070count[0] + I070count[1]))))
    print('I050:', end = "")
    #print(str(I050count[0] / I050count[2]))
    print(str(I050count[1] / I050count[2]))
    #print(str(2 * I050count[0] * I050count[1] / (I050count[2] * (I050count[0] + I050count[1]))))
    print('I030:', end = "")
    #print(str(I030count[0] / I030count[2]))
    print(str(I030count[1] / I030count[2]))
    #print(str(2 * I030count[0] * I030count[1] / (I030count[2] * (I030count[0] + I030count[1]))))
    print('I020:', end = "")
    #print(str(I020count[0] / I020count[2]))
    print(str(I020count[1] / I020count[2]))
    #print(str(2 * I020count[0] * I020count[1] / (I020count[2] * (I020count[0] + I020count[1]))))
    print('I010:', end = "")
    #print(str(I010count[0] / I010count[2]))
    print(str(I010count[1] / I010count[2]))
    #print(str(2 * I010count[0] * I010count[1] / (I010count[2] * (I010count[0] + I010count[1]))))
    print('I000:', end = "")
    #print(I000count[0])
    print(I000count[1])
    #print(I000count[2])


    print('R500:', end = "")
    #print(str(R500count[0] / R500count[2]))
    print(str(R500count[1] / R500count[2]))
    #print(str(2 * R500count[0] * R500count[1] / (R500count[2] * (R500count[0] + R500count[1]))))
    print('R300:', end = "")
    #print(str(R300count[0] / R300count[2]))
    print(str(R300count[1] / R300count[2]))
    #print(str(2 * R300count[0] * R300count[1] / (R300count[2] * (R300count[0] + R300count[1]))))
    print('R100:', end = "")
    #print(str(R100count[0] / R100count[2]))
    print(str(R100count[1] / R100count[2]))
    #print(str(2 * R100count[0] * R100count[1] / (R100count[2] * (R100count[0] + R100count[1]))))
    print('R070:', end = "")
    #print(str(R070count[0] / R070count[2]))
    print(str(R070count[1] / R070count[2]))
    #print(str(2 * R070count[0] * R070count[1] / (R070count[2] * (R070count[0] + R070count[1]))))
    print('R050:', end = "")
    #print(str(R050count[0] / R050count[2]))
    print(str(R050count[1] / R050count[2]))
    #print(str(2 * R050count[0] * R050count[1] / (R050count[2] * (R050count[0] + R050count[1]))))
    print('R030:', end = "")
    #print(str(R030count[0] / R030count[2]))
    print(str(R030count[1] / R030count[2]))
    #print(str(2 * R030count[0] * R030count[1] / (R030count[2] * (R030count[0] + R030count[1]))))
    print('R020:', end = "")
    #print(str(R020count[0] / R020count[2]))
    print(str(R020count[1] / R020count[2]))
    #print(str(2 * R020count[0] * R020count[1] / (R020count[2] * (R020count[0] + R020count[1]))))
    print('R010:', end = "")
    #print(str(R010count[0] / R010count[2]))
    print(str(R010count[1] / R010count[2]))
    #print(str(2 * R010count[0] * R010count[1] / (R010count[2] * (R010count[0] + R010count[1]))))
    print('R000:', end = "")
    #print(R000count[0])
    print(R000count[1])
    #print(R000count[2])

def longtail_TECF():
    typescount = open('experiments/CGEDToR/类型统计.txt', 'r', encoding='utf-8').readlines()
    R_list = dict()
    I_list = dict()
    for tc in typescount:
        if '	I(' in tc:
            tcc = tc.strip().split('	')
            I_list[tcc[1]] = int(tcc[2])
        if '	R(' in tc:
            tcc = tc.strip().split('	')
            R_list[tcc[1]] = int(tcc[2])

    detres = open('experiments/longtail/mask预测/GEDet结果.txt', 'r', encoding='utf-8').readlines()
    dettaglist = list()
    for index1 in range(len(detres)):
        if '========' not in detres[index1]:
            labsen = detres[index1].strip()
            labsen1 = labsen.split(' ')
            for index2 in range(len(labsen1)):
                if labsen1[index2].startswith('[__'):
                    dettaglist.append(labsen1[index2])
                elif index2 == 0 or (not labsen1[index2 - 1].startswith('[__') and not labsen1[index2].startswith('[__')):
                    dettaglist.append('O')
            dettaglist.append('O')


    I500count = [0.0, 0.0, 0.0, 0.0]  #Top1,Top3,Top5,Total
    I300count = [0.0, 0.0, 0.0, 0.0]
    I100count = [0.0, 0.0, 0.0, 0.0]
    I070count = [0.0, 0.0, 0.0, 0.0]
    I050count = [0.0, 0.0, 0.0, 0.0]
    I030count = [0.0, 0.0, 0.0, 0.0]
    I020count = [0.0, 0.0, 0.0, 0.0]
    I010count = [0.0, 0.0, 0.0, 0.0]
    I000count = [0.0, 0.0, 0.0, 0.0]

    R500count = [0.0, 0.0, 0.0, 0.0]  #Top1,Top3,Top5,Total
    R300count = [0.0, 0.0, 0.0, 0.0]
    R100count = [0.0, 0.0, 0.0, 0.0]
    R070count = [0.0, 0.0, 0.0, 0.0]
    R050count = [0.0, 0.0, 0.0, 0.0]
    R030count = [0.0, 0.0, 0.0, 0.0]
    R020count = [0.0, 0.0, 0.0, 0.0]
    R010count = [0.0, 0.0, 0.0, 0.0]
    R000count = [0.0, 0.0, 0.0, 0.0]

    groundt = open('experiments/longtail/mask预测/nolimit-test.txt', 'r', encoding='utf-8').readlines()
    results = open('experiments/longtail/mask预测/GECor结果_1.txt', 'r', encoding='utf-8').readlines()

    for index in range(len(results)):
        if not '	' in results[index] or not '	' in groundt[index]:
            continue

        labeldata = groundt[index].strip().split('	')
        resltdata = results[index].strip().split('	')

        if labeldata[1].startswith('I') and dettaglist[index]=='[__I__]':
            Itype = labeldata[1]
            tags = resltdata[1].strip().split(' ')

            Top1 = tags[0]
            if len(tags)>=3:
                Top3 = tags[0]+tags[1]+tags[2]
            else:
                Top3 = ''
            if len(tags)>=5:
                Top5 = tags[0]+tags[1]+tags[2]+tags[3]+tags[4]
            else:
                Top5 = ''

            if I_list[Itype] >=500:
                if Itype in Top1:
                    I500count[0] += 1
                if Itype in Top3:
                    I500count[1] += 1
                if Itype in Top5:
                    I500count[2] += 1
                I500count[3] += 1
            elif I_list[Itype] >=300:
                if Itype in Top1:
                    I300count[0] += 1
                if Itype in Top3:
                    I300count[1] += 1
                if Itype in Top5:
                    I300count[2] += 1
                I300count[3] += 1
            elif I_list[Itype] >=100:
                if Itype in Top1:
                    I100count[0] += 1
                if Itype in Top3:
                    I100count[1] += 1
                if Itype in Top5:
                    I100count[2] += 1
                I100count[3] += 1
            elif I_list[Itype] >=70:
                if Itype in Top1:
                    I070count[0] += 1
                if Itype in Top3:
                    I070count[1] += 1
                if Itype in Top5:
                    I070count[2] += 1
                I070count[3] += 1
            elif I_list[Itype] >=50:
                if Itype in Top1:
                    I050count[0] += 1
                if Itype in Top3:
                    I050count[1] += 1
                if Itype in Top5:
                    I050count[2] += 1
                I050count[3] += 1
            elif I_list[Itype] >=30:
                if Itype in Top1:
                    I030count[0] += 1
                if Itype in Top3:
                    I030count[1] += 1
                if Itype in Top5:
                    I030count[2] += 1
                I030count[3] += 1
            elif I_list[Itype] >=20:
                if Itype in Top1:
                    I020count[0] += 1
                if Itype in Top3:
                    I020count[1] += 1
                if Itype in Top5:
                    I020count[2] += 1
                I020count[3] += 1
            elif I_list[Itype] >=10:
                if Itype in Top1:
                    I010count[0] += 1
                if Itype in Top3:
                    I010count[1] += 1
                if Itype in Top5:
                    I010count[2] += 1
                I010count[3] += 1
            else:
                if Itype in Top1:
                    I000count[0] += 1
                if Itype in Top3:
                    I000count[1] += 1
                if Itype in Top5:
                    I000count[2] += 1
                I000count[3] += 1

        if labeldata[1].startswith('R'):
            Itype = labeldata[1]
            tags = resltdata[1].strip().split(' ')

            Top1 = tags[0]
            if len(tags)>=3:
                Top3 = tags[0]+tags[1]+tags[2]
            else:
                Top3 = ''
            if len(tags)>=5:
                Top5 = tags[0]+tags[1]+tags[2]+tags[3]+tags[4]
            else:
                Top5 = ''

            if R_list[Itype] >=500:
                if Itype in Top1:
                    R500count[0] += 1
                if Itype in Top3:
                    R500count[1] += 1
                if Itype in Top5:
                    R500count[2] += 1
                R500count[3] += 1
            elif R_list[Itype] >=300:
                if Itype in Top1:
                    R300count[0] += 1
                if Itype in Top3:
                    R300count[1] += 1
                if Itype in Top5:
                    R300count[2] += 1
                R300count[3] += 1
            elif R_list[Itype] >=100:
                if Itype in Top1:
                    R100count[0] += 1
                if Itype in Top3:
                    R100count[1] += 1
                if Itype in Top5:
                    R100count[2] += 1
                R100count[3] += 1
            elif R_list[Itype] >=70:
                if Itype in Top1:
                    R070count[0] += 1
                if Itype in Top3:
                    R070count[1] += 1
                if Itype in Top5:
                    R070count[2] += 1
                R070count[3] += 1
            elif R_list[Itype] >=50:
                if Itype in Top1:
                    R050count[0] += 1
                if Itype in Top3:
                    R050count[1] += 1
                if Itype in Top5:
                    R050count[2] += 1
                R050count[3] += 1
            elif R_list[Itype] >=30:
                if Itype in Top1:
                    R030count[0] += 1
                if Itype in Top3:
                    R030count[1] += 1
                if Itype in Top5:
                    R030count[2] += 1
                R030count[3] += 1
            elif R_list[Itype] >=20:
                if Itype in Top1:
                    R020count[0] += 1
                if Itype in Top3:
                    R020count[1] += 1
                if Itype in Top5:
                    R020count[2] += 1
                R020count[3] += 1
            elif R_list[Itype] >=10:
                if Itype in Top1:
                    R010count[0] += 1
                if Itype in Top3:
                    R010count[1] += 1
                if Itype in Top5:
                    R010count[2] += 1
                R010count[3] += 1
            else:
                if Itype in Top1:
                    R000count[0] += 1
                if Itype in Top3:
                    R000count[1] += 1
                if Itype in Top5:
                    R000count[2] += 1
                R000count[3] += 1

    """
    print(I_count)
    print(I0000_count)
    print(R_count)
    print(R0000_count)
    """

    print('I500:', end = "")
    print(str(I500count[0] / I500count[3]))
    print(str(I500count[1] / I500count[3]))
    print(str(I500count[2] / I500count[3]))

    print('I300:', end = "")
    print(str(I300count[0] / I300count[3]))
    print(str(I300count[1] / I300count[3]))
    print(str(I300count[2] / I300count[3]))

    print('I100:', end = "")
    print(str(I100count[0] / I100count[3]))
    print(str(I100count[1] / I100count[3]))
    print(str(I100count[2] / I100count[3]))

    print('I070:', end = "")
    print(str(I070count[0] / I070count[3]))
    print(str(I070count[1] / I070count[3]))
    print(str(I070count[2] / I070count[3]))

    print('I050:', end = "")
    print(str(I050count[0] / I050count[3]))
    print(str(I050count[1] / I050count[3]))
    print(str(I050count[2] / I050count[3]))

    print('I030:', end = "")
    print(str(I030count[0] / I030count[3]))
    print(str(I030count[1] / I030count[3]))
    print(str(I030count[2] / I030count[3]))

    print('I020:', end = "")
    print(str(I020count[0] / I020count[3]))
    print(str(I020count[1] / I020count[3]))
    print(str(I020count[2] / I020count[3]))

    print('I010:', end = "")
    print(str(I010count[0] / I010count[3]))
    print(str(I010count[1] / I010count[3]))
    print(str(I010count[2] / I010count[3]))

    print('I000:', end = "")
    print(str(I000count[0] / I000count[3]))
    print(str(I000count[1] / I000count[3]))
    print(str(I000count[2] / I000count[3]))

    print('R500:', end = "")
    print(str(R500count[0] / R500count[3]))
    print(str(R500count[1] / R500count[3]))
    print(str(R500count[2] / R500count[3]))

    print('R300:', end = "")
    print(str(R300count[0] / R300count[3]))
    print(str(R300count[1] / R300count[3]))
    print(str(R300count[2] / R300count[3]))

    print('R100:', end = "")
    print(str(R100count[0] / R100count[3]))
    print(str(R100count[1] / R100count[3]))
    print(str(R100count[2] / R100count[3]))

    print('R070:', end = "")
    print(str(R070count[0] / R070count[3]))
    print(str(R070count[1] / R070count[3]))
    print(str(R070count[2] / R070count[3]))

    print('R050:', end = "")
    print(str(R050count[0] / R050count[3]))
    print(str(R050count[1] / R050count[3]))
    print(str(R050count[2] / R050count[3]))

    print('R030:', end = "")
    print(str(R030count[0] / R030count[3]))
    print(str(R030count[1] / R030count[3]))
    print(str(R030count[2] / R030count[3]))

    print('R020:', end = "")
    print(str(R020count[0] / R020count[3]))
    print(str(R020count[1] / R020count[3]))
    print(str(R020count[2] / R020count[3]))

    print('R010:', end = "")
    print(str(R010count[0] / R010count[3]))
    print(str(R010count[1] / R010count[3]))
    print(str(R010count[2] / R010count[3]))

    print('R000:', end = "")
    print(str(R000count[0] / R000count[3]))
    print(str(R000count[1] / R000count[3]))
    print(str(R000count[2] / R000count[3]))

if __name__ == '__main__':
    #typestatis()
    #genLabelData()
    #traindevtest()
    #test_evaluate_TECF()
    #detection_level()
    #identification_level()
    #position_level()
    #correction_level()
    #longtail()
    longtail_TECF()


    """
    filestrs1 = open('experiments/CGEDToR/labels-nolimit.txt','r',encoding='utf-8').readlines()
    filestrs2 = open('experiments/CGEDToR/limit1010-test.txt','r',encoding='utf-8').readlines()
    #outfile = open('experiments/CGEDToR/nolimit-test.txt','w',encoding='utf-8')


    filestrs3 = open('experiments/CGEDToR/nolimit-test.txt', 'r', encoding='utf-8').readlines()

    for index in range(len(filestrs3)):
        ss1 = filestrs2[index]
        ss2 = filestrs3[index]
        if ss1==ss2:
            continue
        sss1 = ss1.split('	')
        sss2 = ss2.split('	')
        if not sss1[0]==sss2[0]:
            print(index)
            break
    
    wlist = ''

    for sss in filestrs2:
        sss = sss.strip()
        if len(sss)==0:
            if len(wlist) > 0:
                for index in range(0, len(filestrs1), 4):
                    if filestrs1[index].strip()==wlist:
                        labsen = filestrs1[index+2].strip()
                        labsen1 = labsen.split(' ')
                        wrdlist = list()
                        taglist = list()
                        for index1 in range(len(labsen1)):
                            if labsen1[index1].startswith('[__'):
                                taglist.append(labsen1[index1])
                                wrdlist.append(labsen1[index1+1])
                            elif index1==0 or (not labsen1[index1-1].startswith('[__') and not labsen1[index1].startswith('[__')):
                                wrdlist.append(labsen1[index1])
                                taglist.append('O')
                        if not len(list(wlist))==len(wrdlist):
                            print(wlist)
                            print(str(wrdlist))
                            break
                        for index2 in range(len(wrdlist)):
                            outfile.write(wrdlist[index2]+'\t'+taglist[index2].replace('[__','').replace('__]','')+'\n')
                        outfile.write('\n')
                        break
            wlist = ''
        else:
            wlist = wlist+sss.split('	')[0]"""