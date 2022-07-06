
import sys
import string



from createTickerList import createTickerNameList
from searchAlpha import searchAlpha


def main():
  tickerNameList=createTickerNameList()

  searchAlpha(tickerNameList)

    
if __name__=="__main__":
    main()

    