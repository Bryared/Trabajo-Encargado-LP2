import pandas as pd
import matplotlib.pyplot as plt

data_bit = pd.read_csv('bitcoin/bitcoin_prices.csv')
data_dog = pd.read_csv('dogecoin/dogecoin_prices.csv')
data_eth = pd.read_csv('ethereum_COIN/ethereum_prices.csv')

# Combinar todos en un solo DataFrame
todo = pd.concat([data_bit , data_dog, data_eth], ignore_index=True)
print(todo)
