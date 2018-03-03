import itchat
import Weather
import Schedule

instruction = {'a': "添加定时格式：a xx:xx\n注意冒号为英文格式", 'c': "", 'd': "删除定时格式：d xx:xx\n注意冒号为英文格式", 'h': "添加定时格式：a xx:xx\n修改天气定位：直接发送定位信息\n删除定时格式：d xx:xx\n删除所有定时：da\n列出所有定时：l\n帮助：h\n注意冒号均为英文格式！"}

@itchat.msg_register('Text')
def text_reply(msg):
    sender = msg['User']['RemarkName']
    content = msg['Content'].split()
    command = content[0]
    if command == 'a':
        try:
            if content[1] not in info[sender]['times']:
                Schedule.SetDailySchedule(sender, [content[1]], info[sender]['loc'])
                info[sender]['times'].append(content[1])
                with open('info.txt', 'w') as f:
                    f.write(str(info))
                    f.close()
            print("Successfully added " + sender + "'s schedule @" + content[1])
            return u'添加成功！'
        except:
            return u'请求错误！\n' + instruction['a']
    elif command == 'd':
        try:
            if content[1] in info[sender]['times']:
                Schedule.ClearSomeone(sender + content[1])
                info[sender]['times'].remove(content[1])
                with open('info.txt', 'w') as f:
                    f.write(str(info))
                    f.close()
                print("Successfully deleted " + sender + "'s schedule @" + content[1])
                return u'删除成功！'
            else:
                return u'无此定时！'
        except:
            return u'请求错误！\n' + instruction['d']
    elif command == 'l':
        s = ""
        for each in info[sender]['times']:
            s = s + each + '\n'
        if s == "":
            return u'当前无定时！'
        else:
            return u'' + s
    elif command == 'da':
        for each in info[sender]['times']:
            Schedule.ClearSomeone(sender + each)
        info[sender]['times'] = []
        with open('info.txt', 'w') as f:
            f.write(str(info))
            f.close()
        print("Successfully deleted all schedules of " + sender)
        return u'已清除全部定时推送！'
    elif command == 'h':
        return u'' + instruction['h']
    else:
        return u'请求错误！\n' + instruction['h']

@itchat.msg_register('Map')
def mm_reply(msg):
    sender = msg['User']['RemarkName']
    res = Weather.GetPosition(msg['Url'].split('=')[1])
    if res == False:
        return u'定位获取失败...请重试！'
    else:
        try:
            for each in info[sender]['times']:
                Schedule.ClearSomeone(sender + each)
            info[sender]['loc'] = res['cid']
            info[sender]['tz'] = eval(res['tz'])
            Schedule.SetDailySchedule(sender, info[sender]['times'], info[sender]['loc'])
            with open('info.txt', 'w') as f:
                f.write(str(info))
                f.close()
            print("Successfully changed " + sender + "'s position to " + res['cid'])
            return u'定位已修改为：' + res['admin_area'] + res['location']
        except:
            print("Unsuccessfully changed location!")
            return u'定位修改失败！'
def run():
    global info
    with open('info.txt', 'r') as f:
        info = eval(f.read())
        f.close()
    itchat.run()

def LogInWechat():
    def lc():
        print('finish login')
    def ec():
        print('exit')
        exit()
    itchat.auto_login(enableCmdQR=2, loginCallback=lc, exitCallback=ec)

def GetUserName(Name):
    friend_info = itchat.search_friends(name = Name)
    if (friend_info == []):
        return False
    else:
        UserName = friend_info[0]['UserName']
        return UserName

def SendWechatMessage(Content, UserName, RemarkName, Time):
    res = itchat.send(msg=Content, toUserName=UserName)
    if (res):
        print("Successfully sent message to " + RemarkName + ' @' + Time)
        return True
    else:
        print("Unsuccessfully sent message to " + RemarkName + ' @' + Time)
        return False

def LogoutWechat():
    itchat.logout()