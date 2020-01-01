import configparser
import io

from iexfinance.stocks import Stock
from tinydb import TinyDB, Query
from tabulate import tabulate

config_file = 'config.ini'
db = TinyDB('db.json')
watchList = []

# Load Configuration file
config = configparser.ConfigParser()
config.read(config_file)
tblFormat = config['config']['TABLE_STYLE'] 
API_TOKEN = config['config']['API_TOKEN']
print("CONFIG::LOAD_STATUS::SUCCESS") 

class StockObj:
  def __init__(self, symbol):
    self.symbol = symbol
    self.data = self.get_data()
    self.companyName = self.data['companyName']
    self.latestPrice = self.data['latestPrice']
    self.changePercent = str(round(float(self.data['changePercent'])*100, 2))+"%"

  def get_data(self):
    data = Stock(self.symbol,token=API_TOKEN)
    stock_data = data.get_quote()
    return stock_data 

class Watchlist:
    def add(symbol):
        stock = Query()
        if (not db.search(stock['symbol'] == symbol)):
            print("Adding {0} to watchlist".format(symbol))
            db.insert({'symbol': symbol})
        else: print("[DEBUG] Already Exists") 
    
    def remove(symbol):
        stock = Query()
        if (db.search(stock['symbol'] == symbol)):
            print("Removing {0} from watchlist".format(symbol))
            db.remove(stock.symbol == symbol)
        else: print("[DEBUG] Item Not Found")
    
    def display():
        for item in db:
            stock = StockObj(item['symbol'])
            stockList=[stock.symbol,stock.companyName,stock.latestPrice,stock.changePercent]
            watchList.append(stockList)
        table = watchList
        print("Pstock v0.01-ALPHA")
        print(tabulate(table, headers=["Symbol", "Company", "Price (USD)", "Change (%)"], tablefmt=tblFormat))


def main():
    Watchlist.display()
    return 0
    

main()

