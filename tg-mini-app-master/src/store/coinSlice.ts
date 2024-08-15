import { getCoinBySymbol } from '@/utils/api/coins'
import { Coin } from '@/utils/types/coin'
import { createAsyncThunk, createSlice, PayloadAction } from '@reduxjs/toolkit'

interface CoinState {
  coins: Coin[];
  loading: boolean;
  error: string | null;
}

const initialState: CoinState = {
  coins: [],
  loading: false,
  error: null,
};

export const getCoinBySymbolAndNetworkThunk = createAsyncThunk<Coin, { contract_address: string; network: string; logo: string }>(
  'coin/getCoinBySymbolAndNetwork',
  async ({ contract_address, network, logo }, { rejectWithValue }) => {
    try {
      const response = await getCoinBySymbol(contract_address, network);
      return { ...response, logo };
    } catch (error: any) {
      return rejectWithValue(error.response?.data || 'Failed to fetch coin data');
    }
  }
);

const coinSlice = createSlice({
  name: 'coin',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(getCoinBySymbolAndNetworkThunk.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(getCoinBySymbolAndNetworkThunk.fulfilled, (state, action: PayloadAction<Coin>) => {
        state.loading = false;
        const existingCoinIndex = state.coins.findIndex(
          (coin) => coin.contract_address === action.payload.contract_address && coin.network_slug === action.payload.network_slug
        );
        if (existingCoinIndex === -1) {
          state.coins.push(action.payload);
        }
      })
      .addCase(getCoinBySymbolAndNetworkThunk.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export default coinSlice.reducer;