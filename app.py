# crypto_logic.py
import ccxt
import pandas as pd
import numpy as np
import tulipy as ti
import feather
import os
import datetime
from os import path
from loguru import logger
from tinydb import TinyDB, Query

# --- TinyDB for local storage ---
db = TinyDB('db.json')
User = Query()

# --- Exchange setup ---
exch = getattr(ccxt, 'binance')()  # instantiate
exch.load_markets()  # preload all symbols

# --- Symbol lists ---
ls, ls1 = [], []
for symbol in exch.symbols:
    ls.append(symbol.split('/')[0])
    ls1.append(symbol.split('/')[1])
ls = list(set(ls))
ls1 = list(set(ls1))

# --- OHLCV storage ---
ohlcv_data1 = {}
ohlcv_data2 = {}
input_coin_pair = []

# --- Base path for feather files ---
base_path = "/Users/tharifansari/desktop/web-mini/feather_file"

# =========================
# Financial/Technical Data
# =========================
def calculate_financial_technical_data(comparision_type, comparision_value):
    """
    Example:
    data = calculate_financial_technical_data('sma', 'close')
    """
    logger.debug(comparision_value)
    data_list = []

    for i in ohlcv_data2.keys():
        data_list.append(ohlcv_data2[i].get(str(comparision_value), 0))

    logger.debug(data_list)

    if comparision_type == 'sma':
        data = ti.sma(np.asarray(data_list), period=10)
        return data
    elif comparision_type == 'stddev':
        data = ti.stddev(np.asarray(data_list), period=5).tolist()
        return data
    else:
        return None