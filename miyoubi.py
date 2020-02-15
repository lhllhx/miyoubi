import tkinter as tk, tkinter.messagebox, sys, requests, json
 
def getcookies(): #获取用户登录信息
    window.withdraw()
    URL1 = 'https://webapi.account.mihoyo.com/Api/cookie_accountinfo_by_loginticket?login_ticket=' + entry.get()
    res = requests.get(URL1)
    res_text = res.text
    json1 = json.loads(res_text)
    dataList_in = json1.get('data')
    if dataList_in['msg'] == "成功":       
        print('%s' % dataList_in['cookie_info']['cookie_token'])
        URL2 = 'https://api-takumi.mihoyo.com/apihub/api/querySignInStatus?gids=1'
        dataList_out = {'cookie_token':0,  'account_id':0}
        dataList_out['cookie_token'] = dataList_in['cookie_info']['cookie_token']
        dataList_out['account_id'] = str(dataList_in['cookie_info']['account_id'])
        print(dataList_out)
        res3 = requests.get(URL2, cookies=dataList_out)
        print(res3.cookies)
        cookies_f = open('cookies.dat', 'w+')
        cookies_f.write('%s\n' % res3.cookies['ltuid'])
        cookies_f.write('%s' % res3.cookies['ltoken'])
        cookies_f.close()
        read_data()
    else:   
        print('%s' % dataList_in['msg'])
        tk.messagebox.showinfo("登录信息已失效", '登录信息已失效，请重新登录')
        input_window()
    
 
 
def send_data(cookies_users): #任务开始
    #获取帖子信息
    URL = 'https://api-community.mihoyo.com/community/forum/home/forumPostList?forum_id=1&is_good=false&is_hot=false&page_size=20&sort=create'
    res = requests.get(URL, cookies=cookies_users)
    res_text = json.loads(res.text)
    post_id = res_text['data']['list'][0]['post_id']
    print(post_id)
    #签到功能
    sign_data = {'gids': '1'}
    URL_signin = 'https://api-takumi.mihoyo.com/apihub/api/signIn'
    res_signin = requests.post(URL_signin, json=sign_data, cookies=cookies_users)
    print(res_signin.text)
    #点赞和阅贴
    URL_upvote = 'https://api-takumi.mihoyo.com/apihub/api/upvotePost'
    URL_read = 'https://api-takumi.mihoyo.com/post/wapi/getPostFull?gids=1&post_id='
    upvote_data = {'gids':'1',  'is_cancel':False,  'post_id':'1'}
    count = 5
    while count > 0:
        upvote_data['post_id'] = post_id
        URL_read_id = URL_read + post_id
        res_read = requests.get(URL_read_id, cookies=cookies_users)
        print(res_read.text)
        res_vote = requests.post(URL_upvote, json=upvote_data, cookies=cookies_users)
        print(res_vote.text)
        post_id = str(int(post_id) - 1)
        count = count - 1
    #分享功能
    URL_share='https://api-takumi.mihoyo.com/apihub/api/getShareConf?entity_id='+ post_id
    URL_share= requests.get(URL_share, cookies=cookies_users)
    global window
    window = tk.Tk()
    window.withdraw()
    tk.messagebox.showinfo("恭喜", "任务已完成！")
    sys.exit()
 
 
def cookise_data(cookies_users):
    URL = 'https://api-takumi.mihoyo.com/apihub/api/querySignInStatus?gids=1'
    res = requests.get(URL, cookies=cookies_users)
    res_text = json.loads(res.text)
    print(res_text)
    if res_text['message'] == 'OK':
        print(res_text['message'])
        send_data(cookies_users)
    else:
        window.withdraw()
        tk.messagebox.showinfo("一键完成米游社米游币任务", '登录信息已失效，请重新登录')
        input_window()
 
 
def read_data(): #读取用户cookies
    cookies_f = open('cookies.dat', 'r')
    cookies_users = {'ltuid':'a',  'ltoken':'a'}
    ltuid = cookies_f.readline()
    ltoken = cookies_f.readline()
    cookies_users['ltuid'] = ltuid.strip()
    cookies_users['ltoken'] = ltoken.strip()
    print(cookies_users)
    cookise_data(cookies_users)
 
 
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