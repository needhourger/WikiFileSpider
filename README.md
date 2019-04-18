## Wiki leaks files spider

>### What's this?
* this is a web crawler that used to download files from [https://file.wikileaks.org/file/](https://file.wikileaks.org/file/)

* by setting the key words that you wants to search for. the program will download files whose name include the key words.

* if you can not connect to the website, you can also set a proxy using socks or http 
protocol.

>### Requirement
* python 3.5+
* beautifuly soup
* requests
```
pip install -r reqirements.txt
```
>### Usage
```
usage: Spider.py [-h] [-K KEY] [-D DIR] [-P PROXY]

Wikileaks file spider

optional arguments:
  -h, --help            show this help message and exit
  -K KEY, --key KEY     keywords for spider
  -D DIR, --dir DIR     directory to save files
  -P PROXY, --proxy PROXY
                        set the spider porxy
```
* Example
```
python Spider.py -K "a b c" -D ./files -P socks5h://127.0.0.1:1080
```

* Prompt

    * if you want to use proxy ,socks5 protocol, please use url like this:
    ```
    socks5h://127.0.0.1:1080
    ```
    not ```socks5://```!!! otherwise this may cause ssl error.