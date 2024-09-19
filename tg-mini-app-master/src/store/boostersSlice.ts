import axios from '@/utils/axios';
import { Boosters } from '@/utils/types/boosters';
import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';

export const getUserBoosters = createAsyncThunk(
  'boosters/getUserBoosters',
  async (_, { rejectWithValue }) => {
    try {
      const response = await axios.get(`/boosters?client_id=1`);
      if (response.status === 200) {
        return response.data;
      }
      return rejectWithValue(response.data);
    } catch (error) {
      return rejectWithValue(error);
    }
  },
);

export const upgradeUserBoosterByType = createAsyncThunk(
  'boosters/upgradeUserBoosterByType',
  async (
    { booster_type }: { booster_type: string },
    { rejectWithValue, dispatch },
  ) => {
    try {
      const response = await axios.post(
        `/boosters/upgrade?client_id=1`,
        booster_type,
      );
      if (response.status === 200) {
        return await dispatch(getUserBoosters());
      }
      return rejectWithValue(response.data);
    } catch (error) {
      return rejectWithValue(error);
    }
  },
);

export const useFreeBoosterByType = createAsyncThunk(
  'boosters/useFreeBoosterByType',
  async (
    { booster_type }: { booster_type: string },
    { rejectWithValue, dispatch },
  ) => {
    try {
      const response = await axios.post(
        `/boosters/use/free?client_id=1`,
        booster_type,
      );
      if (response.status === 200) {
        return await dispatch(getUserBoosters());
      }
      return rejectWithValue(response.data);
    } catch (error) {
      return rejectWithValue(error);
    }
  },
);

const initialState = {
  boosters: {} as Boosters,
  loading: false,
  error: null,
};

export const boostersSlice = createSlice({
  name: 'boosters',
  initialState,
  reducers: {},
  extraReducers(builder) {
    builder
      .addCase(getUserBoosters.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(getUserBoosters.fulfilled, (state, action) => {
        state.loading = false;
        state.error = null;
        state.boosters = action.payload;
      })
      .addCase(getUserBoosters.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(upgradeUserBoosterByType.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(upgradeUserBoosterByType.fulfilled, (state) => {
        state.loading = false;
        state.error = null;
      })
      .addCase(upgradeUserBoosterByType.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(useFreeBoosterByType.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(useFreeBoosterByType.fulfilled, (state) => {
        state.loading = false;
        state.error = null;
      })
      .addCase(useFreeBoosterByType.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export default boostersSlice.reducer;
