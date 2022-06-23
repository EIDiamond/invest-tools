# tinkoff_invest_stream_py

## Description
Main goal is download and keep market data for internal purposes, such as manual analyze, 
historical backtesting, ML purposes etc.

The tool is using [Tinkoff Invest Python gRPC client](https://github.com/Tinkoff/invest-python) api.

The tool is downloading market data via market stream in real-time. 
So, you have to keep running the tool while trading session.  


## Features
- Downloading the following information from MOEX Exchange:
  - Candle
  - Trades (executed orders)
  - Last price (price in time) 
- Saving this data in csv files

## Before Start
### Dependencies

- [Tinkoff Invest Python gRPC client](https://github.com/Tinkoff/invest-python)
<!-- termynal -->
```
$ pip install tinkoff-investments
```

### Brokerage account
Open brokerage account [Тинькофф Инвестиции](https://www.tinkoff.ru/invest/).

Do not forget to take TOKEN for API trading.

### Required configuration (minimal)
1. Open `settings.ini` file
2. Specify token for trade API in `TOKEN` (section `INVEST_API`)

### Run
Recommendation is to use python 3.10. 

Run main.py

## Configuration
Configuration can be specified via [settings.ini](settings.ini) file.
### Section INVEST_API
Specify `TOKEN` and `APP_NAME` for [Тинькофф Инвестиции](https://www.tinkoff.ru/invest/) api.
### Section DATA_COLLECTION
Specify what kind of data the tool will collect:
- 1 - True
- 0 - False

Note: `ORDER_BOOK` is under construction as this moment.  
### Section STOCK_FIGI
Specify stocks via figi.   
### Section STORAGE
Specify name of storage (class with storage logic).

`TYPE=FILES_CSV` by default, but you are able to add your own. 

### Section STORAGE_SETTINGS
Section for storage settings. 
You will have to add your own, if you add self storage class.

## How to add a new storage 
- Write a new class with storage logic
- The new class must have IStorage as super class 
- Give a name for the new class
- Extend StorageFactory class by the name and return the new class by the name
- Specify new settings in settings.ini file. 
  - Put the new class name in `STORAGE` section and `TYPE` field
  - Put new settings into `STORAGE_SETTINGS` section

## Logging
All logs are written in logs/robot.log.
Any kind of settings can be changed in main.py code

## Disclaimer
The author is not responsible for any errors or omissions, or for the trade results obtained from the use of this tool. 
