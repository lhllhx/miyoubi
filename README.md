## miyoubi
这是一个一键完成米游社的米游币的python程序

## 功能

只需要输入一次cookies就可以完成米游社所有米游币任务  

理论上cookies有效期为一年但是只有米哈游才知道cookies有效期有多长  

软件分为无提示版和有提示版，区别在软件完成任务时是否弹出已完成的提示框  

无提示版建议放在电脑计划任务里可以自动完成

## 食用方法

1，下载程序 https://share.weiyun.com/5ry0Pnd 密码 2cow6x  
并打开米游社官网https://bbs.mihoyo.com/bh3/

2，重新登录米游社（已登录的要退出重新登录）  

3，按F12打开控制台，并输入以下代码  

javascript:(function(){var a=function getCookie(name){var strCookie=document.cookie;var arrCookie=strCookie.split("; ");for(var i=0;i<arrCookie.length;i++){var arr=arrCookie[i].split("=");if(arr[0]==name)return arr[1]}return""};var b={};b.a=a("account_id");b.b=a("login_ticket");alert(JSON.stringify(b))})()  

4，复制弹窗中b冒号后的内容 注意不含引号  

5，输入到程序里面 完成！  

注意：当你需要更改账号信息或初始化程序时，请删除同目录下的cookies.dat文件

## 其他

软件使用python3.7编写并使用PyInstaller打包
