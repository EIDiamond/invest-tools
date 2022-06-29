# tinkoff_invest_stream_py

## Description
Main goal is download and keep market data for internal purposes, such as manual analyze, 
historical backtesting, ML purposes etc.

The tool is using [Tinkoff Invest Python gRPC client](https://github.com/Tinkoff/invest-python) api and collecting data from MOEX Exchange.

Please note:
1. The tool is downloading market data via market stream in **real-time**. 
So, you have to keep it running while trading session.   

2. Moreover, you have to start it before start main trade session and stop after. 
Sometimes, market stream can hang between trade sessions. 
I strongly recommend keeping it running only while trade session.

3. If you start the tool before start trading session, the tool will wait till start. But you still have to stop it manually.

4. Also, market stream can hang while trade session. I'm going to add something to struggle with it. But only for trade session time.  

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

Syntax:
ticker_name=figi

### Section STORAGE
Specify name of storage (class with storage logic).

`TYPE=FILES_CSV` by default, but you are able to add your own. (see below)

### Section STORAGE_SETTINGS
Section for storage settings. 
You will have to add your own, if you add your own storage class.

## How to add a new storage 
- Write a new class with storage logic
- The new class must have IStorage as super class 
- Give a name for the new class
- Extend StorageFactory class by the name and return the new class by the name
- Specify new settings in settings.ini file. 
  - Put the new class name in `STORAGE` section and `TYPE` field
  - Put new settings into `STORAGE_SETTINGS` section

## CSV files (default storage)
### Structure on file system
By default, root path is specified in `STORAGE_SETTINGS` section and `ROOT_PATH` field. 

Folders structure: `ROOT_PATH`/{figi}/{data_type_folder}/{year}/{month}/{day}/market_data.csv

{data_type_folder} can be:
- "candle" (for candles)
- "trade" (for executed orders)
- "last_price" (for last price information)

### CSV files structure
#### Candles
Headers in candles csv file: **open**, **close**, **high**, **low**, **volume**, **time**

#### Trades
Headers in trades csv file: **direction**, **price**, **quantity**, **time**

Direction: 1 - Buy, 2 - sell

#### Last Prices
Headers in last_prices csv file: **price**, **time**

## Logging
All logs are written in logs/collector.log.
Any kind of settings can be changed in main.py code

## Disclaimer
The author is not responsible for any errors or omissions, or for the trade results obtained from the use of this tool. 
