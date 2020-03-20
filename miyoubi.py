import tkinter as tk, tkinter.messagebox, sys, requests, json,time
 
def getcookies(): #获取用户登录信息
    window.withdraw()
    URL1 = 'https://webapi.account.mihoyo.com/Api/cookie_accountinfo_by_loginticket?login_ticket=' + entry.get()
    res = requests.get(URL1)
    res_text = res.text
    json1 = json.loads(res_text)
    print(json1)
    dataList_in = json1.get('data')
    if dataList_in['msg'] == "成功":       
        print('%s' % dataList_in['cookie_info']['cookie_token'])
        URL2 = 'https://api-takumi.mihoyo.com/apihub/api/querySignInStatus?gids=1'
        dataList_out = {'cookie_token':0,  'account_id':0}
        dataList_out['cookie_token'] = dataList_in['cookie_info']['cookie_token']
        dataList_out['account_id'] = str(dataList_in['cookie_info']['account_id'])
        print(dataList_out)
        res2 = requests.get(URL2, cookies=dataList_out)
        print(res2.cookies)
        URL3='https://api-takumi.mihoyo.com/auth/api/getMultiTokenByLoginTicket?login_ticket='+entry.get()+'&token_types=3&uid='+str(dataList_in['cookie_info']['account_id'])
        res3 = requests.get(URL3)
        res3_text = res3.text
        json2 = json.loads(res3_text)  
        print(json2)
        cookies_f = open('cookies.dat', 'w+')  #写入数据文件
        cookies_f.write('%s\n' % res2.cookies['ltuid'])
        cookies_f.write('%s\n' % res2.cookies['ltoken'])
        cookies_f.write('%s' % json2['data']['list'][0]['token'])
        cookies_f.close()
        read_data()
    else:   
        print('%s' % dataList_in['msg'])  
        tk.messagebox.showinfo("一键完成米游社米游币任务", '登录信息已失效，请重新登录')
        input_window()
    

def reply(cookise,post_id):  #回复板块
    #pass
    URL="https://api-community.mihoyo.com/community/forum/reply/post"
    data={"gids":"1","post_id":"1","content":"<p>求赞求回复_(笔心心)_(笔心心)_(笔心心)</p>","structured_content":[{"insert":"求赞求回复_(笔心心)_(笔心心)_(笔心心)\n"}]}
    data["post_id"]=post_id
    res=requests.post(URL,json=data,cookies=cookise,headers=header)
    print(res.text)
    time.sleep(25)

def releasePost(cookise):  #发帖模块
    URL="https://api-takumi.mihoyo.com/post/wapi/releasePost"
    data={"gids":"1","view_type":1,"structured_content":"[{\"insert\":\"_(笔心心)求赞求回复 一起来升级吧_(笔心心)\\n\"}]","subject":"求赞求回复 一起来升级吧","f_forum_id":0,"forum_id":0,"post_id":"","cover":"","content":"<p>_(笔心心)求赞求回复 一起来升级吧_(笔心心)</p>","topic_ids":["110"]}
    header['Referer']='https://bbs.mihoyo.com/bh3/newArticle/0/1/110'
    res=requests.post(URL,json=data,cookies=cookise,headers=header)
    print(res.text)
    time.sleep(10)

