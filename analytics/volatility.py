import pandas as pd

def volatility(series: pd.Series, window: int) -> pd.Series:
  """
  Hitung Volatilitas Harga

  Parameters
  ----------
  series : pd.Series
    Data harga (price_usd)
  window : int
    Jumlah window (misal 5, 10)

  Returns
  -------
  pd.Series
    Standard deviation
  """
  return series.rolling(window=window).std()