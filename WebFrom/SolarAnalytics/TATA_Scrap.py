import sys, os
print(os.path.dirname(sys.path[0]))
sys.path.append(os.path.dirname(sys.path[0]))
from urllib.request import Request, urlopen
from lxml.html import parse
from Connections.AWSMySQL import AWSMySQLConn
import bs4 as bs
import re
from ast import literal_eval as make_tuple
import pandas as pd
from datetime import date, timedelta

today = date.today()



for i in range(-1900,-2000,-1):
    date = today - timedelta(days=-1*i)
    print(date)
    url = "https://monitor.tatapowersolar.com/sds/module/solarlogweb/Statistik.php?top=100&left=70&right=120&bottom=" \
          "160&width=770&height=540&fwidth=580&fheight=280&vwidth=770&vheight=540&scaleWidth=1&scaleHeight=1&bg=1&" \
          "fs=1&afs=0&ia=0&cm=0&iw=864&ih=540&of=-1&shadow=0&scroll=1&dragndrop=0&autorefresh=0&nextrefresh=0&logid=0" \
          "&pr=0&r=457913&s=a919e3e74d4f8c0eaef2f3be7020d7a5&m=2147483820&c=5107&mode=0&offset={}&lgr=2048&grp=" \
          "1073741824&inv=1073741950&s0i=1&flag=1&channels=0&sensor=1&pyr=1&batt=1&lng=3&nodataleftoffset=0&" \
          "suppresswait=0&ymaxscale=0&logeeg=0&debug=0&ex=0".format(i)
    print(i)
    req = Request(url=url)
    webpage = urlopen(req).read()
    soup = bs.BeautifulSoup(webpage, 'lxml', from_encoding="utf8")

    time = []
    inv1 = []
    inv2 = []
    inv3 = []
    inv4 = []
    inv5 = []
    inv6 = []

    for j, script in enumerate(soup.find_all("polyline")):
        # if i==0:
        #     continue
        try:
            # print(script)
            # print(script['onmousemove'])
            text = str(script['onmousemove'])
            # print(text)
            # m = re.search('evt,(.+?),161EB3', text)
            # x = re.findall(r"\bINV \w+ \bkW", text)
            # print(x)
            pattern = re.search('INV (.*)W', text)
            result = pattern.group(1)
            inv = "INV " + result.split("[br]")[0]
            time_stamp = result.split("[br]")[1]
            generation = result.split("[br]")[2] + "W"
            # print(inv, time_stamp, generation)
            if generation.split(" ")[1] == 'W':
                gen = float(generation.split(" ")[0])
            else:
                gen = float(generation.split(" ")[0]) * 1000
            # print(inv, time_stamp, gen)
            if inv == 'INV 1 (RPI M20A)':
                time.append(time_stamp)
                inv1.append(gen)
            elif inv == 'INV 2 (RPI M50A)':
                inv2.append(gen)
            elif inv == 'INV 3 (RPI M50A)':
                inv3.append(gen)
            elif inv == 'INV 4 (RPI M50A)':
                inv4.append(gen)
            elif inv == 'INV 5 (RPI M50A)':
                inv5.append(gen)
            elif inv == 'INV 6 (RPI M50A)':
                inv6.append(gen)
        except KeyError:
            continue

    data_dict = {'Time_Stamp':time,
                 'INV 1 (RPI M20A)':inv1,
                 'INV 2 (RPI M50A)':inv2,
                 'INV 3 (RPI M50A)':inv3,
                 'INV 4 (RPI M50A)':inv4,
                 'INV 5 (RPI M50A)':inv5,
                 'INV 6 (RPI M50A)':inv6}
    data_df = pd.DataFrame(data_dict)
    data_df.to_excel("/Users/rahuldhakecha/RajGroup/Solar Anaytics/Venus Data/export_list_{}.xlsx".format(date))



