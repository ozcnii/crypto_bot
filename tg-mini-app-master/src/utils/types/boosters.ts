export type Booster = {
  lvl: number;
  nextPrice: number;
};

export type FreeBooster = {
  uses: number;
  active: boolean;
};

export type FreeBoosters = {
  turbo_range: FreeBooster;
  x_leverage: FreeBooster;
};

export enum BoosterType {
  Range = 'range',
  Leverage = 'leverage',
  Trades = 'trades',
}

export type Boosters = {
  [key: string]: Booster | FreeBoosters;
};
