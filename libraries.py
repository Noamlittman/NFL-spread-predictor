# data
import pandas as pd
import numpy as np
# Web Scraping
import requests
import time
from bs4 import BeautifulSoup, ResultSet
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

# Machine Learning
from tensorflow.keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from sklearn.ensemble import RandomForestClassifier  # or RandomForestRegressor for regression problems
from sklearn.metrics import accuracy_score
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.regularizers import l2
from tensorflow.keras.optimizers import Adam
import tensorflow as tf
from tensorflow.keras.layers import Layer


# Visualization
import matplotlib.pyplot as plt