import pandas as pd

def simple_moving_average(series: pd.Series, window: int) -> pd.Series:
  """
  Hitung Simple Moving Average (SMA)

  Parameters
  ----------
  series : pd.Series
    Data harga (price_usd)
  window : int
    Periode moving average (5, 10)

  Returns
  -------
  pd.Series
    Series yang berisi nilai SMA
  """
  return series.rolling(window=window).mean()