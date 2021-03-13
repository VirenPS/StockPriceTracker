# import numpy as np
# import pandas as pd
# # Data viz
# import plotly.graph_objs as go

import pprint
import smtplib
import ssl

import yfinance as yf

from send_email import Email


class Alert:
    def __init__(self, ticker, alert_price, direction):
        self.ticker = ticker
        self.alert_price = alert_price
        self.direction = direction

# All Data for Ticker - Clean


def ticker_all_info(ticker):
    pp = pprint.PrettyPrinter(width=41, compact=True)
    return pp.pprint(yf.Ticker(ticker).info)
# Use: print(ticker_all_info('amzn'))

# Data Source

# TODO: Adj Close may be more useful. Closer to real time, as if published end of min? Also available: Open, Close.
# print(stock_price_condensed)


def alert_price_reached_boolean(ticker, direction, alert_price, stock_price):

    if direction == 'decreased to':
        if stock_price <= alert_price:
            return True

        else:
            return False

    if direction == 'increased to':
        if stock_price >= alert_price:
            return True
        else:
            return False


def run_alerts(alerts_list):
    tickers_string = ''
    for alert_ticker in alerts_list:
        tickers_string += alert_ticker.ticker + ' '

    stock_price = yf.download(
        tickers=tickers_string, period='1d', interval='1m')['Adj Close']

    most_recent = stock_price.tail(1)

    for alert in alerts_list:
        alert_price_reached_boolean(
            alert.ticker, alert.direction, alert.alert_price, most_recent['{alert.ticker'])


if __name__ == '__main__':
    #

    # print(alert_price_reached_boolean(ticker='AMZN', direction='decreased to',
    #                                   stock_price=stock_price, alert_price=3000))
    # stock_alert_email = Email(subject=r'New_TEST', receiver_email='viren.samani@hotmail.co.uk',
    #   body = 'BLANK', sender_email = "pythontestvs@gmail.com")

    # print(stock_alert_email.sender_email)
    # stock_alert_email.send_email()
    # stock_alert_email.send_email()

    alerts_list = [Alert(ticker='AMZN', alert_price=3000,
                         direction='decreased to'), Alert(ticker='AAPL', alert_price=150,
                                                          direction='decreased to')]

    run_alerts(alerts_list)
