import Schedule
import Weather
import Wechat
import time
import _thread

global server_tz
server_tz = eval(Weather.GetPosition('auto_ip')['tz'])
print('Server timezone：' + str(server_tz))

with open('info.txt', 'r') as f:
    info = eval(f.read())
    f.close()

for name, item in info.items():
    Schedule.SetDailySchedule(name, item['times'], item['loc'])

Wechat.LogInWechat()
_thread.start_new_thread(Wechat.run, ())
print('Wechat is running in a new thread!')

while True:
    Schedule.RunPending()
    time.sleep(5)

Wechat.LogoutWechat()