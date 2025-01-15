import {
  createClanRequest,
  deleteUserClanRequest,
  getClanByIdRequest,
  getClanListRequest,
  getUserClanRequest,
  joinUserClanRequest,
  leaveUserClanRequest,
} from '@/utils/api/clan';
import { Clan, ClanList, ClanState, CreateClan } from '@/utils/types/clan';
import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { closeModal } from './modalsSlice';
import { showNotification } from './notificationSlice';

export const getUserClan = createAsyncThunk(
  'clan/getUserClan',
  async (clanId: number | undefined, { rejectWithValue }) => {
    try {
      const clan = await getUserClanRequest(clanId);
      if (clan === null) {
        return rejectWithValue({ status: 404, message: 'Clan not found' });
      }
      return clan;
    } catch (error: any) {
      return rejectWithValue({
        status: error.response?.status,
        message: error.message,
      });
    }
  },
);

export const deleteUserClan = createAsyncThunk(
  'clan/deleteUserClan',
  async (link: string, { rejectWithValue, dispatch }) => {
    try {
      const clan = await deleteUserClanRequest(link);
      if (clan.status === 200) {
        dispatch(
          showNotification({
            message: "You've deleted clan!",
            type: 'success',
            logo: 'img/bear.png',
          }),
        );
        return clan;
      } else {
        dispatch(
          showNotification({
            message: 'Something is wrong..',
            type: 'error',
            logo: 'img/brokenhouse.png',
          }),
        );
        return rejectWithValue({ status: clan.status, message: clan.message });
      }
    } catch (error: any) {
      dispatch(
        showNotification({
          message: 'Something is wrong..',
          type: 'error',
          logo: 'img/brokenhouse.png',
        }),
      );
      return rejectWithValue({
        status: error.response?.status,
        message: error.message,
      });
    }
  },
);

export const joinUserClan = createAsyncThunk(
  'clan/joinUserClan',
  async (id: number, { rejectWithValue, dispatch }) => {
    try {
      const clan = await joinUserClanRequest(id);
      if (clan.status === 200) {
        dispatch(
          showNotification({
            message: "You've joined clan!",
            type: 'success',
            logo: 'img/house.png',
          }),
        );
        return clan;
      } else {
        dispatch(
          showNotification({
            message: 'Something is wrong..',
            type: 'error',
            logo: 'img/brokenhouse.png',
          }),
        );
        return rejectWithValue({ status: clan.status, message: clan.message });
      }
    } catch (error: any) {
      dispatch(
        showNotification({
          message: 'Something is wrong..',
          type: 'error',
          logo: 'img/brokenhouse.png',
        }),
      );
      return rejectWithValue({
        status: error.response?.status,
        message: error.message,
      });
    }
  },
);

export const leaveUserClan = createAsyncThunk(
  'clan/leaveUserClan',
  async (_, { rejectWithValue, dispatch }) => {
    try {
      const clan = await leaveUserClanRequest();
      if (clan.status === 200) {
        dispatch(
          showNotification({
            message: "You've left clan!",
            type: 'success',
            logo: 'img/bear.png',
          }),
        );
        return clan;
      } else {
        dispatch(
          showNotification({
            message: 'Something is wrong..',
            type: 'error',
            logo: 'img/brokenhouse.png',
          }),
        );
        return rejectWithValue({ status: clan.status, message: clan.message });
      }
    } catch (error: any) {
      dispatch(
        showNotification({
          message: 'Something is wrong..',
          type: 'error',
          logo: 'img/brokenhouse.png',
        }),
      );
      return rejectWithValue({
        status: error.response?.status,
        message: error.message,
      });
    }
  },
);

export const getClanList = createAsyncThunk(
  'clan/getClanList',
  async (_, { rejectWithValue }) => {
    try {
      const clans = await getClanListRequest();
      return clans;
    } catch (error: any) {
      return rejectWithValue({
        status: error.response?.status,
        message: error.message,
      });
    }
  },
);

export const getClanById = createAsyncThunk(
  'clan/getClanById',
  async (id: string | undefined, { rejectWithValue }) => {
    try {
      const clan = await getClanByIdRequest(id);
      return clan;
    } catch (error: any) {
      return rejectWithValue({
        status: error.response?.status,
        message: error.message,
      });
    }
  },
);

