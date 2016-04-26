import requests,re
from bs4 import BeautifulSoup

http_proxy  = "http://10.3.100.207:8080"
https_proxy = "https://10.3.100.207:8080"
ftp_proxy   = "ftp://10.3.100.207:8080"

proxyDict = { "http"  : http_proxy, "https" : https_proxy,"ftp"   : ftp_proxy}
url = 'https://www.tripadvisor.in/MiniMetaCRAjax?detail=190176&inMonth=11%202016&inDay=1&outMonth=11%202016&outDay=2&adults=2&rooms=1&area=QC_Meta_Mini&returnAllOffers=true&imp=true&metaReferer=Hotel_Review&baseLocId=193049&metaRequestTiming=1454318641754&isFirstPageLoad=false&finalRequest=true&isDateChangedRequest=true'
r = requests.get(url,proxies = proxyDict)
html = r.content
soup = BeautifulSoup(html,'lxml')
data = soup.findAll('div',{"class":"price"}) #"no_cpu offer wrap premium                   avail                  hacComplete                "})
data = map(str,data)
#find an appropriate way to do this matching
final = re.findall('\xa0[0-9]*,[0-9]*'," ".join(data))
print final
