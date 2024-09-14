export interface Candles {
  timestamp: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface Coin {
  name: string;
  network_slug: string;
  logo: string; // URL to the logo
  price: number;
  percent_change_24h: number;
  candles: Candles[];
  contract_address: string;
  shortName: string;
}
