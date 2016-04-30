import requests,re,csv,threading
from bs4 import BeautifulSoup

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
        data = data + soup.findAll('span',{"class":"price"})
        data = map(str,data)
        extract = re.findall('\xa0([0-9]*),([0-9]*)'," ".join(data))
        temp = [i+j for i,j in extract]
        final.append(temp)

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
    finally:
        thread_list.append(t)
temp=[]
for t in thread_list:
    t.join()
for item in final:
    temp.append(" ".join(item))
z = "\n".join(temp)
with open('data.txt','w') as f:
    f.write(z)
