#-*- coding:utf-8 -*-
import requests
import bs4

import os
import sys
import argparse

import logging
logging.basicConfig(format="%(asctime)s-[%(levelname)s]: %(message)s",level=logging.INFO)

WORKPLACE,FILENAME=os.path.split(os.path.abspath(__file__))


def input_keywords():
    keywords=input("Please input the keywords:\n")
    return keywords

def input_directory():
    directory=input("Please input a path [default='./']: ")
    if directory=="":
        directory="./"
    elif not os.path.exists(directory):
        os.mkdir(directory)
    return directory

def set_proxy():
    choice=input(
        "Select proxy type[default=4]:\n"
        "1.socks\n"
        "2.http\n"
        "3.https\n"
        "4.None\n"
        "choice: "
    )
    if choice=='1':
        porxy=input("Please input porxy [example: socks5h://user:pass@host:port]: ")
    elif choice=='2':
        porxy=input("Please input proxy [example: http://10.10.1.10:3128]: ")
    elif choice=='3':
        porxy=input("Please input proxy [example: https://10.10.1.10:3128]: ")
    elif choice=='4':
        proxy=None
    else:
        logging.error("error input")
        exit(1)
    return proxy
    
def test_connectin(url,proxy):
    r=requests.get(url,proxies=proxy)
    if r.status_code==200:
        logging.info("proxy test complete")
    else:
        logging.error("proxy error")
        exit(1)

def isKeywordin(keys,href):
    for key in keys:
        if key in href:
            return key
    return None


def loop(URL_BASE,hrefs,keys,path,proxy):
    for href in hrefs:
        if href==None:
            continue
        elif href=='/':
            continue
        elif href=='./':
            continue
        elif href=='../':
            continue
        elif "http" in href:
            continue
        elif href[-1]=='/':
            url=URL_BASE+href
            logging.info("Start Spider on URL: {}".format(url))
            loop(url,Get_hrefs(url,proxy),keys,path,proxy)
        else:
            temp=isKeywordin(keys,href)
            if temp!=None:
                save_path=path+temp+'/'
                if not os.path.exists(save_path):
                    os.mkdir(save_path)
                try:
                    r=requests.get(URL_BASE+href,stream=True,proxies=proxy)
                    with open(save_path+href,"wb") as f:
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                        logging.info("download file: {} to {}".format(href,save_path))
                except:
                    logging.warning("download error on {}".format(href))



def Get_hrefs(URL,proxy):
    logging.info("Trying get URL: {}".format(URL))
    try:
        r=requests.get(URL,proxies=proxy)
    except:
        logging.warning("Can not get URL: {}".format(URL))
        return []
    
    logging.info("Connect to URL: {}".format(URL))
    html=bs4.BeautifulSoup(r.text,"html.parser")
    a_items=html.find_all('a')
    hrefs=[a.get('href') for a in a_items]
    return hrefs


def spider_run(keys,path="./",proxy=None):
    TEST_URL="https://www.baidu.com/"
    URL="https://file.wikileaks.org/file/"
    test_connectin(TEST_URL,proxy)

    keys=list(keys.split(' '))
    
    logging.info("Trying get URL: {}".format(URL))
    try:
        r=requests.get(URL,proxies=proxy)
    except:
        logging.error("Can not get URL: {}".format(URL))
        exit(1)
    logging.info("Connect to URL: {}".format(URL))

    
    hrefs=Get_hrefs(URL,proxy)
    loop(URL,hrefs,keys,path,proxy)


        


    


if __name__=="__main__":
    parser=argparse.ArgumentParser(description="Wikileaks file spider")
    parser.add_argument("-K","--key",help="keywords for spider",type=str)
    parser.add_argument("-D","--dir",help="directory to save files",type=str,default="./")
    parser.add_argument("-P","--proxy",help="set the spider porxy",type=str,default=None)
    args=parser.parse_args()
    if args.key==None:
        parser.print_help()
        print("")
        args.key=input_keywords()
        args.dir=input_directory()
        args.proxy=set_proxy()
    
    if args.proxy!=None:
        args.proxy={
            "http":args.proxy,
            "https":args.proxy
        }
    else:
        args.proxy=None
    
    logging.info("keys: {}".format(args.key))
    logging.info("files directory: {}".format(args.dir))
    logging.info("proxy: {}".format(str(args.proxy)))

    spider_run(args.key,args.dir,args.proxy)


# URL="https://file.wikileaks.org/file/"
# # URL="https://www.baidu.com/"
# r=requests.get(URL,proxies={"https":"socks5h://127.0.0.1:1080","http":"socks5h://127.0.0.1:1080"})
# print(r.text)