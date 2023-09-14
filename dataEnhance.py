"""
This file contains the steps of generating synthetic data
"""

import random
import commonTools

"""
基于good data，产生语法错误样本
"""
## *******************************
## R类型
## *******************************
time_p = ['从','自','自从','于','打','到','往','在','当','朝','向','顺着','沿着','随着']
ways_p = ['按','照','按照','依','依照','本着','经过','通过','根据','以','凭']
purs_p = ['为','为了','为着']
reaz_p = ['因','因为','由于']
obet_p = ['对','对于','把','向','跟','与','同','给','关于']
excd_p = ['除','除了','除去','除非']
pasv_p = ['被','叫','让','给']
comp_p = ['比','和','同']
perp_list = [time_p, ways_p, purs_p, reaz_p, obet_p, excd_p, pasv_p, comp_p]
p_dict = {}
for perp in perp_list:
    for p in perp:
        p_dict[p] = 0
#子女不知道父母_给_孩子的心，不知道父母过日子过得如何。
#子女不知道父母_对_孩子的心，不知道父母过日子过得如何。
def Make_R_perp(sence):
    newsen = ''
    posrest = commonTools.postagging(sence)
    wordlist = list()
    ptaglist = list()
    for word, ptag in posrest:
        wordlist.append(word)
        ptaglist.append(ptag)

    indexlist = [i for i in range(len(wordlist))]
    random.shuffle(indexlist)

    for index in indexlist:
        ptag = ptaglist[index]
        word = wordlist[index]
        if ptag=='p':
            pwlist = list()
            for perp in perp_list:
                if word in perp and p_dict[word]<=2000:
                    pwlist.extend(perp)
                    pwlist.remove(word)

            if len(pwlist)>0:
                index1 = random.randint(0, len(pwlist) - 1)
                wordlist[index] = pwlist[index1]
                p_dict[word] = p_dict[word]+1
                break

    for word in wordlist:
        newsen = newsen+word

    return newsen

synostrs = open('dataEnhance/dict_synonym/dict_synonym.txt', 'r', encoding='utf-8').readlines()
#读书写字，是我们学习各种文化都必须掌握的基本_条件_。
#读书写字，是我们学习各种文化都必须掌握的基本_本领_。
def Make_R_syno(sence):
    newsen = ''
    posrest = commonTools.postagging(sence)
    wordlist = list()
    ptaglist = list()
    for word, ptag in posrest:
        wordlist.append(word)
        ptaglist.append(ptag)

    indexlist = [i for i in range(len(wordlist))]
    random.shuffle(indexlist)

    for index in indexlist:
        synlist = list()
        for sstr in synostrs:
            if '= ' in sstr or '# ' in sstr:
                strlist = sstr.strip().split(' ')
                if wordlist[index] in strlist:
                    synlist.extend(strlist[1:])
                    synlist.remove(wordlist[index])

        if len(synlist) > 0:
            index1 = random.randint(0, len(synlist) - 1)
            wordlist[index] = synlist[index1]
            break

    for word in wordlist:
        newsen = newsen+word

    return newsen

## *******************************
## I类型
## *******************************
I_dict = {}
for index in range(1, 28):
    I_dict[index] = 0
