
def createTickerNameList():
  
  
  x = open("C:\\Users\\pored\\source\\repos\\LTSParser-Main-\\tickerlist.txt", mode = 'r')

  y = open("C:\\Users\\pored\\source\\repos\\LTSParser-Main-\\namelist.txt", mode = 'r')
  
  listLength = 504;
  
  tickerNameList = [""]*listLength # intializes ticker list
  
  
  i=0
  while i<listLength:
    
    if i > listLength:
      tickerNameList+=""

    ticker = x.readline()[:1-2]
    name= y.readline()[:1-2]

    
    if len(ticker)>4:
          ticker = ticker[:4]+" "+ticker[4]

   
    

    tickerNameList[i] = [ticker, name]
    i += 1
   


  return tickerNameList