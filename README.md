# html2wx_rich_text

python程序：将html文本转成微信小程序富文本格式  
在开发小程序的时候，有时候需要写一些排版复杂的页面，而微信提供的富文本接口是json格式的，使用起来比较麻烦，也没有直接使用html标签来的方便  
使用这个python程序可以把编写好的html格式的文件转成微信小程序里需要的格式，再复制到对应页面的js中的data里即可    
省去了直接编写微信小程序富文本的麻烦

接口函数为：**parseHtml**； 参数为要处理的字符串和输出文件路径


例子：
输入的原始html文本(注：程序只解析body标签里的部分；如果没有body标签就解析全部内容)
```
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
```

输出的微信小程序富文本格式如下
```
 {
  node0:{
   name:'h1',
   attrs:{
    style:"font-family:verdana;",
   },
   children: [{
     type:'text',
     text:'一个标题'
    }]
  },
  node1:{
   name:'p',
   attrs:{
    style:"font-family:arial;color:red;font-size:20px;",
   },
   children: [{
     type:'text',
     text:'一个段落。'
    }]
  },
  node2:{
   name:'p',
   attrs:{
    class:"forg",
    size:"10",
    value:,
   },
   children: [{
     name:'img',
     attrs:{
      class:"logo",
      src:"img/logo.png",
     },
     children: []
    },
    {
     type:'text',
     text:'图片'
    }]
  },
  node3:{
   name:'div',
   attrs:{
    class:"div-class score",
   },
   children: [{
     name:'div',
     attrs:{
     },
     children: [{
       name:'p',
       attrs:{
       },
       children: [{
         type:'text',
         text:'example'
        }]
      }]
    },
    {
     name:'br',
     attrs:{
     },
     children: []
    }]
  }
 }
```