def I_ALLTypes(sence, type=1):
    newsen = ''
    posrest = commonTools.postagging(sence)
    wordlist = list()
    ptaglist = list()
    for word, ptag in posrest:
        wordlist.append(word)
        ptaglist.append(ptag)

    indexlist = [i for i in range(len(wordlist))]
    random.shuffle(indexlist)

    # I_nounverb: 他们总是围绕着这个话题_讨论_。
    if type == 1:
        for index in indexlist:
            if index>=1 and (ptaglist[index]=='v' or ptaglist[index]=='vn') and (ptaglist[index-1] == 'n' or\
                ptaglist[index-1] == 'vn' or ptaglist[index-1] == 'nz' or ptaglist[index-1] == 'nr' or\
                ptaglist[index-1] == 'nt' or ptaglist[index-1] == 'an' or ptaglist[index-1] == 'ns') and\
                commonTools.num_hanzi(wordlist[index])>=1:
                wordlist[index] = ''
                I_dict[type] = I_dict[type]+1
                break

    # I_verb_le: 因为这个原因让他认识_了_这位女生。
    if type == 2:
        for index in indexlist:
            if index>=1 and wordlist[index] == '了' and ptaglist[index-1]=='v':
                wordlist[index] = ''
                I_dict[type] = I_dict[type] + 1
                break

    # I_verb_r: 而常常陪着我一起去玩儿，甚至没有因我错了而打过_我_。
    if type == 3:
        for index in indexlist:
            if index>=1 and ptaglist[index] == 'r' and (ptaglist[index-1]=='v' or ptaglist[index-1]=='u') and \
                commonTools.num_hanzi(wordlist[index])>=1:
                wordlist[index] = ''
                I_dict[type] = I_dict[type] + 1
                break

    # I_de_noun: 世界上既有绿色食品又没有饥饿_的现象_，如果有这样的世界多好！
    if type == 4:
        for index in indexlist:
            if index>=1 and index<(len(wordlist) - 1) and ptaglist[index] == 'n' and wordlist[index - 1] == '的' and \
                ptaglist[index + 1] == 'w' and commonTools.num_hanzi(wordlist[index])>=1:
                wordlist[index] = ''
                wordlist[index - 1] = ''
                I_dict[type] = I_dict[type] + 1
                break

    # I_verb_1: 我有帮_忙_安排那个节目。
    if type==5:
        for index in indexlist:
            if ptaglist[index] == 'v' and commonTools.num_hanzi(wordlist[index]) > 1:
                wordlist[index] = wordlist[index][:-1]
                I_dict[type] = I_dict[type] + 1
                break

    # I_conj_1: 因此，我能够表达自己，也不会_因为_看到无计其数的游客而怯场。
    if type==6:
        for index in indexlist:
            if index<(len(wordlist)-1) and ptaglist[index] == 'c' and not ptaglist[index+1] == 'w' and \
                    commonTools.num_hanzi(wordlist[index])>=1:
                wordlist[index] = ''
                I_dict[type] = I_dict[type] + 1
                break

    # I_v_de_n: 太阳出来_的_同时他开始准备冲浪了。
    if type==7:
        for index in indexlist:
            if index>=1 and index<(len(wordlist)-1) and wordlist[index]=='的' and ptaglist[index-1] == 'v' and ptaglist[index+1] == 'n':
                wordlist[index] = ''
                I_dict[type] = I_dict[type] + 1
                break

    # I_subj_1: _毒品_对身体不好，对环境也不好，而且对青少年的教育也不好。
    if type == 8:
        if ptaglist[0]=='r' or ptaglist[0]=='n' or ptaglist[0]=='vn' or ptaglist[0]=='an':
            wordlist[0] = ''
            I_dict[type] = I_dict[type] + 1

    # I_adj_de_n: 电影里面有一个很幸福_的_家庭：妈妈，爸爸，哥哥，姊姊还有妹妹。
    if type==9:
        for index in indexlist:
            if index>=1 and index<(len(wordlist)-1) and wordlist[index]=='的' and ptaglist[index-1] == 'a' and ptaglist[index+1] == 'n':
                wordlist[index] = ''
                I_dict[type] = I_dict[type] + 1
                break

    # I_fang_1: 所以从那时候_起_，他们两个不能再见面了。
    if type==10:
        for index in indexlist:
            if ptaglist[index] == 'f' and commonTools.num_hanzi(wordlist[index])>=1:
                wordlist[index] = ''
                I_dict[type] = I_dict[type] + 1
                break

    # I_zhuci_1: 我很小的时候已经看_过_这部电影了。
    if type==11:
        for index in indexlist:
            if index>=1 and ptaglist[index] == 'u' and ptaglist[index-1]=='v' and commonTools.num_hanzi(wordlist[index])>=1:
                wordlist[index] = ''
                I_dict[type] = I_dict[type] + 1
                break

    # I_perpverb_1: 他们见面，有一个共同点就是_对_音乐的兴趣。
    # 还有很多电影也_使用_这样的方式。
    if type==12:
        for index in indexlist:
            if index<(len(wordlist)-1) and (ptaglist[index] == 'p' or ptaglist[index] == 'v') and \
                (ptaglist[index+1]=='n' or ptaglist[index+1]=='r') and commonTools.num_hanzi(wordlist[index])>=1:
                wordlist[index] = ''
                I_dict[type] = I_dict[type] + 1
                break

    # I_n_de_n: 但是因为被跳舞团_的_人员发现他们就不喜欢这个女生，很看不起她。
    if type==13:
        for index in indexlist:
            if index>=1 and index<(len(wordlist)-1) and wordlist[index] == '的' and ptaglist[index-1]=='n' and ptaglist[index+1]=='n':
                wordlist[index] = ''
                I_dict[type] = I_dict[type] + 1
                break

    # I_adv_adj: 起初，这个男孩子_很_胆小，甚至因害怕而舍弃女孩子跑掉了。
    if type==14:
        for index in indexlist:
            if index<(len(wordlist)-1) and ptaglist[index]=='d' and ptaglist[index+1]=='a' and commonTools.num_hanzi(wordlist[index])>=1:
                wordlist[index] = ''
                I_dict[type] = I_dict[type] + 1
                break

    # I_perp_n_r: 这次侯导演会讲到关于_在_柏林得了金熊奖的故事，演讲后有Ｑ＆Ａ的时间。
    if type==15:
        for index in indexlist:
            if index<(len(wordlist)-1) and ptaglist[index]=='p' and (ptaglist[index+1]=='n' or
                ptaglist[index+1]=='vn' or ptaglist[index+1]=='an' or ptaglist[index+1]=='nr' or
                ptaglist[index+1]=='nt' or ptaglist[index+1]=='nz' or ptaglist[index+1]=='ns' or
                ptaglist[index+1]=='r') and commonTools.num_hanzi(wordlist[index])>=1:
                wordlist[index] = ''
                I_dict[type] = I_dict[type] + 1
                break

    # I_v_u_d: 志玲姊那天穿_得_很休闲，表现得就好像自己也是学生，让我们都感受到她的热情。
    if type==16:
        for index in indexlist:
            if index>=1 and (ptaglist[index]=='d' or ptaglist[index]=='u') and ptaglist[index-1]=='v' and commonTools.num_hanzi(wordlist[index])>=1:
                wordlist[index] = ''
                I_dict[type] = I_dict[type] + 1
                break

    # I_rn_r_1: 像你_这样_一个侯迷，这次的活动应该不会错过。
    if type==17:
        for index in indexlist:
            if index>=1 and ptaglist[index]=='r' and (ptaglist[index-1]=='r' or ptaglist[index-1]=='n' or
                ptaglist[index-1]=='vn' or ptaglist[index-1]=='an' or ptaglist[index-1]=='ns' or
                ptaglist[index-1]=='nz' or ptaglist[index-1]=='nt' or ptaglist[index-1]=='nr') and \
                commonTools.num_hanzi(wordlist[index])>=1:
                wordlist[index] = ''
                I_dict[type] = I_dict[type] + 1
                break

    # I_end_le: 好久没听到你的消息了！
    if type==18:
        for index in indexlist:
            if index<(len(wordlist)-1) and wordlist[index]=='了' and ptaglist[index+1]=='w':
                wordlist[index] = ''
                I_dict[type] = I_dict[type] + 1
                break

    # I_hai_shi: 虽然我是外国人，我还_是_了解一点台湾文化。
    if type == 19:
        for index in indexlist:
            if wordlist[index] == '还是':
                wordlist[index] = '还'
                I_dict[type] = I_dict[type] + 1
                break

    # I_shi_jieci: 我最喜欢这部_是_由于他们四位主角每一位都有很特别的性格和才能。
    if type==20:
        for index in indexlist:
            if index<(len(wordlist)-1) and wordlist[index] == '是' and ptaglist[index+1]=='p':
                wordlist[index] = ''
                I_dict[type] = I_dict[type] + 1
                break

    # I_hui_1: 看了第一次_会_很想要再看。
    if type==21:
        for index in indexlist:
            if index<(len(wordlist)-1) and wordlist[index] == '会' and (ptaglist[index+1]=='v' or ptaglist[index+1]=='d'):
                wordlist[index] = ''
                I_dict[type] = I_dict[type] + 1
                break

    # I_liangci_1: 他们师徒四位一起去西藏取经的每一个历程都遇见不同的妖怪如：白骨精等。
    if type==22:
        for index in indexlist:
            if ptaglist[index]=='m' and (wordlist[index].endswith('条') or wordlist[index].endswith('根') or \
                wordlist[index].endswith('张') or wordlist[index].endswith('颗') or wordlist[index].endswith('粒') or\
                wordlist[index].endswith('个') or wordlist[index].endswith('双') or wordlist[index].endswith('对') or\
                wordlist[index].endswith('位') or wordlist[index].endswith('例')):
                wordlist[index] = wordlist[index][:-1]
                I_dict[type] = I_dict[type] + 1
                break

    # I_you_noun: 我觉得这是一部很有特色的电影。
    if type==23:
        for index in indexlist:
            if index<(len(wordlist)-1) and wordlist[index]=='有' and ptaglist[index+1]=='n':
                wordlist[index] = ''
                I_dict[type] = I_dict[type] + 1
                break

    # I_yao_v: 可是如果_要_推荐一部电影的话，我选日本的「俄罗斯睡梦谭」这部电影。
    if type==24:
        for index in indexlist:
            if index<(len(wordlist)-1) and wordlist[index]=='要' and ptaglist[index+1]=='v':
                wordlist[index] = ''
                I_dict[type] = I_dict[type] + 1
                break

    # I_dou_dv: 我对电影跟音乐都很有兴趣。
    if type==25:
        for index in indexlist:
            if index<(len(wordlist)-1) and wordlist[index]=='都' and (ptaglist[index+1]=='v' or ptaglist[index+1]=='d'):
                wordlist[index] = ''
                I_dict[type] = I_dict[type] + 1
                break

    # I_fang_de: 我看银幕里的日译字幕而懂意思。
    if type==26:
        for index in indexlist:
            if index>=1 and wordlist[index]=='的' and ptaglist[index-1]=='f':
                wordlist[index] = ''
                I_dict[type] = I_dict[type] + 1
                break

    # I_v_lai: 周杰伦是个很有才华的歌手，也是个演员，这些是听来的。
    if type==27:
        for index in indexlist:
            if index>=1 and (wordlist[index]=='来' or wordlist[index]=='下来') and ptaglist[index-1]=='v':
                wordlist[index] = ''
                I_dict[type] = I_dict[type] + 1
                break

    for word in wordlist:
        newsen = newsen + word

    return newsen

