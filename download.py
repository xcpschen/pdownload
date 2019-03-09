#!/usr/bin/env python3
# -*- coding: UTF-8 -*- 
import os,requests,threading,time


class Download(object):
    threadNum = 5
    
    def __init__(self,url=''):
        if url!='':
            self.url = url
        self.run()
        pass
    def doDownload(self,start,end,fd):
        
        threadname = threading.current_thread().name
        print("start thread:%s at %s" % (threadname, time.time()))
        headers = {
            "Range":"bytes=%s-%s"%(start,end),
            # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            # "Accept-Encoding": "gzip, deflate",
            # "Accept-Language": "zh-CN,zh;q=0.9",
            # "Connection": "keep-alive",
            # "Host": "xt3.wmp8.com:6403",
            # "Referer":" http://www.ghost580.com/windows10/luobo/27628.html",
            # "Upgrade-Insecure-Requests": 1,
            # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
        }
        res = requests.get(self.url,headers=headers,stream=True)
        self.threadLock.acquire()
        fd.seek(start)
        fd.write(res.content)
        fd.flush()
        self.threadLock.release()
        # for line in res.iter_lines(chunk_size=10*1024):
        #     if line:
        #         fd.write(chunk)
        print("stop thread:%s at %s" % (threadname, time.time()))
        pass
    def getFileSize(self,url):
        # headers = {
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        #     "Accept-Encoding": "gzip, deflate",
        #     "Accept-Language": "zh-CN,zh;q=0.9",
        #     "Connection": "keep-alive",
        #     "Host": "xt3.wmp8.com:6403",
        #     "Referer":" http://www.ghost580.com/windows10/luobo/27628.html",
        #     "Upgrade-Insecure-Requests": 1,
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
        # }
        header = requests.get(url).headers
        return int(header['Content-Length'])
    def createEmptyFile(self,name):
        tmf = open(name,'w')
        tmf.close()
        return True
    def run(self):
        print('run')
        # filesize = self.getFileSize(self.url)
        filesize = 4127401984
        step = filesize//self.threadNum
        print(step)
        tlist = []
        start = 0
        end   = -1
        filename = '3.iso'
        self.createEmptyFile(filename)
        self.threadLock = threading.Lock()
        with open(filename,'rb+') as f:
            fileno = f.fileno()
            while end<filesize-1:
                start = end+1
                end   = start + step -1
                if end > filesize:
                    end = filesize
                dup = os.dup(fileno)
                fd  = os.fdopen(dup,'rb+',-1)
                t   = threading.Thread(target=self.doDownload,args=(start,end,fd))
                t.start()
                tlist.append(t)
            
            for i in tlist:
                i.join()
        pass

if __name__ == "__main__":
    url ='http://xt3.wmp8.com:6403/17763.348/3/LB_WIN10_X64_3_17763.348.iso'
    Download(url)
    pass