# 恭喜你发现了宝藏！
此版本会继续维护并添加更多反爬虫处理和更多功能  

目前为止未发现米哈游封禁此程序（包括之前的基础版也未封禁 封禁的并不是此项目版本 但不建议继续使用）


此版本目前已实现：

米游币任务全部完成！

自动完成全板块点赞收藏回帖任务！

~~自动发帖~~（未实装） 

# 用前必看

此程序**严禁**分享到**nga 贴吧 米游社**等**大型社交平台**大面积传播  
具体原因可以看一下master版本的更新日志


# miyoubi
这是一个一键完成米游社的米游币的python程序

## 功能

只需要输入一次cookies就可以完成米游社所有米游币任务

登录失效会弹出提示  

理论上cookies有效期为一年但是只有米哈游才知道cookies有效期有多长  

软件分为无提示版和有提示版，区别在软件完成任务时是否弹出已完成的提示框  
无提示版建议放在电脑计划任务里可以自动完成
（本项目提供无提示版下载）

**自动完成点赞收藏任务**

## 食用方法

1 到release里下载 编译版本请到目录里dist文件夹里下下载

并打开米游社官网https://bbs.mihoyo.com/bh3/

2，重新登录米游社（已登录的要退出重新登录）  

3，按F12打开控制台，并输入以下代码  

javascript:(function(){var a=function getCookie(name){var strCookie=document.cookie;var arrCookie=strCookie.split("; ");for(var i=0;i<arrCookie.length;i++){var arr=arrCookie[i].split("=");if(arr[0]==name)return arr[1]}return""};var b={};b.a=a("account_id");b.b=a("login_ticket");alert(JSON.stringify(b))})()  

4，复制弹窗中 b冒号后的内容 注意**不含**冒号和引号（如图）  

![b](https://github.com/lhllhx/miyoubi/blob/master/b.png)

5，输入到程序里面 等待约3秒

6，完成！（有提示版本会弹出成功提示）  

注意：当你需要更改账号信息或初始化程序时，请删除同目录下的cookies.dat文件

## 开发相关

软件使用python3.7编写并使用PyInstaller打包

第三方模块：  requests  

源文件为miyoubi.py 其他为编译副产物

## 更新日记
2020.3.18
更新反爬虫处理  
更新发帖模块（未实装）

2020.3.13  
增加反爬虫处理 防检测和封禁

2020.2.28  
增加发帖模块（未实装）

2020.2.19  
实现全板块签到点赞收藏任务  
新增评论功能

2020.2.17  
全板块签到实现

2020.2.15  
修复bug  

2020.2.14  
创建项目