## *******************************
## D类型
## *******************************
D_dict = {}
for index in range(1, 17):
    D_dict[index] = 0
def Make_D_ALLTypes(sence, type=1):
    newsen = ''
    posrest = commonTools.postagging(sence)
    wordlist = list()
    ptaglist = list()
    for word, ptag in posrest:
        wordlist.append(word)
        ptaglist.append(ptag)

    indexlist = [i for i in range(len(wordlist))]
    random.shuffle(indexlist)

    # D_mq_de_n: 他虽然总共参加三次_的_高考。
    if type==1:
        for index in indexlist:
            if index<(len(wordlist)-1) and (ptaglist[index]=='m' or ptaglist[index]=='q') and (ptaglist[index+1]=='n' or
                ptaglist[index+1]=='vn' or ptaglist[index+1]=='an' or ptaglist[index+1]=='nt' or \
                ptaglist[index+1]=='nz' or ptaglist[index+1]=='nr' or ptaglist[index+1]=='ns'):
                wordlist[index] = wordlist[index]+'的'
                D_dict[type] = D_dict[type]+1
                break

    # D_end_de: 但也有相当部分的人学吸烟是为了装酷_的_。
    if type==2:
        for index in indexlist:
            if index<(len(wordlist)-1) and ptaglist[index]=='v' and ptaglist[index+1]=='w':
                wordlist[index] = wordlist[index]+'的'
                D_dict[type] = D_dict[type]+1
                break

    # D_end_le: 但也有相当部分的人学吸烟是为了装酷_了_。
    if type==3:
        for index in indexlist:
            if index<(len(wordlist)-1) and ptaglist[index]=='v' and ptaglist[index+1]=='w':
                wordlist[index] = wordlist[index]+'了'
                D_dict[type] = D_dict[type] + 1
                break

    # D_verb_le: 每个家庭有_了_很多孩子，因此我童年的朋友大部分是邻居的朋友。
    if type==4:
        for index in indexlist:
            if ptaglist[index]=='v':
                wordlist[index] = wordlist[index]+'了'
                D_dict[type] = D_dict[type] + 1
                break

    # D_verb_dao: 如果有机会阅读_到_，也须注意“有效阅读”。
    if type==5:
        for index in indexlist:
            if ptaglist[index]=='v':
                wordlist[index] = wordlist[index]+'到'
                D_dict[type] = D_dict[type] + 1
                break

    # D_verb_di: 如果有机会阅读_地_，也须注意“有效阅读”。
    if type==6:
        for index in indexlist:
            if ptaglist[index]=='v':
                wordlist[index] = wordlist[index]+'地'
                D_dict[type] = D_dict[type] + 1
                break

    # D_verb_de: 如果有机会阅读_得_，也须注意“有效阅读”。
    if type==7:
        for index in indexlist:
            if ptaglist[index]=='v':
                wordlist[index] = wordlist[index]+'得'
                D_dict[type] = D_dict[type] + 1
                break

    # D_n_shang_v: 随着年龄的增长，我毕业后慢慢进入社会上做事。
    if type==8:
        for index in indexlist:
            if index<(len(wordlist)-1) and ptaglist[index]=='n' and ptaglist[index+1]=='v' and commonTools.num_hanzi(wordlist[index])>=1:
                wordlist[index] = wordlist[index]+'上'
                D_dict[type] = D_dict[type] + 1
                break

    # D_n_xia_v: 随着年龄的增长，我毕业后慢慢进入社会下做事。
    if type==9:
        for index in indexlist:
            if index<(len(wordlist)-1) and ptaglist[index]=='n' and ptaglist[index+1]=='v' and commonTools.num_hanzi(wordlist[index])>=1:
                wordlist[index] = wordlist[index]+'下'
                D_dict[type] = D_dict[type] + 1
                break

    # D_n_li_v: 随着年龄的增长，我毕业后慢慢进入社会里做事。
    if type==10:
        for index in indexlist:
            if index<(len(wordlist)-1) and ptaglist[index]=='n' and ptaglist[index+1]=='v' and commonTools.num_hanzi(wordlist[index])>=1:
                wordlist[index] = wordlist[index]+'里'
                D_dict[type] = D_dict[type] + 1
                break

    # D_n_zhong_v: 随着年龄的增长，我毕业后慢慢进入社会中做事。
    if type==11:
        for index in indexlist:
            if index<(len(wordlist)-1) and ptaglist[index]=='n' and ptaglist[index+1]=='v' and commonTools.num_hanzi(wordlist[index])>=1:
                wordlist[index] = wordlist[index]+'中'
                D_dict[type] = D_dict[type] + 1
                break

    # D_n_nei_v: 随着年龄的增长，我毕业后慢慢进入社会内做事。
    if type==12:
        for index in indexlist:
            if index<(len(wordlist)-1) and ptaglist[index]=='n' and ptaglist[index+1]=='v' and commonTools.num_hanzi(wordlist[index])>=1:
                wordlist[index] = wordlist[index]+'内'
                D_dict[type] = D_dict[type] + 1
                break

    # D_end_de: 我想日本的家长认为孩子的学习好坏不一定跟早恋有关。
    if type==13:
        for index in indexlist:
            if index<(len(wordlist)-1) and (ptaglist[index]=='n' or ptaglist[index]=='a' or ptaglist[index]=='v') and \
                ptaglist[index+1]=='w' and commonTools.num_hanzi(wordlist[index])>=1:
                wordlist[index] = wordlist[index]+'的'
                D_dict[type] = D_dict[type] + 1
                break

    # D_you_va: 那时，我心中怕得无法言表了。
    if type==14:
        for index in indexlist:
            if ptaglist[index]=='a' or ptaglist[index]=='v':
                wordlist[index] = '有'+wordlist[index]
                D_dict[type] = D_dict[type] + 1
                break

    # D_v_lai_u: 受灾难的时候，救活的人们没有地方住，只好像大家庭一样一起住。
    if type==15:
        for index in indexlist:
            if index<(len(wordlist)-1) and ptaglist[index]=='v' and ptaglist[index+1]=='u':
                wordlist[index] = wordlist[index]+'来'
                D_dict[type] = D_dict[type] + 1
                break

    # D_n_shi_p: 这样的惩罚措施对吸烟者来说可能是太严格。
    if type==16:
        for index in indexlist:
            if index<(len(wordlist)-1) and ptaglist[index]=='n' and ptaglist[index+1]=='p' and commonTools.num_hanzi(wordlist[index])>=1:
                wordlist[index] = wordlist[index]+'是'
                D_dict[type] = D_dict[type] + 1
                break

    for word in wordlist:
        newsen = newsen + word

    return newsen

