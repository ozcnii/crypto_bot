
export type ClanListUsers = {
	name: string,
	balance: number,
	p_n_l: number,
	avatar_url: string
}

export type Clan = {
	id: number
	name: string
	link: string
	league_id: string
	balance: number
	users: number
	logo_url: string,
	owner_id: number,
	usersList: ClanListUsers[]
}

export type ClanList = {
	id: number
	name: string,
	league: string,
	logo_url: string
}

export type CreateClan = {
	id: number,
	message: string
}

export type ClanState = {
	clan: Clan,
	clans: ClanList[],
	clanById: Clan,
	createdClan: CreateClan,
	loading: boolean,
	status: string,
	error: string
}