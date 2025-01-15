import { LoadingStatus } from '@/constants';
import { getUserByJWTRequest } from '@/utils/api/user';
import { AllUsers, User } from '@/utils/types/userType';
import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';

export const getByJWTUser = createAsyncThunk(
  'user/getByJWTUser',
  async (_, { rejectWithValue }) => {
    try {
      const response = await getUserByJWTRequest();
      if (response.status === 200) {
        return response.data;
      }
      return rejectWithValue(response.data);
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  },
);

const initialState: AllUsers = {
  // TODO mocked
  user: {
    balance: 1000.0,
    balance_features: 1000.0,
    boosters: [0, 0, 0, 0, 0],
    chat_id: 528254266,
    clan: null,
    historycheck: null,
    league: 'bronze',
    pnl: null,
    referals: null,
    tasks: null,
    trades: null,
    username: 'qqnvos',
  } as User,
  status: LoadingStatus.none,
  error: LoadingStatus.none,
};

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    getUserByJWT(_, action) {
      return action.payload;
    },
  },
  extraReducers: (builder) => {
    builder.addCase(getByJWTUser.pending, (state) => {
      state.status = LoadingStatus.pending;
      state.error = LoadingStatus.none;
    });
    builder.addCase(getByJWTUser.fulfilled, (state, action) => {
      state.user = action.payload;
      state.status = LoadingStatus.fulfilled;
      state.error = LoadingStatus.none;
    });
    builder.addCase(getByJWTUser.rejected, (state) => {
      state.status = LoadingStatus.rejected;
      state.error = LoadingStatus.none;
    });
  },
});

export const { getUserByJWT } = userSlice.actions;

export default userSlice.reducer;