## *******************************
## W类型
## *******************************
# 她是我的日本大学的同事，正好假期她回中国来了。
def Make_W_aword(sence):
    newsen = ''
    posrest = commonTools.postagging(sence)
    wordlist = list()
    ptaglist = list()
    for word, ptag in posrest:
        wordlist.append(word)
        ptaglist.append(ptag)

    indexlist = [i for i in range(len(wordlist))]
    random.shuffle(indexlist)

    for index in indexlist:
        if (ptaglist[index] == 'n' or ptaglist[index] == 'v' or ptaglist[index] == 'vn' or \
            ptaglist[index] == 'an' or ptaglist[index] == 'l' or ptaglist[index] == 'i' or \
            ptaglist[index] == 'a' or ptaglist[index] == 'ad' or ptaglist[index] == 'd' or \
            ptaglist[index] == 'c') and len(wordlist[index]) > 1 and len(wordlist[index]) <= 4 and \
            commonTools.num_hanzi(wordlist[index])==len(wordlist[index]):
            if len(wordlist[index]) == 4:
                wordlist[index] = wordlist[index][-2:] + wordlist[index][:-2]
            elif len(wordlist[index]) == 2:
                wordlist[index] = wordlist[index][-1:] + wordlist[index][:-1]
            elif len(wordlist[index]) == 3:
                if random.randint(1, 2) == 1:
                    wordlist[index] = wordlist[index][-1:] + wordlist[index][:-1]
                else:
                    wordlist[index] = wordlist[index][-2:] + wordlist[index][:-2]
            break

    for word in wordlist:
        newsen = newsen + word

    return newsen

