import pandas as pd

def generate_signal(df: pd.DataFrame) -> pd.DataFrame:
  """
  Generate trading signals based on SMA and Volatility

  Returns
  -------
  str : BUY / SELL / HOLD
  """

  if row["sma_5"] > row["sma_10"] and row["vol_5"] > row["vol_10"]:
      return "BUY"
  elif row["sma_5"] < row["sma_10"] and row["vol_5"] > row["vol_10"]:
    return "SELL"
  else:
    return "HOLD"
