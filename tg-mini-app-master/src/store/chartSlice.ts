import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  isOpen: false,
  chartTime: '1',
};

export const chartSlice = createSlice({
  name: 'referral',
  initialState,
  reducers: {
    setChartTime: (state, action) => {
      state.chartTime = action.payload;
    },
    openChart: (state) => {
      state.isOpen = true;
    },
    closeChart: (state) => {
      state.isOpen = false;
    },
  },
});

export const { setChartTime, openChart, closeChart } = chartSlice.actions;

export default chartSlice.reducer;
