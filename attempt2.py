import pprint
import smtplib
import ssl

import numpy as np
import pandas as pd
import yfinance as yf

from send_email import Email


class Alert:
    def __init__(self, ticker, direction, alert_price, send_email='True'):
        self.ticker = ticker
        self.direction = direction
        self.alert_price = alert_price
        self.send_email = send_email


def ticker_all_info(ticker):
    pp = pprint.PrettyPrinter(width=41, compact=True)
    return pp.pprint(yf.Ticker(ticker).info)


def alert_price_reached_boolean(ticker, direction, alert_price, stock_price):

    if direction == 'decrease to':
        if stock_price <= alert_price:
            return True
        else:
            return False

    if direction == 'increase to':
        if stock_price >= alert_price:
            return True
        else:
            return False


def run_alerts(alerts_list):
    float_formatter = "{:.2f}".format

    # List of tickers, then converted into string format required for yf data download.
    tickers_list = []
    for alert_ticker in alerts_list:
        tickers_list.append(alert_ticker.ticker)
    tickers_string = ' '.join(tickers_list)

    stock_price = yf.download(
        tickers=tickers_string, period='1d', interval='1m')['Adj Close']

    most_recent = stock_price.tail(1)
    # print(most_recent)

    for alert in alerts_list:
        if most_recent.size == 1:
            stock_price = most_recent[0]
        else:
            stock_price = most_recent[alert.ticker][0]

        if alert_price_reached_boolean(alert.ticker, alert.direction, alert.alert_price, stock_price):
            if alert.send_email:
                stock_alert_email = Email(subject=f'{alert.ticker} price alert triggered - Price {alert.direction} {float_formatter(stock_price)} < {alert.alert_price}',
                                          receiver_email='viren.samani@hotmail.co.uk', body=f'https://uk.finance.yahoo.com/quote/{alert.ticker}', sender_email='pythontestvs@gmail.com')
                stock_alert_email.send_email()
                print('Email sent: ' + alert.ticker +
                      f' price alert triggered - Price {alert.direction}: ' + float_formatter(stock_price) + f' (PA: {alert.alert_price})')
            else:
                print(alert.ticker +
                      f' price alert triggered - Price {alert.direction}: ' + float_formatter(stock_price) + f' (PA: {alert.alert_price})')
        else:
            pass


if __name__ == '__main__':
    alerts_list = [
        Alert('AMZN', 'decrease to', 3200),
        Alert('AAPL', 'decrease to', 115),
        Alert('MSFT', 'decrease to', 230),
        Alert('TSLA', 'decrease to', 650)
    ]

    run_alerts(alerts_list)
    print('Completed Run.')
