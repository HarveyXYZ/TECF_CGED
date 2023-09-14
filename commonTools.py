import re
import pkuseg

# 保留分割符号，置于句尾，比如标点符号
def sen_split(str, sep=u"！|。|？"):  # 分隔符可为多样的正则表达式
    wlist = re.split(sep, str)
    sepword = re.findall(sep, str)
    #sepword.insert(0, " ") # 开头（或末尾）插入一个空字符串，以保持长度和切割成分相同
    wlist = [ x+y for x,y in zip(wlist,sepword) ] # 顺序可根据需求调换
    return wlist

def is_chnChar(chr):
    if (chr >= u'\u4e00' and chr <= u'\u9fa5'):
        return True
    else:
        return False

def num_hanzi(str):
    num = 0
    for ss in str:
        if is_chnChar(ss):
            num = num+1

    return num

lexicon = [('ANAME', 'n'), ('ANUM', 'm'), ('ATIME', 't'), ('AEMAIL', 'n'), ('ALINK', 'n')]
seg = pkuseg.pkuseg(user_dict=lexicon, postag=True)
def postagging(sence):
    resut = seg.cut(sence)
    return resut

# 1995年坐8612345在公车上黯然的流a@qw.com下我脆弱的眼泪23.45,一位老23外经过看见a@2.com这样的https://zhuanlan.zhihu.com/p/338826624
# 我对我说”be a  girl, good8612345 luck“他给，2002/1/2，反面写着“good luck”，天真的ANdy我以为这是上8612345天带给。
def rmSingleByte(sstr):
    sstr = sstr.replace(' ', ' ').replace('	', ' ').replace(' ', ' ').replace(' ', ' ')

    EMAILs = re.findall(r"[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)", sstr)
    EMAILs.sort(key=lambda i:len(i), reverse=True)
    for EMAIL in EMAILs:
        sstr = sstr.replace(EMAIL, 'AEMAIL')

    TIMEs = re.findall(r'\d{4}(?:-|\/|.)\d{1,2}(?:-|\/|.)\d{1,2}', sstr)
    TIMEs.sort(key=lambda i: len(i), reverse=True)
    for TIME in TIMEs:
        sstr = sstr.replace(TIME, 'ATIME')

    NUMs = re.findall(r"\d+\.?\d*", sstr)
    NUMs.sort(key=lambda i:len(i), reverse=True)
    for NUM in NUMs:
        sstr = sstr.replace(NUM, 'ANUM')

    NAMEs = re.findall(r'[a-zA-Z][a-zA-Z\s]{0,20}[a-zA-Z]', sstr)
    NAMEs.sort(key=lambda i:len(i), reverse=True)
    for NAME in NAMEs:
        if not NAME in ['ANUM','AEMAIL','ATIME']:
            sstr = sstr.replace(NAME, 'ANAME')

    LINKs = re.findall(r"[\x00-\xff]+", sstr)
    LINKs.sort(key=lambda i: len(i), reverse=True)
    for LINK in LINKs:
        if not LINK in ['ANUM','(ANUM','ANUM)','(ANUM)','[ANUM','ANUM]','[ANUM]','{ANUM','ANUM}','{ANUM}','ANUM%','ANUM-ANUM'\
                        'ANAME','(ANAME','ANAME)','(ANAME)','[ANAME','ANAME]','[ANAME]','{ANAME','ANAME}','{ANAME}', \
                        'AEMAIL', '(AEMAIL', 'AEMAIL)', '(AEMAIL)', '[AEMAIL', 'AEMAIL]', '[AEMAIL]', '{AEMAIL', 'AEMAIL}', '{AEMAIL}', \
                        'ATIME', '(ATIME', 'ATIME)', '(ATIME)', '[ATIME', 'ATIME]', '[ATIME]', '{ATIME', 'ATIME}', '{ATIME}'] \
                and len(LINK)>=2:
            sstr = sstr.replace(LINK, 'ALINK')

    return sstr

# 全角字符转换为半角字符
def strQ2B(ustring):
    rstring = ""
    for uchar in ustring:
        if uchar=='，' or uchar=='！' or uchar=='？':
            rstring += uchar
            continue

        inside_code = ord(uchar)
        if inside_code == 12288:              # 全角空格直接转换
            inside_code = 32
        elif 65281 <= inside_code <= 65374:   # 全角字符（除空格）根据关系转化
            inside_code -= 65248
        rstring += chr(inside_code)
    return rstring
