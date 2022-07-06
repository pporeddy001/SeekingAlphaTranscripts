import re
import sys
import string
import time
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import random


def searchAlpha(tickerNameList):
  global i
  i = 0
  failCount = 0;

  file = open('C:\\Users\\pored\\source\\repos\\LTSParser-Main-\\ltsdownloads.txt', 'w')
  #file = open('C:\\Users\\Rushi\\Downloads\\LTSParser\\ltsdownloads.txt', 'w') 

  while i<1:
      global fullName
      fullName= tickerNameList[i][1]
      
   
      sitesearchFail= False

      try:
         urls = siteSearch(tickerNameList[i][0])


      except:
          print("-----SiteSearch Failed-----")
          print("Position in List:", i)    
          print("Name in TickerList:", tickerNameList[i][0])  
          print("Search Name (first):", first[0])
          print("Full Company Name:", fullName)
          failCount +=1
          print("Fail Count", failCount)
          print("---------------------------")
          sitesearchFail= True

      if sitesearchFail == False:    
        file.write(fullName + '; ' + "LowSim?" + '; ' + str(urls[2]) + '; ' + str(urls[3]) + '\n')   

      else: 
           file.write(fullName + '; ' + "Fail" + '; ' + "exception" + '; ' + "potential fix:" + '\n')   

      i = i +1
  
  print("Final Fail Count:", failCount)

def similar(a, b):
    return SequenceMatcher(None, a , b).ratio()
      

def siteSearch(ticker):
  
  proxylist=ProxyList()
  '''
  proxy=random.choice(ProxyList)
  '''

  url1 = "https://seekingalpha.com/symbol/" + ticker + "/earnings/transcripts"

  print(url1)
 

  #request1= Request(url1,proxies='"https": "https//'+proxy", headers= {'User-Agent':'Mozilla/5.0(X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'})

  request1= Request(url1, headers= {'User-Agent':'Mozilla/5.0(X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'})

  searchpage1= urlopen(request1).read()
  soup1 = BeautifulSoup(searchpage1, 'html.parser')
  soup1.prettify()

  linkList=soup1.find_all('tr')
 
  finalLink = companySelector(linkList, ticker) 


  compnumber = re.split(r"[]\b\W\b]+",finalLink[48:])

  url2= "https://www.mergentonline.com/companyannualreports.php?compnumber" + "=" + compnumber[1]

  
  
  request2= Request(url2, headers= {'User-Agent':'Mozilla/5.0(X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'})

  searchpage2= urlopen(request2).read()
  soup2 = BeautifulSoup(searchpage2, 'html.parser')
  
  downloadList=soup2.find_all('a')

  downloadLink=[]

  

  for potentialLink in downloadList:
      stringLink = str(potentialLink)

      test=stringLink.translate(str.maketrans("","", string.punctuation)).split(" ")
      
      
      keywordLetter = False
      keywordAnnual = False
      keyyear = False
      
      

      if len(test)>4:
          if test[4] == "Letter":
              keywordLetter=True
          elif test[4] == "Annual" or test[4] == "Annual10K":
              keywordAnnual=True
          
          if test[3][:-4] == "targetblank2020" :
              keyyear=True
      if (keywordAnnual == True or keywordLetter==True) and keyyear==True:
          downloadLink.append("https://www.mergentonline.com/"+potentialLink.get('href'))
      if keywordLetter==True and keyyear==True:
          return [url1, url2, "https://www.mergentonline.com/"+potentialLink.get('href')]
   

  testTitle = soup2.title.string
  outputName = testTitle[33:]

 

  outputNameWordList = outputName.split()


  simVal = similar(name.lower(), outputNameWordList[0].lower())
  print(i)
  if simVal < 0.8:

    
    print("--Low Similarity--")
    print(simVal)
    print("Position in List:", i)   
    print("Actual Title")
    print(fullName)
    print("Searched TITLE:")
    print(name)
    print(" TITLE:")
    print(outputNameWordList[0])
    print("----------------")
    if len(downloadLink) > 0:
        return [url1, url2, "true", downloadLink[0]]
    else:
        return [url1, url2, "true", "Link not Found."]
        
  if len(downloadLink) ==0:
      return [url1, url2, "false", "Link not Found."]
  return [url1, url2, "false", downloadLink[0]]


def ProxyList():
  request1= Request("https://free-proxy-list.net/", headers= {'User-Agent':'Mozilla/5.0(X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'})

  searchpage1= urlopen(request1).read()
  soup1 = BeautifulSoup(searchpage1, 'html.parser')

  siteList=soup1.find_all('td')

  proxyList =[]
  for element in siteList:
      if len(element.split(.))==4:
          proyList.append(elelment)

  return proxyList


  
  
  




def companySelector(linkList, ticker):
  
  for potentialLink in linkList:
      stringLink = str(potentialLink)
      

      #print(stringLink)

      activeStatus= False
      tickerTrue= False

      test=stringLink.translate(str.maketrans('>','<', "")).split("<")
      #print(ticker)

      if len(test) == 47:

          #print("this is the Ticker "+test[26])
          #print("this is the Active Status "+test[30])

          if test[26] == ticker:
              tickerTrue=True


          
          if test[30] == 'Active':
              activeStatus=True

      if (activeStatus==True and tickerTrue==True):

          
          return "https://www.mergentonline.com/"+ potentialLink.find_all('a')[0].get('href')

          