W_dict = {}
for index in range(1, 9):
    W_dict[index] = 0
def Make_W_words(sence, type=1):
    newsen = ''
    posrest = commonTools.postagging(sence)
    wordlist = list()
    ptaglist = list()
    for word, ptag in posrest:
        wordlist.append(word)
        ptaglist.append(ptag)

    indexlist = [i for i in range(len(wordlist))]
    random.shuffle(indexlist)

    # W_vd_rn: 它们总是告诉我没事。
    if type==1:
        for index in indexlist:
            if index<(len(wordlist) - 1) and (ptaglist[index] == 'v' or
                ptaglist[index] == 'd') and (ptaglist[index + 1] == 'r' or ptaglist[index + 1] == 'n' or
                ptaglist[index + 1] == 'vn' or ptaglist[index + 1] == 'an' or ptaglist[index+1] == 'ns' or
                ptaglist[index+1] == 'nz' or ptaglist[index+1] == 'nr' or ptaglist[index+1] == 'nt'):
                tmp = wordlist[index]
                wordlist[index] = wordlist[index+1]
                wordlist[index+1] = tmp
                W_dict[type] = W_dict[type]+1
                break

    # W_rn_vd: 我想他可能现在不需要那些书。
    if type==2:
        for index in indexlist:
            if index<(len(wordlist) - 1) and (ptaglist[index+1] == 'v' or
                ptaglist[index+1] == 'd') and (ptaglist[index] == 'r' or ptaglist[index] == 'n' or
                ptaglist[index] == 'vn' or ptaglist[index] == 'an' or ptaglist[index] == 'ns' or
                ptaglist[index] == 'nz' or ptaglist[index] == 'nr' or ptaglist[index] == 'nt'):
                tmp = wordlist[index]
                wordlist[index] = wordlist[index+1]
                wordlist[index+1] = tmp
                W_dict[type] = W_dict[type]+1
                break

    # W_v_v: 静音环境应该是对人体有危害的。
    if type==3:
        for index in indexlist:
            if index<(len(wordlist) - 1) and ptaglist[index] == 'v' and ptaglist[index+1] == 'v':
                tmp1 = wordlist[index]
                tmp2 = wordlist[index+1]
                wordlist[index] = tmp2
                wordlist[index+1] = tmp1
                W_dict[type] = W_dict[type]+1
                break

    # W_d_v: 我国近年也开始不允许在公共场所边走边抽烟。
    if type==4:
        for index in indexlist:
            if index<(len(wordlist) - 1) and ((ptaglist[index] == 'd' or ptaglist[index] == 'ad') and
                ptaglist[index+1] == 'v') or (ptaglist[index] == 'v' and (ptaglist[index+1] == 'd' or ptaglist[index+1] == 'ad')):
                tmp1 = wordlist[index]
                tmp2 = wordlist[index+1]
                wordlist[index] = tmp2
                wordlist[index+1] = tmp1
                W_dict[type] = W_dict[type]+1
                break

    # W_mq_ndea: 我们当了好几年朋友了。
    if type==5:
        for index in indexlist:
            if index<(len(wordlist) - 2) and ptaglist[index] == 'm' and \
                (ptaglist[index+1] == 'n' or ptaglist[index+1] == 'u' or ptaglist[index+1] == 'a'):
                tmp1 = wordlist[index]
                tmp2 = wordlist[index+1]
                wordlist[index] = tmp2
                wordlist[index+1] = tmp1
                W_dict[type] = W_dict[type]+1
                break
            if index<(len(wordlist) - 2) and ptaglist[index] == 'm' and \
                ptaglist[index+1] == 'q' and (ptaglist[index+2] == 'n' or ptaglist[index+2] == 'u' or ptaglist[index+2] == 'a'):
                tmp1 = wordlist[index]
                tmp2 = wordlist[index+1]
                wordlist[index] = wordlist[index+2]
                wordlist[index+1] = tmp1
                wordlist[index + 2] = tmp2
                W_dict[type] = W_dict[type]+1
                break

    # W_p_n_vd: 所以我想最大限度地利用在中国留学的优势。
    if type==6:
        for index in indexlist:
            if index<(len(wordlist) - 2) and ptaglist[index] == 'p' and (ptaglist[index+1] == 'r' or
                ptaglist[index+1] == 'n' or ptaglist[index+1] == 'vn' or ptaglist[index+1] == 'an' or
                ptaglist[index+1] == 'ns' or ptaglist[index+1] == 'nz' or ptaglist[index+1] == 'nr' or
                ptaglist[index+1] == 'nt') and (ptaglist[index+2] == 'v' or ptaglist[index+2] == 'd'):
                tmp1 = wordlist[index]
                tmp2 = wordlist[index+1]
                wordlist[index] = wordlist[index+2]
                wordlist[index+1] = tmp1
                wordlist[index + 2] = tmp2
                W_dict[type] = W_dict[type]+1
                break

    # W_vd_p_n: 因为，烟雾刺激就会对人体有危害。
    if type==7:
        for index in indexlist:
            if index<(len(wordlist) - 2) and (ptaglist[index] == 'v' or ptaglist[index] == 'd') and \
                ptaglist[index+1] == 'p' and (ptaglist[index + 2] == 'r' or ptaglist[index + 2] == 'n' or
                ptaglist[index + 2] == 'vn' or ptaglist[index + 2] == 'an' or ptaglist[index + 2] == 'ns' or
                ptaglist[index + 2] == 'nz' or ptaglist[index + 2] == 'nr' or ptaglist[index + 2] == 'nt'):
                tmp1 = wordlist[index + 1]
                tmp2 = wordlist[index + 2]
                wordlist[index+2] = wordlist[index]
                wordlist[index] = tmp1
                wordlist[index+1] = tmp2
                W_dict[type] = W_dict[type]+1
                break

    # W_rn_t: 我们平时把自己的门口打扫得干净。
    if type==8:
        for index in indexlist:
            if index<(len(wordlist) - 1) and ptaglist[index+1] == 't' and (ptaglist[index] == 'r' or
                ptaglist[index] == 'n' or ptaglist[index] == 'vn' or ptaglist[index] == 'an' or ptaglist[index] == 'ns' or
                ptaglist[index] == 'nz' or ptaglist[index] == 'nr' or ptaglist[index] == 'nt'):
                tmp = wordlist[index]
                wordlist[index] = wordlist[index+1]
                wordlist[index+1] = tmp
                W_dict[type] = W_dict[type]+1
                break

    for word in wordlist:
        newsen = newsen + word

    return newsen


