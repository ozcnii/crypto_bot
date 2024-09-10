const addresses = {
  'EQARK5MKz_MK51U5AZjK3hxhLg1SmQG2Z-4Pb7Zapi_xwmrN': 'OKX:NOTUSDT',
  'EQA-X_yo3fzzbDbJ_0bzFWKqtRuZFIRa1sJsveZJ1YpViO3r': 'OKX:TONUSDT',
  '0xc7bbec68d12a0d1830360f8ec58fa599ba1b0e9b': 'OKX:ETHUSDT',
  EQAyOzOJYwzrXNdhQkskblthpYmm6iL_XeXEcaDuQmV0vxQQ: 'OKX:DOGSUSDT',
  '0x6aa9c4eda3bf8ac038ad5c243133d6d25aa9cc73': 'OKX:BTCUSDT',
  DSUvc5qf5LJHHV5e2tD184ixotSnCnwj7i4jJa4Xsrmt: 'OKX:SOLUSDT',
};

export const useGetSymbolPair = ({
  contract,
}: {
  contract: string;
}): string => {
  return addresses[contract];
};
