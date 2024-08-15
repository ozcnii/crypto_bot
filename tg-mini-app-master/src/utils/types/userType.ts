import { LoadingStatus } from '@/constants'

export type User = {
	user_id?: string
	league_id?: number
	token?: string
	blocked?: boolean
	balance?: number
	power?: number
	username?: string
	clan_id?: number
	id?: number
	role?: string
	created_at?: string
	p_n_l?: number | null
	avatar_url?: string
	is_premium?: boolean
	referral_code?: string
	referrer_id?: number
}

export type AllUsers = {
	user: User;
	status: LoadingStatus;
	error: LoadingStatus;
}

export type UserResponse = {
	user: AllUsers;
}