#################
### MAKE DATA ###
#################
def makedata_R_Perp():
    filedir = 'data_raw/THUCNews/for_enhance/'
    filenames = ['星座','彩票','时尚','房产','游戏','家居','时政','财经','教育','社会','娱乐','体育','股票','科技']

    strslist = list()
    for filename in filenames:
        filestrs = open(filedir + filename + '.txt', 'r', encoding='utf-8').readlines()
        for sstr in filestrs:
            if random.randint(1, 10)==1:
                sstr = commonTools.rmSingleByte(sstr.strip())
                if ' ' not in sstr.strip():
                    strslist.append(sstr.strip())

    index = [i for i in range(len(strslist))]
    random.shuffle(index)

    newfile = open('dataEnhance/makedata/Make_R_Perp_ALL.txt', 'w', encoding='utf-8')
    for id in index:
        sstr = strslist[id].strip().replace('','').replace('','')
        newsen = Make_R_perp(sstr)
        if not newsen==sstr:
            newfile.write(sstr + '\n' + newsen + '\n******************************\n')

    for perp in perp_list:
        for p in perp:
            print(p+": "+str(p_dict[p]))

def makedata_R_syno():
    filedir = 'data_raw/THUCNews/for_enhance/'
    filenames = ['星座','彩票','时尚','房产','游戏','家居','时政','财经','教育','社会','娱乐','体育','股票','科技']

    strslist = list()
    for filename in filenames:
        filestrs = open(filedir + filename + '.txt', 'r', encoding='utf-8').readlines()
        for sstr in filestrs:
            if random.randint(1, 10)==1:
                sstr = commonTools.rmSingleByte(sstr.strip())
                if ' ' not in sstr.strip():
                    strslist.append(sstr.strip())

    index = [i for i in range(len(strslist))]
    random.shuffle(index)

    newfile = open('dataEnhance/makedata/Make_R_Syno_ALL.txt', 'w', encoding='utf-8')
    for id in index:
        sstr = strslist[id].strip().replace('','').replace('','')
        newsen = Make_R_syno(sstr)
        if not newsen==sstr:
            newfile.write(sstr + '\n' + newsen + '\n******************************\n')

