import sys, os
print(os.path.dirname(sys.path[0]))
sys.path.append(os.path.dirname(sys.path[0]))
from urllib.request import Request, urlopen
from lxml.html import parse
from Connections.AWSMySQL import AWSMySQLConn
import bs4 as bs

'''
Returns a tuple (Sector, Indistry)
Usage: GFinSectorIndustry('IBM')
'''
def GFinSectorIndustry(name):
  tree = parse(urlopen('http://www.google.com/finance?&q='+name))
  return tree.xpath("//a[@id='sector']")[0].text, tree.xpath("//a[@id='sector']")[0].getnext().text


def return_sector(company):
  try:
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36'}
    req = Request(url="https://www.google.com/search?q={}".format(company), headers=headers)
    webpage = urlopen(req).read()
    soup = bs.BeautifulSoup(webpage, 'lxml', from_encoding="utf8")
    desc = soup.find("div",class_="wwUB2c PZPZlf").descendants
    print(company, list(desc)[-1])
    return list(desc)[-1]
  except:
    return ''


# print(return_source("glenmark"))
connection = AWSMySQLConn()
client_data = connection.execute_query("select client_name from RajGroupClientList group by 1;")
# client_data['client_sector'] = client_data['client_name'].apply(return_sector)
# client_data.to_csv("/Users/rahuldhakecha/RajGroup/ClientList/Sector/RajElectricalsClientwithSector.csv", index=False)
print(client_data)