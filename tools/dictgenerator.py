#!/usr/bin/env python
# encoding: utf-8

import sys

WIKI_SOURCE = 'http://svn.wikimedia.org/svnroot/mediawiki/trunk/phase3/includes/ZhConversion.php'
WIKI_SOURCE_LOCAL_FILE = 'ZhConversion.php'

# 最大正向匹配
def conv(string,dic):
    i = 0
    while i < len(string):
        for j in range(len(string) - i, 0, -1):
            if string[i:][:j] in dic:
                t = dic[string[i:][:j]]
                string = string[:i] + t + string[i:][j:]
                i += len(t) - 1
                break
        i += 1
    return string
 
# 生成转换字典
def mdic():    
    table = open(WIKI_SOURCE_LOCAL_FILE,'r').readlines()
    dic = {}
    name = []
    for line in table:
        if line[0] == '$':
            name.append(dic)
            dic = {}
        if line[0] == "'":
            word = line.split("'")
            dic[word[1]] = word[3]
    name.append(dic)
            
    name[3].update(name[1]) # 简繁通用转换规则(zh2Hant)加上台湾区域用法(zh2TW)
    name[4].update(name[1]) # 简繁通用转换规则(zh2Hant)加上香港区域用法(zh2HK)
    name[6].update(name[1]) # 简繁通用转换规则(zh2Hant)加上新加坡区域用法(zh2SG)
    name[5].update(name[2]) # 繁简通用转换规则(zh2Hans)加上大陆区域用法(zh2CN)
    
    return name[3], name[4], name[6], name[5]

def downloadWikiSource():
    """docstring for downloadWikiSource"""
    import urllib
    print 'Downloading', WIKI_SOURCE_LOCAL_FILE, '...'
    content = urllib.urlretrieve(WIKI_SOURCE, WIKI_SOURCE_LOCAL_FILE)
    print 'Download accomplished.'

def makeDictFile():
    print 'Parsing wiki source...'
    [dic_TW, dic_HK, dic_SG, dic_CN] = mdic()
    print 'Parse accomplished.'
    
    dic = {}
    dic['zh2TW'] = dic_TW
    dic['zh2HK'] = dic_HK
    dic['zh2SG'] = dic_SG
    dic['zh2CN'] = dic_CN
    
    print 'Saving dictionary files...'
    for f in dic.keys():
        filename = f + '.txt'
        file = open(filename, 'w')
        for k in dic[f].keys():
            content = k + '\t' + dic[f][k] + '\n'
            file.write(content)
        file.close()
    print 'Save accomplished.'

def main():
    v = sys.argv
    if len(v) <= 1 or v[1] != 'n':
        downloadWikiSource()
    makeDictFile()
    
if __name__ == '__main__':
    main()