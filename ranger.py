import sys,os,re,socket,binascii,time,json,random,threading,Queue,pprint,urlparse,smtplib,telnetlib,os.path,hashlib,string,urllib2,glob,sqlite3,urllib,argparse,marshal,base64,colorama,requests
from colorama import *
from random import choice
from colorama import Fore,Back,init
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from platform import system
from Queue import Queue
from time import strftime
from urlparse import urlparse
from urllib2 import urlopen
colorama.init()


# Now regular ANSI codes should work, even in Windows
CLEAR_SCREEN = '\033[2J'
RED = '\033[31m'   # mode 31 = red forground
RESET = '\033[0m'  # mode 0  = reset
BLUE  = "\033[34m"
CYAN  = "\033[36m"
GREEN = "\033[32m"
RESET = "\033[0m"
BOLD    = "\033[m"
REVERSE = "\033[m"
#coded by mister spy
#contact me 712083179
def logo():
        clear = "\x1b[0m"
        colors = [36, 32, 34, 35, 31, 37  ]

        x = """ 

______                    _____      
| ___ \                  |_   _|     
| |_/ /__ _ _ __   __ _    | | _ __  
|    // _` | '_ \ / _` |   | || '_ \ 
| |\ \ (_| | | | | (_| |  _| || |_) |
\_| \_\__,_|_| |_|\__, |  \___/ .__/ 
                   __/ |      | |    
                  |___/       |_| v.1
                  
		CODED BY TUX-MACG1V		  
											   				  
				  
				  
			                  """
        for N, line in enumerate(x.split("\n")):
            sys.stdout.write("\x1b[1;%dm%s%s\n" % (random.choice(colors), line, clear))
            time.sleep(0.05)
logo()

def scan(site):
    ur = site.rstrip()
    ch = site.split('\n')[0].split('.')
    ip1 = ch[0]
    ip2 = ch[1]
    ip3 = ch[2]
    taz = str(ip1) + '.' + str(ip2) + '.' +str(ip3) + '.'
    i = 0
    while i <= 255:
        i += 1
        
        print "Ranging ==>" + GREEN + str(taz) + RED + str(i)
        open('Ranged.txt', 'a').write(str(taz) + str(i) + '\n')


nam = raw_input('List Ips  :')
with open(nam) as f:
    for site in f:
        scan(site)
