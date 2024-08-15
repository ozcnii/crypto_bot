export type League = {
	id: number
	name: string
	user_count: number
	clan_count: number
}

export type User = {
	id: number
	name: string
	balance: number
	avatar_url: string
}

export type Clan = {
	id: number
	name: string
	logo_url: string
	balance: number
}

export type LeagueType = {
	userLeague: League
	clanLeague: League
	status: string
	error: string
	users_list: User[]
	clans_list: Clan[]
}