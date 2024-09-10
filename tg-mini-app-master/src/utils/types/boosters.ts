export type Booster = {
  lvl: number;
  nextPrice: number;
};

export type FreeBooster = {
  turbo_range: number;
  x_leverage: number;
};

export enum BoosterType {
  Range = 'range',
  Leverage = 'leverage',
  Trades = 'trades',
}

export type Boosters = {
  [key: string]: Booster | FreeBooster;
};
