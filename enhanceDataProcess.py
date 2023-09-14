import commonTools
import os
"""
基于搜狗和THU新闻数据，产生 good data
"""
def processSougouData():
    for index in range(1, 40):
        filepath = 'F:/无备份的数据/DataStorage/SogouNewsData/news_tensite_xml_parts/' + str(index) + '.txt'
        filestrs = open(filepath, 'r', encoding='utf-8').readlines()
        newfile = open('dataEnhance/googdata/sougou/' + str(index) + '.txt', 'w', encoding='utf-8')

        for index in range(0, len(filestrs)):
            sentence = filestrs[index]
            if sentence.startswith('<content>'):
                sentence = sentence.replace('<content>', '').replace('</content>', '').strip()
                sens = commonTools.sen_split(sentence)
                for sen in sens:
                    sen = cleansen(sen)
                    if commonTools.num_hanzi(sen) >= 5:
                        newfile.write(sen+'\n')

def cleansen(sen):
    sen = sen.replace('','')
    sen = sen.replace('①','')
    sen = sen.replace('②','')
    sen = sen.replace('③', '')
    sen = sen.replace('④', '')
    sen = sen.replace('⑤', '')
    sen = sen.replace('⑥', '')
    sen = sen.replace('⑦', '')
    sen = sen.replace('⑧', '')
    sen = sen.replace('⑨', '')
    sen = sen.replace('⑩', '')
    sen = sen.replace('　', ' ')
    sen = sen.replace(' ', ' ')

    while sen.find('  ') > 0:
        sen = sen.replace('  ', ' ')

    sen = sen.replace(' ，', '，')
    sen = sen.replace('， ', '，')
    sen = sen.replace('、 ', '、')
    sen = sen.replace(' 、', '、')
    sen = sen.replace('》 ', '》')
    sen = sen.replace(' 》', '》')
    sen = sen.replace(' “', '“')
    sen = sen.replace('“ ', '“')
    sen = sen.replace(' ”', '”')
    sen = sen.replace('” ', '”')
    sen = sen.replace('( ', '(')
    sen = sen.replace(' (', '(')
    sen = sen.replace('& ', '&')
    sen = sen.replace(' &', '&')
    sen = sen.replace('： ', '：')
    sen = sen.replace(' ：', '：')
    sen = sen.replace(' 。', '。')
    sen = sen.replace(' ? ', '——')
    sen = sen.replace(' ?', '——')
    sen = sen.replace('? ', '——')
    sen = sen.replace('—— ', '——')
    sen = sen.replace('% ', '%')
    sen = sen.replace(' %', '%')
    sen = sen.replace('； ', '；')
    sen = sen.replace(' ；', '；')
    sen = sen.replace('(论坛 相册 户型 样板间 地图搜索)', '')
    sen = sen.replace('(论坛 相册 户型 样板间 点评 地图搜索)', '')
    for num in range(0, 10):
        sen = sen.replace(str(num)+' ', str(num))
        sen = sen.replace(' '+str(num), str(num))
    sen = sen.strip()

    if sen.startswith('”') or sen.startswith('”'):
        sen = sen[1:]

    pos = sen.find('讯 ')
    if pos > 0:
        sen = sen[pos+2:]
    pos = sen.find('电 ')
    if pos > 0:
        sen = sen[pos+2:]
    pos = sen.find('报道 ')
    if pos > 0:
        sen = sen[pos+3:]
    pos = sen.find(')--')
    if pos > 0:
        sen = sen[pos+3:]
    pos = sen.find('记者 ')
    if pos > 0:
        if sen.find(')',pos) > pos:
            sen = sen[(sen.find(')',pos) + 1):]
        elif sen.find('）',pos) > pos:
            sen = sen[(sen.find('）',pos) + 1):]
        elif sen.find('】',pos) > pos:
            sen = sen[(sen.find('】',pos) + 1):]

    return sen.strip()

def processTHUData():
    filedir = 'F:/无备份的数据/DataStorage/THUCNews/社会/'
    newfile = open('dataEnhance/googdata/THUCNews/社会.txt', 'w', encoding='utf-8')

    for filename in os.listdir(filedir):
        filestrs = open(filedir+filename, 'r', encoding='utf-8').readlines()

        for index in range(0, len(filestrs)):
            sentence = filestrs[index].strip()
            if sentence.endswith('。') or sentence.endswith('！') or sentence.endswith('？'):
                sens = commonTools.sen_split(sentence)
                for sen in sens:
                    sen = cleansen(sen)
                    if commonTools.num_hanzi(sen) >= 5:
                        newfile.write(sen+'\n')
