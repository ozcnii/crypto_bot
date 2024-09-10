import requests
from Database.models import Order
from good_guard import COINMARKETCAP_API_KEY, coin_to_usdt_rate

addresses = {
  'EQARK5MKz_MK51U5AZjK3hxhLg1SmQG2Z-4Pb7Zapi_xwmrN': 'ton',
  'EQA-X_yo3fzzbDbJ_0bzFWKqtRuZFIRa1sJsveZJ1YpViO3r': 'ton',
  '0xc7bbec68d12a0d1830360f8ec58fa599ba1b0e9b': 'ethereum',
  'EQAyOzOJYwzrXNdhQkskblthpYmm6iL_XeXEcaDuQmV0vxQQ': 'ton',
  '0x6aa9c4eda3bf8ac038ad5c243133d6d25aa9cc73': 'bsc',
  'DSUvc5qf5LJHHV5e2tD184ixotSnCnwj7i4jJa4Xsrmt': 'solana'
}

def get_current_rate(contract_address: str) -> float:
	network = addresses.get(contract_address)
	if network is None:
		print("Network not found")
		return ValueError("Network not found")
  
	url = f"https://pro-api.coinmarketcap.com/v4/dex/pairs/quotes/latest?network_slug={network}&contract_address={contract_address}"
	headers = {
		'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY
	}
 
	response = requests.get(url, headers=headers)
	data = response.json()
	
	if contract_address == '0xa43fe16908251ee70ef74718545e4fe6c5ccec9f' or 'DSUvc5qf5LJHHV5e2tD184ixotSnCnwj7i4jJa4Xsrmt':
		price_by_quote_asset = data['data'][0]['quote'][0]['price']
	else:
		price_by_quote_asset = data['data'][0]['quote'][0]['price_by_quote_asset']
    
	return price_by_quote_asset

def calculate_pnl(order: Order, exit_rate: float):
  coin_in_usdt = order.amount * coin_to_usdt_rate
  pnl_in_usdt = (exit_rate - order.entry_rate) if order.direction == "long" else (order.entry_rate - exit_rate) * coin_in_usdt * order.leverage / order.entry_rate
  pnl_in_coin = pnl_in_usdt / coin_to_usdt_rate
  
  if pnl_in_coin < -order.amount:
    pnl_in_coin = -order.amount
  
  return pnl_in_coin