def makedata_aword():
    filedir = 'data_raw/THUCNews/for_enhance/'
    filenames = ['星座','彩票','时尚','房产','游戏','家居','时政','财经','教育','社会','娱乐','体育','股票','科技']

    strslist = list()
    for filename in filenames:
        filestrs = open(filedir + filename + '.txt', 'r', encoding='utf-8').readlines()
        for sstr in filestrs:
            if random.randint(1,20)==1:
                sstr = commonTools.rmSingleByte(sstr.strip())
                if ' ' not in sstr.strip():
                    strslist.append(sstr.strip())

    index = [i for i in range(len(strslist))]
    random.shuffle(index)

    newfile = open('dataEnhance/makedata/Make_W_aword_ALL.txt', 'w', encoding='utf-8')
    for id in index:
        sstr = strslist[id].strip().replace('','').replace('','')
        newsen = Make_W_aword(sstr)
        if not newsen==sstr:
            newfile.write(sstr + '\n' + newsen + '\n******************************\n')

def makedata_W_words():
    filedir = 'data_raw/THUCNews/for_enhance/'
    filenames = ['星座','彩票','时尚','房产','游戏','家居','时政','财经','教育','社会','娱乐','体育','股票','科技']

    strslist = list()
    for filename in filenames:
        filestrs = open(filedir + filename + '.txt', 'r', encoding='utf-8').readlines()
        for sstr in filestrs:
            if random.randint(1, 4)==1:
                sstr = commonTools.rmSingleByte(sstr.strip())
                if ' ' not in sstr.strip():
                    strslist.append(sstr.strip())

    index = [i for i in range(len(strslist))]
    random.shuffle(index)

    newfile = open('dataEnhance/makedata/Make_W_words_ALL.txt', 'w', encoding='utf-8')
    num_limit = [70000,70000,70000,40000,70000,70000,70000,70000]
    for id in index:
        sstr = strslist[id].strip().replace('','').replace('','')

        rand = random.randint(1,8)
        count = 0
        while count<8 and W_dict[rand]>=num_limit[rand-1]:
            rand = rand + 1
            count = count + 1
            if rand>8:
                rand=1

        if count<8:
            newsen = Make_W_words(sstr, rand)
            if not newsen==sstr:
                newfile.write(sstr + '\n' + newsen + '\n******************************\n')
        else:
            break

    for index in range(1,9):
        print(W_dict[index])

def makedata_I():
    filedir = 'data_raw/THUCNews/for_enhance/'
    filenames = ['星座','彩票','时尚','房产','游戏','家居','时政','财经','教育','社会','娱乐','体育','股票','科技']

    strslist = list()
    for filename in filenames:
        filestrs = open(filedir + filename + '.txt', 'r', encoding='utf-8').readlines()
        for sstr in filestrs:
            if random.randint(1, 2)==1:
                sstr = commonTools.rmSingleByte(sstr.strip())
                if ' ' not in sstr.strip():
                    strslist.append(sstr.strip())

    index = [i for i in range(len(strslist))]
    random.shuffle(index)

    newfile = open('dataEnhance/makedata/Make_I_ALL.txt', 'w', encoding='utf-8')
    num_limit = [100000, 10000, 50000, 10000, 10000, 10000, 100000, 10000, 100000,
                 10000, 20000, 100000, 100000, 30000, 30000, 30000, 30000, 10000,
                 1000,  10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000]
    for id in index:
        sstr = strslist[id].strip().replace('','').replace('','')

        rand = random.randint(1,27)
        count = 0
        while count<27 and I_dict[rand]>=num_limit[rand-1]:
            rand = rand + 1
            count = count + 1
            if rand > 27:
                rand = 1

        if count<27:
            newsen = I_ALLTypes(sstr, rand)
            if not newsen==sstr:
                newfile.write(sstr + '\n' + newsen + '\n******************************\n')
        else:
            break

    for index in range(1,28):
        print(I_dict[index])

