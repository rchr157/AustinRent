import string
import re
import time
import os

# Data wrangling
import pandas as pd
import numpy as np
from scipy import stats

# Geocoding
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy.extra.rate_limiter import RateLimiter

# Machine Learning
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.model_selection import cross_val_score

geolocator = Nominatim(user_agent="edaTool")


def get_secret():
    mapbox_token = os.environ.get("MAPBOX_TOKEN")
    style_url = os.environ.get("STYLE_URL")
    return mapbox_token, style_url


def get_latlong(series):
    latitude = []
    longitude = []
    for s in series:
        time.sleep(1)
        try:
            a = geolocator.geocode(s, timeout=10)
        except GeocoderTimedOut:
            try:
                time.sleep(2)
                a = geolocator.geocode(s, timeout=1000)
            except GeocoderTimedOut:
                a = ""
        if a:
            latitude.append(a.latitude)
            longitude.append(a.longitude)
        else:
            latitude.append(np.nan)
            longitude.append(np.nan)

    loc_df = pd.DataFrame({"Address": series, "latitude": latitude, "longitude": longitude})

    return loc_df


def ml_alg(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42, shuffle=True)

    # Train the machine learning algorithm
    clf = LinearRegression()
    clf.fit(X_train, y_train)



    return clf


def format_column(series, col):
    col = col.lower()

    if col == "date":
        # Handle Date Column
        series = pd.to_datetime(series)
        series = series.dt.strftime("%b %y")
        return series
    elif col == "beds":
        replace_str = ["bedroom", "br"]
        series = series.str.replace("Studio", "0")
    elif col == "baths":
        replace_str = ["bathroom", "bath"]
        series = series.str.replace('½', '.5').str.replace('¼', '.25')
    elif col == "rent":
        replace_str = "$"
        series = series.str.replace("CallforRent", "")
    elif col == "sqft":
        replace_str = ["sq ft", "sqft"]
    else:
        return series

    # Remove strings
    # Flow: compare lower string to list, remove strings from list, remove trailing "s", remove ","
    series = series.str.lower().str.replace('|'.join(replace_str), '').\
        str.replace("s", "").str.replace(",", "")

    # Handle Range by replacing with mean of range
    series.fillna(value="", inplace=True)
    sub = series[series.str.contains('-')]
    if not sub.empty:
        sub = sub.str.split('-')
        sub_index = sub.index
        sub = pd.Series([[int(ss) for ss in s] for s in sub], index=sub_index)
        # if second value for range is much greater, value is likely for more rooms
        for s in sub:
            if s[1] > s[0]*1.5:
                s[1] = s[0]*1.5
        sub = pd.Series([int(pd.to_numeric(s).mean()) for s in sub], index=sub_index)
        series.loc[sub_index] = sub

    series = pd.to_numeric(series, downcast='integer')

    return series


def fill_nan(df):
    df_nan = df.select_dtypes(include=[np.number]).copy()
    cols = df_nan.columns
    imputer = KNNImputer(missing_values=np.nan, n_neighbors=4, weights="distance")
    df_nan = imputer.fit_transform(df_nan)
    df[cols] = df_nan

    return df

