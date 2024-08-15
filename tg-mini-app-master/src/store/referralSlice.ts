import { getUserReferralsRequest } from '@/utils/api/referral'
import { ReferralState } from '@/utils/types/referral'
import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'

export const getUserReferrals = createAsyncThunk('referral/getUserReferrals', async (_, { rejectWithValue }) => {
	try {
		const response = await getUserReferralsRequest();
		if (response.status === 200) {
			return response.data
		}
		return rejectWithValue(response.data)
	} catch(error) {
		return rejectWithValue(error)
	}
})

const initialState: ReferralState = {
	referrals: [],
	error: null,
	status: 'none',
}

export const referralSlice = createSlice({
	name: 'referral',
	initialState,
	reducers: {},
	extraReducers: (builder) => {
		builder
			.addCase(getUserReferrals.pending, (state) => {
				state.status = 'pending'
			})
			.addCase(getUserReferrals.fulfilled, (state, action) => {
				state.status = 'fulfilled'
				state.referrals = action.payload
			})
			.addCase(getUserReferrals.rejected, (state, action) => {
				state.status = 'rejected'
				state.error = action.payload
			})
	},
})

export default referralSlice.reducer