def makedata_D():
    filedir = 'data_raw/THUCNews/for_enhance/'
    filenames = ['星座','彩票','时尚','房产','游戏','家居','时政','财经','教育','社会','娱乐','体育','股票','科技']

    strslist = list()
    for filename in filenames:
        filestrs = open(filedir + filename + '.txt', 'r', encoding='utf-8').readlines()
        for sstr in filestrs:
            if random.randint(1, 10) == 1:
                sstr = commonTools.rmSingleByte(sstr.strip())
                if ' ' not in sstr.strip():
                    strslist.append(sstr.strip())

    index = [i for i in range(len(strslist))]
    random.shuffle(index)

    newfile = open('dataEnhance/makedata/Make_D_ALL.txt', 'w', encoding='utf-8')
    num_limit = [30000, 10000, 10000, 10000, 10000, 10000, 10000, 30000,
                 30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000]
    for id in index:
        sstr = strslist[id].strip().replace('','').replace('','')

        rand = random.randint(1,16)
        count = 0
        while count<16 and D_dict[rand]>=num_limit[rand-1]:
            rand = rand + 1
            count = count + 1
            if rand > 16:
                rand = 1

        if count < 16:
            newsen = Make_D_ALLTypes(sstr, rand)
            if not newsen==sstr:
                newfile.write(sstr + '\n' + newsen + '\n******************************\n')
        else:
            break

    for index in range(1, 17):
        print(D_dict[index])

# 按真实比例产生各种类型的错误数据
def combineData():
    strs_D = open('dataEnhance/makedata/labels/labels_D_ALL.txt', 'r', encoding='utf-8').readlines() #36w*2/3
    strs_I = open('dataEnhance/makedata/labels/labels_I_ALL.txt', 'r', encoding='utf-8').readlines() #76w
    strs_RP = open('dataEnhance/makedata/labels/labels_R_perp_ALL.txt', 'r', encoding='utf-8').readlines() #6.67w
    strs_RS = open('dataEnhance/makedata/labels/labels_R_Syno_ALL.txt', 'r', encoding='utf-8').readlines() #101w
    strs_WA = open('dataEnhance/makedata/labels/labels_W_aword_ALL.txt', 'r', encoding='utf-8').readlines() #50w*1/6
    strs_WS = open('dataEnhance/makedata/labels/labels_W_words_ALL.txt', 'r', encoding='utf-8').readlines() #53w*1/3
    newfile = open('dataEnhance/makedata/labels_Enhance_ALL_1204.txt', 'w', encoding='utf-8')

    strslist = list()

    for index in range(len(strs_D)):
        if strs_D[index].startswith('========================================'):
            if random.randint(1, 3) >= 2:
                #astr = strs_D[index-4]+strs_D[index-3]+strs_D[index-2]+strs_D[index-1]
                astr = strs_D[index - 4] + strs_D[index - 3] + strs_D[index - 2]
                strslist.append(astr)
    for index in range(len(strs_I)):
        if strs_I[index].startswith('========================================'):
            #astr = strs_I[index-4]+strs_I[index-3]+strs_I[index-2]+strs_I[index-1]
            astr = strs_I[index - 4] + strs_I[index - 3] + strs_I[index - 2]
            strslist.append(astr)
    for index in range(len(strs_RP)):
        if strs_RP[index].startswith('========================================'):
            #astr = strs_RP[index-4]+strs_RP[index-3]+strs_RP[index-2]+strs_RP[index-1]
            astr = strs_RP[index - 4] + strs_RP[index - 3] + strs_RP[index - 2]
            strslist.append(astr)
    for index in range(len(strs_RS)):
        if strs_RS[index].startswith('========================================'):
            #astr = strs_RS[index-4]+strs_RS[index-3]+strs_RS[index-2]+strs_RS[index-1]
            astr = strs_RS[index - 4] + strs_RS[index - 3] + strs_RS[index - 2]
            strslist.append(astr)
    for index in range(len(strs_WS)):
        if strs_WS[index].startswith('========================================'):
            if random.randint(1,3)==1:
                #astr = strs_WS[index-4]+strs_WS[index-3]+strs_WS[index-2]+strs_WS[index-1]
                astr = strs_WS[index - 4] + strs_WS[index - 3] + strs_WS[index - 2]
                strslist.append(astr)
    for index in range(len(strs_WA)):
        if strs_WA[index].startswith('========================================'):
            if random.randint(1,6)==1:
                #astr = strs_WA[index-4]+strs_WA[index-3]+strs_WA[index-2]+strs_WA[index-1]
                astr = strs_WA[index - 4] + strs_WA[index - 3] + strs_WA[index - 2]
                strslist.append(astr)

    index = [i for i in range(len(strslist))]
    random.shuffle(index)

    for id in index:
        newfile.write(strslist[id])
        newfile.write('==========\n')

if __name__ == '__main__':
    #makedata_R_Perp()
    #makedata_R_syno()
    #makedata_aword()
    #makedata_W_words()
    #makedata_I()
    #makedata_D()
    combineData()
