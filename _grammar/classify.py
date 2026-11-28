# -*- coding: utf-8 -*-
"""从「本课新语法」列生成语法卡片数据：归并 889 个细碎点 → 规范语法大类"""
import openpyxl,re,collections,json

wb=openpyxl.load_workbook(r'D:\YoYo\YoYo-study\YoYo-study\红火箭读本正文汇总.xlsx',read_only=True)
ws=wb['正文汇总']
items=[]
for row in ws.iter_rows(min_row=2,values_only=True):
    v=row[13]
    if not v: continue
    for line in str(v).split('\n'):
        line=line.strip()
        if line: items.append(re.sub(r'^\d+、\s*','',line))

pts=collections.OrderedDict()
for it in items:
    if '：' in it: head,rest=it.split('：',1)
    else: head,rest=it,''
    key=re.sub(r'\s+','',head); key=re.sub(r'(的用法|的位置|结构|语序)$','',key)
    if key not in pts: pts[key]={'name':head.strip(),'descs':set(),'exs':set()}
    if rest.strip(): pts[key]['descs'].add(rest.split('（')[0].strip())
    for m in re.findall(r'（([^）]+)）',rest): pts[key]['exs'].add(m.strip())

def nk(s): return re.sub(r'\s+','',s).lower()

TOPICS=[
 ("There be 句型","句型",["there be","there is","there are","there was","there were","there will","there be 否定"]),
 ("祈使句与日常用语","句型",["祈使句","let's","look at +","否定祈使句","please 用于礼貌请求","训练口令","祈使句 + please","祝愿表达","问候语","i'm sorry","祈使句的宾语","祈使句 look"]),
 ("感叹句","句型",["感叹句","感叹词","感叹号","感叹表达","感叹句 what","拟声词","how + 形容词","ow 表示","ooops","感叹"]),
 ("一般疑问句","句型",["一般疑问句","yes / no","yes/no","选择疑问句","be 动词疑问句","be 动词一般疑问句","do 开头一般疑问句","can 引导的一般疑问句","can 的简略回答","省略回答","have you got","do 引导的一般疑问句","把 can 提到主语前"]),
 ("特殊疑问句","句型",["特殊疑问","what 疑问","who 引导","whose 引导","where 引导","where is","how 引导","how old","how much","how fast","what / when","what / how","疑问词 how","what else","what 引导","when 询问时间"]),
 ("否定句","句型",["否定句","否定","don't","didn't","did not","won't","can't","cannot","be 动词否定","no + 名词","have no","no one","no +"]),
 ("直接引语","句型",["直接引语","引出说话人","said 的用法","引号","said 是 say"]),
 ("并列与转折（and / or / but）","句型",["并列","转折","but 表示转折","but 表转折","or 表示选择","or 表选择","or 连接","选择疑问","and 连接","and 并列","and / or","省略重复的动词","反义动词成对","反义词成对"]),
 ("陈述句与语序","句型",["陈述句","主系表","be + 形容词","be + 名词","be + 介词短语","动词单独成句","短语独立成句","语序","here is","here + be","缩写","缩写形式","that's","it's 是","what's 是","then 表顺序","时间顺序词","then 表示","then 表","语序与句号"]),
 ("be 动词与主谓一致","动词",["be动词is","be动词are","be动词am","be动词单复数","be动词复数","be动词is与","be动词is+","be动词一般现在时","主谓一致","主语和be动词","主语与谓语一致","be动词与主语一致","单数主语+is","复数主语+are","be动词is/are","时be动词","be动词表判断","be 动词 is + 形容词","be 动词 is + 名词","主语变化不影响","be动词单数用is","be动词+名词"]),
 ("一般现在时","时态",["一般现在时","三单","第三人称单数","动词原形","动词用原形","动词加 -s","三单动词","主语是复数时动词用原形","复数主语 + 动词原形","主语 we + 动词原形","主语 you + 动词原形","like to do","like doing","like 加动词","want to do","want to +","love to do","like to +","第一人称","人称代词 we 作主语","主语 i","主语 we","主语 you","主语 he","do 替代","every day","频率表达","一般现在时（","like、love、hate","need + 名词","词类意识","主语变化"]),
 ("现在进行时","时态",["现在进行时","动词 -ing","动词加 ing","动词加-ing","-ing 形式","动词-ing","加 ing","双写末尾辅音","was + 动词-ing","动词 ing","keep + 动词","keep + 宾语","go + 动词-ing","动名词","作介词宾语","作主语","动词加 -ing","-ing 作标题"]),
 ("一般过去时","时态",["过去时","过去式","was / were","was/were","was 是","were","did not","规则动词","不规则动词","单数主语配 was","be 动词过去式","主语变化时动词过去式","be + 过去分词","一般过去时否定","一般过去时疑问"]),
 ("过去进行时","时态",["过去进行时"]),
 ("一般将来时","时态",["一般将来时","will","be going to","there will be","won't"]),
 ("情态动词 can / could","动词",["情态动词","can +","can 没有人称","can 后接","can 提到句首","can 表","can 与","can / can't","can/can't","could","can 引导","can 的否定","can't +","主语为第三人称单数时 can","后接 can","第一人称 i 与 can 连用","can 没有人称和数","you 后面 can","this box can","can 不随人称","can 的用法","can 不变形式","can you...?"]),
 ("动词不定式 to do","动词",["不定式","to do","to + 动词原形","to ski","to eat","动词 + to do","need + to do","forget to","to 后面用动词原形","to do 表示目的","to do 表目的","it is fun to do","it's time to do","be ready to do","be happy to do","疑问词 how + to do","how + to do","would like to do","ask sb. to do","tell + 人 + to do","want / like + 人 + to do","wait for sb. to do","something to eat","help to do","help + to do","help 后接动词原形","stop to do","it's time","want to do sth"]),
 ("have / has 表拥有","动词",["have / has","have /has","have 与 has","have/has","have got","have 表","have 表示","have +","has 的三单","has 表","have 与 has 的选择","have 与 has 表拥有","have no","have 的用法"]),
 ("have to / must","动词",["have to","has to","had to","must"]),
 ("let / make / help + 动词原形","动词",["let +","make +","help +","help sb","help 某人","make ... out","make + 人","call + 宾语","see + 宾语","see sb","show sth","give sth","give +","give sb","双宾语","put +","ask sb","call 的用法","动词 follow","动词 carry","carry 的搭配","let go","let sb. do","put ... into","put ... in / on"]),
 ("动词短语","动词",["动词短语","短语动词","look at +","固定搭配 look at","clean up","put on","play with","play the +","go to +","be made from","get sth","get lost","let go of","动词的层次"]),
 ("感官动词与 like 表比喻","动词",["感官动词","feel 作","feel 后接","look + 形容词","look like","be like","look like / be like","be like / look like","smell","like 表比喻","like 表「像","like 作介词","be frightened","be good at"]),
 ("名词复数","名词",["名词复数","复数","加 -s","加 -es","加 -ies","-o 结尾","以 o 结尾","以 -o","y 结尾的名词","y 结尾，把 y","单复数","成对","fish 单复数","复数读音","可数名词复数","数字加可数名词复数","数词 + 名词复数","数词 two","数词 + 形容词","数词与名词","clothes 只有复数","people 作复数","名词不规则复数","名词复数加","复数特殊","不规则复数","特殊复数","名词单复数","可数名词单复数","名词复数（含不规则","名词复数不规则","名词复数规则","以元音字母加 y 结尾","the family"]),
 ("名词的构成与类别","名词",["合成名词","复合名词","名词组合","名词短语","动物名词","表示人的名词","名词与动词同形","名词的层次递进","词尾 ling","词类意识"]),
 ("不可数名词","名词",["不可数名词","hair 作不可数","some + 不可数","too much +","much 修饰","some 修饰颜色","可数与不可数","some 修饰可数名词复数和不可数"]),
 ("数量表达","名词",["some +","some 修饰","some 的用法","some 和 more","a lot of","lots of","a lot 作状语","a pair of","a piece of","a bag of","a set of","half of","数词 one","数词 + 量词","数量短语","a set","表示次数","all the +","all 与 some","most + 名词","most 表","more 表示","only 的位置","数字 1 后面","数字加","序数词","基数词作表语","数词 one / two","数词与名词搭配"]),
 ("名词所有格","名词",["所有格","of 表所属","of 短语","of 表材料","of 表","of 表示","介词 of"]),
 ("专有名词与书写规范","名词",["专有名词","字母大小写","字母大写","首字母大写","书写规范","标点","逗号的使用","字母大写与句号","句号","问号","标点与语气","字母作主语"]),
 ("人称代词","代词",["人称代词","代词 it","代词 they","代词 them","宾格","they / their","we / us","him / his","her / she","they / her","it 指代","he 指代","she 指代","it/them","代词 it/they","代词 they 指代","代词 it 指代前面","代词 it 指代动物","代词 them 指代","it 指代前面提到的物品"]),
 ("物主代词","代词",["形容词性物主代词","物主代词","its 的用法","its（","your / you","they / their 的用法","this / his / my 的用法","my（","物主代词 their","物主代词 my","his / his"]),
 ("指示代词 this / that / these","代词",["指示代词","this +","this 加","this 的","these 的用法","that 的用法","that 指较远","this one","this is...","this / that","this 的指示用法","this / his / my 的用法"]),
 ("不定冠词 a / an","冠词",["不定冠词","冠词 a","a + 单数","a + 形容词","a 修饰","a 的用法","a 与 an","a、an","a / an","an umbrella","不定冠词 a","不定冠词 an","a 与 the","冠词 a 和 the","a 与 an 的选择","a 与 an 的用法","定冠词 the 与不定冠词"]),
 ("定冠词 the 与零冠词","冠词",["定冠词","the 的用法","the +","零冠词","冠词用法","可数名词单数前要有限定词","可数名词单数前要加冠词","可数名词单数前加冠词","可数名词单数前用 a","a 与 the 的区别","名词单数前用 the","be for"]),
 ("方位与方向介词","介词",["介词 in","介词 on","介词 at","介词 up","介词 down","介词 over","介词 into","介词 onto","介词 under","介词 by","in / out","up / down","on 与 in","in / on","in / into","in、out","on 表","in 表","at 表","up 表","副词 up / down","介词 up、down","方位介词","介词表交通","介词 on 用于","介词 on 表示","on +","in / at","over / on","介词 over 表","down from","onto 表","副词 past","in / out 表示方向","on 用于具体某一天","on + 星期","on + 身体部位","on + 形容词","时间状语 on","地点状语放句首"]),
 ("其他介词","介词",["介词 for","介词 with","介词 from","介词 about","介词 to","介词 by","介词搭配","介词短语","with 表","with +","for +","from ... to","without","by myself","介词 to 表","for 表","with 短语","with 表示","for 表含义","to 表方向","to 表对象","about 表","for + doing","for + 动词ing","from / out","out of","in / for","for 表示对象","with 表方式","with 表伴随","with 表「用","介词 like","for 表「","with 表以…开头","介词 with 表示特征","with 表「和","on fire","in big danger","be for","with 表以……开头","介词 with 表示特征"]),
 ("形容词的用法","形容词与副词",["形容词","颜色词","颜色形容","描述特征","描述状态","名词作定语","复合形容词","形容词并列","形容词重复","颜色形容词","名词表形状","动物幼崽","颜色词用作名词","be + 颜色"]),
 ("副词的用法","形容词与副词",["副词","very +","very 修饰","so + 形容词","so 表示结果","程度副词","频率副词","频度副词","sometimes","often","always","later 表时间","today 放句首","时间副词","副词 fast","副词 very","副词修饰","副词 up","a lot 作状语","表示程度","表示怎么做"]),
 ("比较级与最高级","形容词与副词",["比较级","最高级","the most","more and more","比较范围","as...as","as ... as","as + 形容词","同级比较","the same","different from"]),
 ("too 的用法","形容词与副词",["too 的位置","too 放","too 表","too 表示","too much","too many","too + 形容词","be + too","too short","too 的用法","too 修饰","too / so"]),
 ("时间与条件从句","其他",["when 表示","when 引导","when / as","when / after","时间表达","时间状语","频率表达","later","if 条件句","after","时间副词 today","every day","sometimes 表频率","so 表示结果"]),
]
# 手动兜底映射（关键词没覆盖到的）
MANUAL={
 "问候语 Hello 可以连着说，表示反复打招呼（Hello, hello, hello.）":("祈使句与日常用语","句型"),
 "I'm sorry":("祈使句与日常用语","句型"),
 "词类意识":("名词的构成与类别","名词"),
 "名词短语":("名词的构成与类别","名词"),
 "合成名词":("名词的构成与类别","名词"),
 "动物名词":("名词的构成与类别","名词"),
 "以元音字母加 y 结尾":("名词复数","名词"),
 "表示人的名词":("名词的构成与类别","名词"),
 "名词与动词同形":("名词的构成与类别","名词"),
 "复合名词":("名词的构成与类别","名词"),
 "名词的层次递进":("名词的构成与类别","名词"),
 "词尾 ling":("名词的构成与类别","名词"),
 "基数词作表语":("数量表达","名词"),
 "可数与不可数":("不可数名词","名词"),
 "have 的用法":("have / has 表拥有","动词"),
 "省略重复的动词":("并列与转折（and / or / but）","句型"),
 "the family 表示“一家人”，看作一个整体":("名词复数","名词"),
 "地点状语放句首":("方位与方向介词","介词"),
 "What can you see? 把 can 提到主语前":("一般疑问句","句型"),
 "When 询问时间（When is your birthday?）":("特殊疑问句","句型"),
 "some 的用法":("数量表达","名词"),
 "some 和 more 的用法":("数量表达","名词"),
 "can 的用法":("情态动词 can / could","动词"),
 "This is...":("指示代词 this / that / these","代词"),
 "like、love、hate 后接名词表喜好（We love mud.）":("一般现在时","时态"),
 "Can you...? 表请求/能力":("情态动词 can / could","动词"),
 "祝愿表达":("祈使句与日常用语","句型"),
 "be + 过去分词表示\"被……\"":("一般过去时","时态"),
 "put ... into ... 表示位置移动（put him into the cage）":("let / make / help + 动词原形","动词"),
 "let sb. do sth.（let their penguins go）":("let / make / help + 动词原形","动词"),
 "be for":("定冠词 the 与零冠词","冠词"),
 "need + 名词":("一般现在时","时态"),
 "主语 the string 为单数，动词用 went":("一般过去时","时态"),
 "名词组合":("名词的构成与类别","名词"),
}

mapping={}
for k,v in pts.items():
    nkf=nk(k); hit=None
    for name,group,kws in TOPICS:
        for kw in kws:
            if nk(kw) in nkf or nkf in nk(kw):
                hit=(name,group); break
        if hit: break
    if not hit and v['name'] in MANUAL: hit=MANUAL[v['name']]
    mapping[k]=hit or ("待分类","其他")

stats=collections.Counter((v[0],v[1]) for v in mapping.values())
print('分类完成。大类数:',len(stats))
for (n,g),c in sorted(stats.items(),key=lambda x:-x[1]):
    print(f'{c:4d}  {g}  {n}')
# 输出每大类素材
topics=collections.OrderedDict()
for k,(name,group) in mapping.items():
    t=topics.setdefault(name,{'name':name,'group':group,'count':0,'descs':set(),'exs':set()})
    t['count']+=1
    t['descs'].update(pts[k]['descs'])
    t['exs'].update(pts[k]['exs'])
out=[{'name':t['name'],'group':t['group'],'count':t['count'],
      'descs':sorted(t['descs'])[:8],'exs':sorted(t['exs'])[:8]} for t in topics.values()]
json.dump(out,open('_grammar/topics.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(' topics.json 已生成，共',len(out),'个卡片')
