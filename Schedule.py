import schedule
import Weather
import Wechat

def send(Name, Loc, Time):
    WeatherStr = Weather.GetWeather(Loc)
    UserName = Wechat.GetUserName(Name)
    if (UserName == False):
        print("This user doesn't exist！")
    else:
        Wechat.SendWechatMessage(WeatherStr, UserName, Name, Time)

def SetDailySchedule(name, times, loc):
    for t in times:
        schedule.every().day.at(t).do(send, name, loc, t).tag(name + t)

def RunPending():
    schedule.run_pending()

def ClearSomeone(tag):
    schedule.clear(tag)