import requests,re,csv,threading
from bs4 import BeautifulSoup

def output_converter(item):
    if item and len(item)>1:
        item = int(item[0])+int(item[1])
    elif item:
        item = int(item[0])
    else :
        return None
    return item

http_proxy  = "http://10.3.100.207:8080"
https_proxy = "https://10.3.100.207:8080"
ftp_proxy   = "ftp://10.3.100.207:8080"
proxyDict = { "http"  : http_proxy, "https" : https_proxy,"ftp"   : ftp_proxy}

def dict_information_access():
    with open('TripAdvisorValidURLs.csv','r') as f:
        reader = csv.reader(f)
        links = [str(line)[2:-2] for line in reader]
        return links

def web_scrapping(url,final):
    global proxyDict
    r = requests.get(url,proxies = proxyDict)
    html = r.content
    soup = BeautifulSoup(html,'lxml')
    data = soup.findAll('div',{"class":"price"})
    data = map(str,data)
    extract = re.findall('\xa0([0-9]*),([0-9]*)'," ".join(data))
    extract = map(output_converter,final)
    final.append(extract)

class mythread(threading.Thread):
    def __init__(self,threadid,url,final):
        threading.Thread.__init__(self)
        self.threadid=threadid
        self.url = url
        self.final = final
    def run(self):
        print "Starting thread "+ str(self.threadid)
        web_scrapping(self.url,self.final)

final=[]
thread_list=[]
links = dict_information_access()
for i in xrange(len(links)):
    t = mythread(i,links[i],final)
    try:
        t.start()
    except:
        break
    thread_list.append(t)
for t in thread_list():
    t.join()
print len(final)
