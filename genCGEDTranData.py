import leven2edit as l2e
import commonTools
import random
import opencc
cc = opencc.OpenCC('t2s')

def splittraintest():
    allstrs = open('data_processed/labels_1211_trainpairs_all_ANUM_clean.txt', 'r', encoding='utf-8').readlines()
    trainfile = open('data_processed/labels_1211_trainpairs_all_ANUM_clean_train.txt', 'w', encoding='utf-8')
    devfile = open('data_processed/labels_1211_trainpairs_all_ANUM_clean_dev.txt', 'w', encoding='utf-8')
    testfile = open('data_processed/labels_1211_trainpairs_all_ANUM_clean_test.txt', 'w', encoding='utf-8')

    trainlist = list()
    devlist = list()
    testlist = list()

    for index in range(0, len(allstrs)):
        if allstrs[index].strip()=='===========':
            if len(allstrs[index - 3]) > 300 or len(allstrs[index - 3]) < 5:
                continue
            num = random.randint(1, 20)
            if num <= 3:
                devlist.append(allstrs[index - 1].strip())
            elif num<=6:
                testlist.append(allstrs[index - 1].strip())
            else:
                trainlist.append(allstrs[index - 1].strip())

    index1 = [x for x in range(len(trainlist))]
    index2 = [x for x in range(len(devlist))]
    index3 = [x for x in range(len(testlist))]

    random.shuffle(index1)
    random.shuffle(index2)
    random.shuffle(index3)

    for index in index1:
        trainfile.write(trainlist[index] + '\n')
    for index in index2:
        devfile.write(devlist[index] + '\n')
    for index in index3:
        testfile.write(testlist[index] + '\n')

def isLabel(str):
    if str.startswith('[__') and str.endswith('__]'):
        return True
    else:
        return False

def formattrainfile():
    files = ['train', 'dev', 'test']

    for filename in files:
        inpstrs = open('data_processed/labels_1211_trainpairs_all_ANUM_clean_'+filename+'.txt',
                       'r', encoding='utf-8').readlines()
        outfile = open('data_processed/fmt_labels_1211_trainpairs_all_ANUM_clean_'+filename+'.txt',
                       'w', encoding='utf-8')

        for str1 in inpstrs:
            str1 = str1.strip()
            str2 = str1.split(' ')
            #charseq = ''
            #tagsseq = ''
            for index in range(0, len(str2)):
                if isLabel(str2[index]):
                    cgedtag = str2[index][3:-3]     #[__I(教育)__] --> I(教育)
                    if '(' in cgedtag:
                        cgedtag = cgedtag[:1]
                    outfile.write(str2[index+1] + '\t' + cgedtag + '\n')
                elif not isLabel(str2[index-1]):
                    outfile.write(str2[index] + '\tO\n')

                """
                if isLabel(str2[index]):
                    charseq = charseq + str2[index+1] + '\t'
                    tagsseq = tagsseq + str2[index][3:-3] + '\t'
                elif not isLabel(str2[index - 1]):
                    charseq = charseq + str2[index] + '\t'
                    tagsseq = tagsseq + 'O\t'"""

            #oufile.write(charseq + '\n')
            #oufile.write(tagsseq + '\n')
            outfile.write('\n')

def tokenizer_clean():
    from transformers import BertTokenizer
    bert_base_path = '/PythonScripts/001_common_resources/LERT'
    tokenizer = BertTokenizer.from_pretrained(bert_base_path)

    filestrs = open('data_processed/labels_1211_trainpairs_all_ANUM.txt', 'r', encoding='utf-8').readlines()
    newfile = open('data_processed/labels_1211_trainpairs_all_ANUM_clean.txt', 'w', encoding='utf-8')

    for index in range(len(filestrs)):
        if filestrs[index].strip()=='===========':
            text = filestrs[index - 3].strip()
            text = text.replace('ANUM', '_').replace('AEMAIL', '_').replace('ATIME', '_').replace('ANAME', '_').replace(
                'ALINK', '_')

            tokens = tokenizer.tokenize(text)
            if len(tokens) == len(text):
                newfile.write(filestrs[index - 3])
                newfile.write(filestrs[index - 2])
                newfile.write(filestrs[index - 1])
                newfile.write('===========\n')
            else:
                print(index)

def text_clean():
    filestrs = open('data_processed/1211_trainpairs_all.txt', 'r', encoding='utf-8').readlines()
    newfile = open('data_processed/1211_trainpairs_all_ANUM.txt', 'w', encoding='utf-8')

    for sstr in filestrs:
        if not sstr.startswith('==========='):
            sss = sstr.strip().replace('', '').replace('', '').replace('�','').replace('','')
            sss = sss.replace(' ','').replace('	','')
            ### change num,name,link,time,email to ANUM,ANAME,ALINK,ANAME,AEMAIL
            sss = commonTools.strQ2B(sss)
            sss = commonTools.rmSingleByte(sss)
            newfile.write(sss+'\n')
        else:
            newfile.write(sstr)

def gen_labels():
    inpstrs = open('data_processed/1211_trainpairs_all_ANUM.txt', 'r', encoding='utf-8').readlines()
    outfile = open('data_processed/labels_1211_trainpairs_all_ANUM.txt', 'w', encoding='utf-8')

    for index in range(0, len(inpstrs)):
        if inpstrs[index].startswith('==========='):
            input = inpstrs[index - 2].strip()
            output = inpstrs[index - 1].strip()

            sen_wrong = ' ' + input
            sen_right = ' ' + output

            if sen_wrong == sen_right:
                outfile.write(sen_wrong.strip() + '\n')
                outfile.write(sen_right.strip() + '\n')

                ops = l2e.editops(sen_wrong, sen_right)
                labels2 = l2e.genLabels(sen_wrong, sen_right, ops, 2)

                outfile.write(l2e.T_to_W(l2e.add_space(labels2.strip())) + '\n')
                outfile.write('===========\n')
                continue

            while not sen_wrong == sen_right:
                outfile.write(sen_wrong.strip()+'\n')

                ops = l2e.editops(sen_wrong, sen_right)
                labels2 = l2e.genLabels(sen_wrong, sen_right, ops, 2)
                sen_wrong = l2e.genNewSen(sen_wrong, sen_right, ops)

                outfile.write(sen_wrong.strip()+'\n')
                outfile.write(l2e.T_to_W(l2e.add_space(labels2.strip())) + '\n')
                outfile.write('===========\n')

if __name__ == '__main__':
    #text_clean()
    #gen_labels()
    #tokenizer_clean()
    #splittraintest()
    formattrainfile()

