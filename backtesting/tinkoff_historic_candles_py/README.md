# tinkoff_historic_candles_py

## Description
Historical backtesting tool based on historical candles.

Candles are downloading via [Tinkoff Invest Python gRPC client](https://github.com/Tinkoff/invest-python) api.

The main goal is to use the tool with [invest-bot](https://github.com/EIDiamond/invest-bot) project.
Test and tune strategies for the bot. 

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
### Section TEST_STRATEGY
Detailed settings for test strategy on historical candles.    

- `STRATEGY_NAME` - name of algorithm
- `TICKER` - ticker name 
- `FIGI` - figi of stock. Required for API
- `MAX_LOTS_PER_ORDER` - Maximum count of lots per order

### Section TEST_STRATEGY_SETTINGS

Detailed settings for strategy. Strategy class reads and parses settings manually.  

Note: Only one strategy in configuration can be specified.

## Test strategy details

Test strategy on historical candles (1 min interval) for last 7 days: 
- Strategy class analyses candles and returns signal (long or short) if needed  
- If signal exists, historical candles use last price to check take profit or stop loss price levels
- If stop or take price levels are confirmed, strategy will start find signals again
- In the end, test results with summary will be written in log file
- You can analyze it and make a decision about next steps

## How to add a new strategy
- Write a new class with trade logic
- The new class must have IStrategy as super class 
- Give a name for the new class
- Extend StrategyFactory class by the name and return the new class by the name
- Specify new settings in settings.ini file. Put the new class name in `STRATEGY_NAME`
- Test the new class on historical candles

## Logging
All logs are written in logs/test.log.
Any kind of settings can be changed in main.py code

## Project change log
[Here](CHANGELOG.md)

## Disclaimer
The author is not responsible for any errors or omissions, or for the trade results obtained from the use of this tool. 
