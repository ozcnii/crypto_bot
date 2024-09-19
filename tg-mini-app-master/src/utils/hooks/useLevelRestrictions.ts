const LEVEL_RESTRICTIONS = {
  1: { maxAmountPercentage: 0.1, maxLeverage: 2 },
  2: { maxAmountPercentage: 0.15, maxLeverage: 3 },
  3: { maxAmountPercentage: 0.25, maxLeverage: 5 },
  4: { maxAmountPercentage: 0.35, maxLeverage: 7 },
  5: { maxAmountPercentage: 0.5, maxLeverage: 10 },
  6: { maxAmountPercentage: 0.65, maxLeverage: 15 },
  7: { maxAmountPercentage: 0.75, maxLeverage: 25 },
  8: { maxAmountPercentage: 0.85, maxLeverage: 50 },
  9: { maxAmountPercentage: 0.95, maxLeverage: 100 },
  10: { maxAmountPercentage: 1, maxLeverage: 125 },
};

export const useLevelRestrictions = ({
  balance,
  levels,
  freeBoosters,
}: {
  balance: number;
  levels: {
    range_lvl: number;
    leverage_lvl: number;
  };
  freeBoosters: {
    x_leverage: {
      uses: number;
      active: boolean;
    };
    turbo_range: {
      uses: number;
      active: boolean;
    };
  };
}) => {
  const { maxAmountPercentage } = LEVEL_RESTRICTIONS[levels.range_lvl];
  const { maxLeverage } = LEVEL_RESTRICTIONS[levels.leverage_lvl];
  return {
    maxAmount:
      freeBoosters.turbo_range.uses !== 0 && freeBoosters.turbo_range.active
        ? balance * maxAmountPercentage * 2
        : balance * maxAmountPercentage,
    maxLeverage:
      freeBoosters.x_leverage.uses !== 0 && freeBoosters.x_leverage.active
        ? maxLeverage * 2
        : maxLeverage,
  };
};
