import requests,re,csv,threading
from bs4 import BeautifulSoup

def dict_information_access():
    with open('TripAdvisorValidURLs.csv','r') as f:
        reader = csv.reader(f)
        links = [str(line)[2:-2] for line in reader]
        return links

def web_scrapping(url,final):
        r = requests.get(url)
        html = r.content
        soup = BeautifulSoup(html)
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
j=0
final=[]
thread_list=[]
links = dict_information_access()
while j < 12:
    for i in xrange(200):
        t = mythread(i,links[i],final)
        t.start()
        thread_list.append(t)
    j=j+1
    links = links[j+1:]
    for t in thread_list:
        t.join()
    thread_list=[]
temp=[]
for item in final:
    temp.append(" ".join(item))
z = "\n".join(temp)
with open('data.txt','w') as f:
    f.write(z)