def send_data(cookies_users): #任务开始
    global header
    header={'Referer':'11',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Origin' : 'https://bbs.mihoyo.com'}
   
    #发贴模块
    releasePost(cookies_users)
   
    #全板块签到功能    
    header['Referer']='https://bbs.mihoyo.com/bh3/'
    sign_data = {'gids': '1'}
    URL_signin = 'https://api-takumi.mihoyo.com/apihub/api/signIn'
    res_signin = requests.post(URL_signin, json=sign_data, cookies=cookies_users,headers=header)
    
    header['Referer']='https://bbs.mihoyo.com/ys/'
    sign_data = {'gids': '2'}
    URL_signin = 'https://api-takumi.mihoyo.com/apihub/api/signIn'
    res_signin = requests.post(URL_signin, json=sign_data, cookies=cookies_users,headers=header)
    
    header['Referer']='https://bbs.mihoyo.com/bh2/'
    sign_data = {'gids': '3'}
    URL_signin = 'https://api-takumi.mihoyo.com/apihub/api/signIn'
    res_signin = requests.post(URL_signin, json=sign_data, cookies=cookies_users,headers=header)
    print(res_signin.text)
    
    #点赞和阅贴和收藏功能
    
    #崩3板块
    #获取帖子信息
    URL = 'https://api-community.mihoyo.com/community/forum/home/forumPostList?forum_id=1&is_good=false&is_hot=false&page_size=20&sort=create' 
    #forum_id 1为崩3 26为原神 30为崩2
    res = requests.get(URL, cookies=cookies_users)
    res_text = json.loads(res.text)
    URL_upvote = 'https://api-takumi.mihoyo.com/apihub/api/upvotePost'
    URL_read = 'https://api-takumi.mihoyo.com/post/wapi/getPostFull?gids=1&post_id='
    upvote_data = {'gids':'1',  'is_cancel':False,  'post_id':'1'}
    book_URL='https://api-community.mihoyo.com/community/forum/post/assessPost'
    book_data={'gids':'1',"post_id":"1","access":"book"}
    book_cancel_data={'gids':'1',"post_id":"1","access":"book","cancel":"1"}
    count = 11
    while count > 0:
        post_id = res_text['data']['list'][count]['post_id']
        upvote_data['post_id'] = post_id
        URL_read_id = URL_read + post_id
        book_data['post_id']=res_text['data']['list'][count]['post_id']
        book_cancel_data['post_id']=res_text['data']['list'][count]['post_id']
        header['Referer']='https://bbs.mihoyo.com/bh3/article/'+post_id
        res_book = requests.get(URL_read_id, cookies=cookies_users,headers=header)
        print(res_book.text)
        res_unbook = requests.get(book_URL, cookies=cookies_users,params=book_data,headers=header)
        print(res_unbook.text)
        res_read = requests.get(book_URL, cookies=cookies_users,params=book_cancel_data,headers=header)
        print(res_read.text)
        res_vote = requests.post(URL_upvote, json=upvote_data, cookies=cookies_users,headers=header)
        print(res_vote.text)
        if(count<4):
            reply(cookies_users,post_id)
        count = count - 1
   
    #原神板块   
    URL = 'https://api-community.mihoyo.com/community/forum/home/forumPostList?forum_id=26&is_good=false&is_hot=false&page_size=20&sort=create' 
    #forum_id 1为崩3 26为原神 30为崩2
    res = requests.get(URL, cookies=cookies_users)
    res_text = json.loads(res.text)
    URL_upvote = 'https://api-takumi.mihoyo.com/apihub/api/upvotePost'
    URL_read = 'https://api-takumi.mihoyo.com/post/wapi/getPostFull?gids=1&post_id='
    upvote_data = {'gids':'1',  'is_cancel':False,  'post_id':'1'}
    book_URL='https://api-community.mihoyo.com/community/forum/post/assessPost'
    book_data={'gids':'1',"post_id":"1","access":"book"}
    book_cancel_data={'gids':'1',"post_id":"1","access":"book","cancel":"1"}
    count = 11
    while count > 0:
        post_id = res_text['data']['list'][count]['post_id']
        upvote_data['post_id'] = post_id
        URL_read_id = URL_read + post_id
        book_data['post_id']=res_text['data']['list'][count]['post_id']
        book_cancel_data['post_id']=res_text['data']['list'][count]['post_id']
        header['Referer']='https://bbs.mihoyo.com/ys/article/'+post_id
        res_book = requests.get(URL_read_id, cookies=cookies_users,headers=header)
        print(res_book.text)
        res_unbook = requests.get(book_URL, cookies=cookies_users,params=book_data,headers=header)
        print(res_unbook.text)
        res_read = requests.get(book_URL, cookies=cookies_users,params=book_cancel_data,headers=header)
        print(res_read.text)
        res_vote = requests.post(URL_upvote, json=upvote_data, cookies=cookies_users,headers=header)
        print(res_vote.text)
        if(count<4):
            reply(cookies_users,post_id)
        count = count - 1   
    
    #崩2板块
    URL = 'https://api-community.mihoyo.com/community/forum/home/forumPostList?forum_id=30&is_good=false&is_hot=false&page_size=20&sort=create' 
    #forum_id 1为崩3 26为原神 30为崩2
    res = requests.get(URL, cookies=cookies_users)
    res_text = json.loads(res.text)
    URL_upvote = 'https://api-takumi.mihoyo.com/apihub/api/upvotePost'
    URL_read = 'https://api-takumi.mihoyo.com/post/wapi/getPostFull?gids=1&post_id='
    upvote_data = {'gids':'1',  'is_cancel':False,  'post_id':'1'}
    book_URL='https://api-community.mihoyo.com/community/forum/post/assessPost'
    book_data={'gids':'1',"post_id":"1","access":"book"}
    book_cancel_data={'gids':'1',"post_id":"1","access":"book","cancel":"1"}
    count = 11
    while count > 0:
        post_id = res_text['data']['list'][count]['post_id']
        upvote_data['post_id'] = post_id
        URL_read_id = URL_read + post_id
        book_data['post_id']=res_text['data']['list'][count]['post_id']
        book_cancel_data['post_id']=res_text['data']['list'][count]['post_id']
        header['Referer']='https://bbs.mihoyo.com/bh2/article/'+post_id
        res_book = requests.get(URL_read_id, cookies=cookies_users,headers=header)
        print(res_book.text)
        res_unbook = requests.get(book_URL, cookies=cookies_users,params=book_data,headers=header)
        print(res_unbook.text)
        res_read = requests.get(book_URL, cookies=cookies_users,params=book_cancel_data,headers=header)
        print(res_read.text)
        res_vote = requests.post(URL_upvote, json=upvote_data, cookies=cookies_users,headers=header)
        print(res_vote.text)
        if(count<4):
            reply(cookies_users,post_id)
        count = count - 1 
    
    #分享功能
    header['Referer']='https://app.mihoyo.com'
    header['x-rpc-client_type']='2'
    header['x-rpc-app_version']='1.6.0'
    header['x-rpc-sys_version']='6.0.1'
    header['x-rpc-channel']='xiaomi'
    header['x-rpc-device_id']='fc5235c6-c40d-33a6-a3e6-64e97b6e9c03'
    header['x-rpc-device_name']='OPPO oppo R11s Plus'
    header['x-rpc-device_model']='oppo R11s Plus'
    header['Accept-Encoding']='gzip'
    header['User-Agent']='okhttp/3.10.0'
    del cookies_users['ltuid']
    del cookies_users['ltoken']
    URL_share='https://api-takumi.mihoyo.com/apihub/api/getShareConf?'+'entity_type=1'+'&entity_id='+ post_id 
    res_share= requests.get(URL_share, cookies=cookies_users,headers=header)
    print(res_share.text)

    #需要提示请取消注销以下三行
    #window = tk.Tk()                                       
    #window.withdraw()
    #tk.messagebox.showinfo("恭喜", "任务已完成！")
    sys.exit()
 
 
def cookise_data(cookies_users): #检测用户信息
    URL = 'https://api-takumi.mihoyo.com/apihub/api/querySignInStatus?gids=1'
    res = requests.get(URL, cookies=cookies_users)
    res_text = json.loads(res.text)
    print(res_text)
    if res_text['message'] == 'OK':
        print(res_text['message'])
        send_data(cookies_users)
    else:
        window = tk.Tk()
        window.withdraw()
        tk.messagebox.showinfo("一键完成米游社米游币任务", '登录信息已失效，请重新登录')
        input_window()
 
 
def read_data(): #读取用户cookies
    try:
        cookies_f = open('cookies.dat', 'r')
        cookies_users = {'ltuid':'a',  'ltoken':'a', 'stoken':'a' ,'stuid' :'a' }
        ltuid = cookies_f.readline()
        ltoken = cookies_f.readline()
        stoken = cookies_f.readline()
        cookies_users['ltuid'] = ltuid.strip()
        cookies_users['ltoken'] = ltoken.strip()
        cookies_users['stoken'] = stoken.strip()
        cookies_users['stuid'] = cookies_users['ltuid']
        cookies_f.close
        print(cookies_users)
        cookise_data(cookies_users)
    except IOError:
        window = tk.Tk()
        window.withdraw()
        tk.messagebox.showinfo("一键完成米游社米游币任务", '读取数据文件失败，请重新登录')
        input_window()

 
 
def input_window(): #输入界面
    global window
    window = tk.Tk()
    global entry
    sw = window.winfo_screenwidth()
    sh = window.winfo_screenheight()
    ww = 300
    wh = 200
    x = (sw - ww) / 2
    y = (sh - wh) / 2
    window.geometry('%dx%d+%d+%d' % (ww, wh, x, y))
    window.title('一键完成米游社米游币任务')
    (tk.Label(window, text='请输入login_ticket', font=('Arial', 12), width=30, height=2)).pack()
    entry = tk.Entry(window, show=None, font=('Arial', 14))
    entry.pack()
    button = tk.Button(window, text='确定', command=getcookies)
    button.pack()
    window.mainloop()
 

try:
    f = open('cookies.dat', 'r')
    f.close()
    read_data()
except IOError:
    input_window()