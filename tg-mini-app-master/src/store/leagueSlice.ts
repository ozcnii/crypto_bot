import { getLeagueByIdRequest, getLeagueByNameRequest, getLeagueClansRequest, getLeagueUsersRequest, getUserLeagueRequest } from '@/utils/api/league'
import { Clan, League, LeagueType, User } from '@/utils/types/league'
import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'

export const getUserLeague = createAsyncThunk('league/getUserLeague', async (_, { rejectWithValue }) => {
	try {
		const response = await getUserLeagueRequest();
		if (response.status === 200) {
			return response.data
		}
		return rejectWithValue(response.data)
	} catch(error) {
		return rejectWithValue(error)
	}
})

export const getUserLeagueById = createAsyncThunk('league/getUserLeagueById', async (id: number | undefined, { rejectWithValue }) => {
	try {
		const response = await getLeagueByIdRequest(id)
		if (response.status === 200) {
			return response.data
		}
		return rejectWithValue(response.data)
	} catch(error) {
		return rejectWithValue(error)
	}
})

export const getClanLeagueById = createAsyncThunk('league/getClanLeagueById', async (id: number | undefined, { rejectWithValue }) => {
	try {
		const response = await getLeagueByIdRequest(id)
		if (response.status === 200) {
			return response.data
		}
		return rejectWithValue(response.data)
	} catch(error) {
		return rejectWithValue(error)
	}
})

export const getLeagueByName = createAsyncThunk('league/getLeagueByName', async (name: string | undefined, { rejectWithValue }) => {
	try {
		const response = await getLeagueByNameRequest(name)
		if (response.status === 200) {
			return response.data
		}
		return rejectWithValue(response.data)
	} catch(error) {
		return rejectWithValue(error)
	}
})

export const getLeagueUsers = createAsyncThunk('league/getLeagueUsers', async (name: string | undefined, { rejectWithValue }) => {
	try {
		const response = await getLeagueUsersRequest(name);
		if (response.status === 200) {
			return response.data
		}
		return rejectWithValue(response.data)
	} catch(error) {
		return rejectWithValue(error)
	}
})

export const getLeagueClans = createAsyncThunk('league/getLeagueClans', async (name: string | undefined, { rejectWithValue }) => {
	try {
		const response = await getLeagueClansRequest(name);
		if (response.status === 200) {
			return response.data
		}
		return rejectWithValue(response.data)
	} catch(error) {
		return rejectWithValue(error)
	}
})

const initialState: LeagueType = {
	userLeague: {} as League,
	clanLeague: {} as League,
	users_list: [] as User[],
	clans_list: [] as Clan[],
	status: 'idle',
	error: ''
}

export const leagueSlice = createSlice({
	name: 'league',
	initialState,
	reducers: {},
	extraReducers: (builder) => {
		builder
			.addCase(getUserLeague.pending, (state) => {
				state.status = 'loading'
			})
			.addCase(getUserLeague.fulfilled, (state, action) => {
				state.userLeague = action.payload
				state.status = 'succeeded'
			})
			.addCase(getUserLeague.rejected, (state, action) => {
				state.status = 'failed'
				state.error = action.error
			})
			.addCase(getUserLeagueById.pending, (state) => {
				state.status = 'loading'
			})
			.addCase(getUserLeagueById.fulfilled, (state, action) => {
				state.userLeague = action.payload
				state.status = 'succeeded'
			})
			.addCase(getUserLeagueById.rejected, (state, action) => {
				state.status = 'failed'
				state.error = action.error
			})
			.addCase(getLeagueByName.pending, (state) => {
				state.status = 'loading'
			})
			.addCase(getLeagueByName.fulfilled, (state, action) => {
				state.userLeague = action.payload
				state.status = 'succeeded'
			})
			.addCase(getLeagueByName.rejected, (state, action) => {
				state.status = 'failed'
				state.error = action.error
			})
			.addCase(getLeagueUsers.pending, (state) => {
				state.status = 'loading'
			})
			.addCase(getLeagueUsers.fulfilled, (state, action) => {
				state.users_list = action.payload
				state.status = 'succeeded'
			})
			.addCase(getLeagueUsers.rejected, (state, action) => {
				state.status = 'failed'
				state.error = action.error
			})
			.addCase(getLeagueClans.pending, (state) => {
				state.status = 'loading'
			})
			.addCase(getLeagueClans.fulfilled, (state, action) => {
				state.clans_list = action.payload
				state.status = 'succeeded'
			})
			.addCase(getLeagueClans.rejected, (state, action) => {
				state.status = 'failed'
				state.error = action.error
			})
			.addCase(getClanLeagueById.pending, (state) => {
				state.status = 'loading'
			})
			.addCase(getClanLeagueById.fulfilled, (state, action) => {
				state.clanLeague = action.payload
				state.status = 'succeeded'
			})
			.addCase(getClanLeagueById.rejected, (state, action) => {
				state.status = 'failed'
				state.error = action.error
			})
	}
})

export default leagueSlice.reducer