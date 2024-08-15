export type Referral = {
	id: number
	avatar_url: string
	username: string
	salary: number
}

export type ReferralState = {
	referrals: Referral[],
	error: string | null,
	status: 'pending' | 'fulfilled' | 'rejected' | 'none'
}