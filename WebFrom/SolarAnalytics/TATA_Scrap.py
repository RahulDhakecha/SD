import sys, os
print(os.path.dirname(sys.path[0]))
sys.path.append(os.path.dirname(sys.path[0]))
from urllib.request import Request, urlopen
from lxml.html import parse
from Connections.AWSMySQL import AWSMySQLConn
import bs4 as bs













req = Request(url="https://monitor.tatapowersolar.com/sds/module/solarlogweb/Statistik.php?top=100&left=70&right=120&bottom=160&width=770&height=540&fwidth=580&fheight=280&vwidth=770&vheight=540&scaleWidth=1&scaleHeight=1&bg=1&fs=1&afs=0&ia=0&cm=0&iw=864&ih=540&of=-1&shadow=0&scroll=1&dragndrop=0&autorefresh=0&nextrefresh=0&logid=0&pr=0&r=393937&s=a919e3e74d4f8c0eaef2f3be7020d7a5&m=2147483820&c=5107&mode=0&offset=0&lgr=2048&grp=1073741824&inv=1073741950&s0i=1&flag=1&channels=0&sensor=1&pyr=1&batt=1&lng=3&nodataleftoffset=0&suppresswait=0&ymaxscale=0&logeeg=0&debug=0&ex=0")
webpage = urlopen(req).read()
soup = bs.BeautifulSoup(webpage, 'lxml', from_encoding="utf8")
# desc = soup.find_all("script",type="text/javascript").descendants
# for desc in list(soup.find_all("script",type="text/javascript").descendants):
#     print(list(desc)[0])
# for i, script in enumerate(soup.find_all("script",type="text/javascript")):
#     if i==0:
#         continue
#     print(list(script.descendants))
# print(soup.polyline)
for i, script in enumerate(soup.find_all("polyline")):
    # if i==0:
    #     continue
    try:
        print(script)
        print(script['onmousemove'])
    except:
        continue
    # for i in script.children:
    #     print(i)
    # print(list(script.descendants))

