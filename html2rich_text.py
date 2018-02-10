#encoding:utf-8
import re

SPACE = " "
init_deepth = 1

#  按照tag切分成list
def parseDoc2TagList(text):
    tag_pattern = re.compile("([^<]*)(<.+?>)(.*)")
    res = []
    text = text.replace("\r\n", "")
    text = text.replace("\n", "")
    while True:
        m = tag_pattern.match(text)
        if m is None: break
        pretext, tag, text = m.group(1), m.group(2), m.group(3)
        res.append(pretext)
        res.append(tag)
        if(len(text.strip()) <= 0): break
    res = map(lambda x: x.strip(), res)
    return list(filter(lambda x: len(x), res))

# 选取body标签里的内容， 删除注释， 将<br/> 替换成<br> </br>
def extractBodyPart(olst):
    olst = list(filter(lambda x: not x.startswith("<!"), olst))
    # discard tags not in body
    lst = []
    for tag in olst:
        if tag.endswith("/>"): 
            tag = tag[0:-2] 
            lst.append(tag + '>')
            tag = tag.split(' ', 1)
            tmp = tag[0][0] + '/' + tag[0][1:] + ">"
            lst.append(tmp)
        else:
            lst.append(tag)

    b = 0
    e = len(lst)
    for i,tag in enumerate(lst):
        if tag.startswith("<body"): 
            b = i + 1
        if tag.startswith("</body"): 
            e = i
    return lst[b:e]

# 解析tag内的属性
def parseAttrs(ss):
    pattern = re.compile('(\s*[-\w]+\s*=\s*".+?")(.*)|(\s*[-\w]+)(.*)')
    ss = ss.strip()
    res = []
    while len(ss) > 0:
        match = pattern.match(ss)
        if not match: break
        if match.group(1):
            ss = match.group(2).strip()
            res.append(match.group(1))
        else:
            ss = match.group(4).strip()
            res.append(match.group(3))
    tmp = [ a.split('=') for a in res]
    attrs = {}
    for e in tmp:
        if len(e) == 1:
            attrs[e[0].strip()] = '""'
        else:
            attrs[e[0].strip()] = e[1].strip()
    return attrs

# 解析tag
def parseTag(ele):
    tp = "TEXT"; name = ""; attrs = {}
    if ele.startswith('<'): 
        tp = "TAG"
        assert(ele[-1] == '>')
        if ele.startswith("</"):
            name = ele[2:-1]
            assert(name.find(" ") == -1)
            tp = "ETAG"
        else:
            sub_eles = ele[1:-1].split(" ", 1)
            name = sub_eles[0]
            if len(sub_eles) > 1:
                attrs = parseAttrs(sub_eles[1])
    else:
        name = ele
    return (tp, name, attrs)
            

"""
type: node, text
name: 
attrs:
children:
"""
def eles2DomTree(lst, idx = 0):
    res = []
    while idx < len(lst):
        if lst[idx][0] == "TEXT":
            res.append(lst[idx][0:2])
            idx = idx + 1
        elif lst[idx][0] == "ETAG":
            return (lst[idx][1], idx + 1, res)
        else:
            tmp = eles2DomTree(lst, idx + 1)
            assert tmp[0] == lst[idx][1], tmp[0] + " " + lst[idx][1]
            one_node = ("NODE", lst[idx][1], lst[idx][2], tmp[2])
            res.append(one_node)
            idx = tmp[1]

    return ("", idx, res)

def node2Json(node, deepth):
    res = []
    res.append("{\n")
    if node[0] == "TEXT":
        s = SPACE * (deepth+1)  + "type:'text',\n"  + (deepth+1)*SPACE + "text:'%s'\n"%(node[1].replace("'", '"'))
        res.append(s)
    else:
        res.append(SPACE * (deepth + 1) + "name:'" + node[1] + "',\n")
        res.append(SPACE * (deepth + 1) + "attrs:{\n" )
        for k,v in node[2].items():
            res.append(SPACE * (deepth + 2) + "%s:%s,\n"%(k,v))
        res.append(SPACE * (deepth + 1) + "},\n" )
        res.append(SPACE * (deepth + 1) + "children: ")
        s = (",\n" + (deepth+2) *SPACE).join(nodes2Json(node[3], deepth + 2))
        res.append("[" + s + "]\n" )

    res.append(deepth*SPACE + "}")
    return "".join(res)
    
def nodes2Json(nodes, deepth):
    return list(map(lambda x: node2Json(x, deepth), nodes))

def out2wx_rich_text(nodes, outFile = None):
    deepth = init_deepth
    outStr = ""
    s1 = "%sdata: {\n"%(SPACE*deepth)
    nodes_str = nodes2Json(nodes, deepth+1)
    nodes_str = [(deepth+1)*SPACE + "node%d:["%i + nodes_str[i] + "]" for i in range(len(nodes_str))]
    s2 = ",\n".join(nodes_str)
    s3 = "\n%s}"%(deepth*SPACE)
    ss = s1 + s2 + s3
    if outFile: out2file(ss, outFile)
    return ss

# 入口函数
def parseHtml(text, outFile = None):
    lst = parseDoc2TagList(text)
    lst = extractBodyPart(lst)
    lst = list(map(parseTag, lst))
    tree = eles2DomTree(lst)
    ss = out2wx_rich_text(tree[2], outFile)
    return ss

# 输出到文件
def out2file(ss, outFile):
    out = open(outFile, "w")
    out.write(ss)
    out.close()

text = """
<html>
<head> 
<meta charset="utf-8"> 
<title>教程(runoob.com)</title> 
</head>
<body>
<h1 style="font-family:verdana;">一个标题</h1>
<p style="font-family:arial;color:red;font-size:20px;">一个段落。</p>
<p class="forg" size="10" value><img class="logo" src="img/logo.png" />  图片</p>
<div class="div-class score"> 
<div> <p> example </p> </div>
<br/>
</div>
</body>
</html>
"""

print(parseHtml(text, "D://tmp.txt"))
