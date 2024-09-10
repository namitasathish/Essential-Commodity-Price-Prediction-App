import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import warnings

warnings.filterwarnings("ignore")

def forecast_price(df, commodity, state_ut, forecast_year):

    commodity_data = df[(df['Food Commodities'] == commodity) & (df['State/UT'] == state_ut)]

    if commodity_data.empty:
        raise ValueError(f"No data available for commodity: {commodity} in {state_ut}.")

 
    price_data = commodity_data.iloc[0, 2:].values 
    price_data = pd.to_numeric(price_data, errors='coerce') 


    if np.isnan(price_data).any():
       
        price_data = pd.Series(price_data).fillna(method='ffill').fillna(method='bfill').values

       
        if np.isnan(price_data).any():
            raise ValueError("The price data contains invalid or NaN values. Cannot proceed with forecasting.")

    model = ARIMA(price_data, order=(1, 1, 1))
    fitted_model = model.fit()

    forecast_steps = forecast_year - 2023
    if forecast_steps <= 0:
        raise ValueError("The forecast year must be in the future.")


    forecast_result = fitted_model.forecast(steps=forecast_steps)
    forecast_price = forecast_result[-1]  
    return forecast_price