export const createClan = createAsyncThunk(
  'clan/createClan',
  async (link: string, { rejectWithValue, dispatch }) => {
    try {
      const clan = await createClanRequest(link);
      if (clan.status !== 200) {
        dispatch(
          showNotification({
            message: clan.data.message,
            type: 'error',
            logo: 'img/brokenhouse.png',
          }),
        );
        return rejectWithValue({
          status: clan.status,
          message: clan.data.message,
        });
      }
      dispatch(
        showNotification({
          message: 'Clan created',
          type: 'success',
          logo: 'img/house.png',
        }),
      );
      dispatch(closeModal());
      return clan.data;
    } catch (error: any) {
      dispatch(
        showNotification({
          message: 'Something is wrong..',
          type: 'error',
          logo: 'img/brokenhouse.png',
        }),
      );
      return rejectWithValue({
        status: error.response?.status,
        message: error.message,
      });
    }
  },
);

const initialState: ClanState = {
  clan: {} as Clan,
  clans: [] as ClanList[],
  clanById: {} as Clan,
  createdClan: {} as CreateClan,
  loading: false,
  status: '',
  error: 'none',
};

const clanSlice = createSlice({
  name: 'clan',
  initialState,
  reducers: {
    getClanUser: (_, action) => {
      return action.payload;
    },
    clearStatus: (state) => {
      state.status = '';
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(getUserClan.pending, (state) => {
        state.loading = true;
        state.status = '';
        state.error = 'none';
      })
      .addCase(getUserClan.fulfilled, (state, action) => {
        state.status = '';
        state.loading = false;
        state.clan = action.payload;
        state.error = 'none';
      })
      .addCase(getUserClan.rejected, (state, action) => {
        state.status = `${action.payload.status}`;
        state.loading = false;
        if (action.payload.status === 404) {
          state.error = 'Clan not found';
        } else {
          state.error = action.payload.message;
        }
      })
      .addCase(deleteUserClan.pending, (state) => {
        state.status = '';
        state.error = 'none';
      })
      .addCase(deleteUserClan.fulfilled, (state, action) => {
        state.status = "You've deleted clan!";
        state.clan = {} as Clan;
        state.error = 'none';
      })
      .addCase(deleteUserClan.rejected, (state, action) => {
        state.status = 'Something is wrong..';
        state.error = action.payload.message;
      })
      .addCase(joinUserClan.pending, (state) => {
        state.status = '';
        state.error = 'none';
      })
      .addCase(joinUserClan.fulfilled, (state, action) => {
        state.status = "You've joined clan!";
        state.error = 'none';
      })
      .addCase(joinUserClan.rejected, (state, action) => {
        state.status = 'Something is wrong..';
        state.error = action.payload.message;
      })
      .addCase(leaveUserClan.pending, (state) => {
        state.status = '';
        state.error = 'none';
      })
      .addCase(leaveUserClan.fulfilled, (state, action) => {
        state.status = "You've left clan!";
        state.error = 'none';
        state.clan = {} as Clan;
      })
      .addCase(leaveUserClan.rejected, (state, action) => {
        state.status = 'Something is wrong..';
        state.error = action.payload.message;
      })
      .addCase(getClanList.pending, (state) => {
        state.loading = true;
        state.status = '';
        state.error = 'none';
      })
      .addCase(getClanList.fulfilled, (state, action) => {
        state.status = '200';
        state.clans = action.payload;
        state.loading = false;
        state.error = 'none';
      })
      .addCase(getClanList.rejected, (state, action) => {
        state.status = `${action.payload.status}`;
        state.loading = false;
        state.error = action.payload.message;
      })
      .addCase(getClanById.pending, (state) => {
        state.status = '';
        state.error = 'none';
      })
      .addCase(getClanById.fulfilled, (state, action) => {
        state.status = '200';
        state.clanById = action.payload;
        state.error = 'none';
      })
      .addCase(getClanById.rejected, (state, action) => {
        state.status = `${action.payload.status}`;
        state.error = action.payload.message;
      })
      .addCase(createClan.pending, (state) => {
        state.status = '';
        state.error = 'none';
      })
      .addCase(createClan.fulfilled, (state, action) => {
        state.status = `${action.payload.message}`;
        state.createdClan = action.payload;
        state.error = 'none';
      })
      .addCase(createClan.rejected, (state, action) => {
        state.status = 'Бот не найден в указанном канале или группе';
        state.error = action.payload.message;
      });
  },
});

export const { getClanUser, clearStatus } = clanSlice.actions;

export default clanSlice.reducer;
