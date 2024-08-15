import axios from '@/utils/axios'

export const getUserLeagueRequest = async () => {
	const response = await axios.get(`/users/current_user/league?client_id=1`)
	return response
} 

export const getLeagueByIdRequest = async (id: number | undefined) => {
	const response = await axios.get(`/league/info?client_id=1&league_id=${id}`)
	return response
}

export const getLeagueByNameRequest = async (name: string | undefined) => {
	const response = await axios.get(`/league/info/${name}?client_id=1`)
	return response
}

export const getLeagueUsersRequest = async (name: string | undefined) => {
	const response = await axios.get(`/league/info/${name}/users?client_id=1`)
	return response
}

export const getLeagueClansRequest = async (name: string | undefined) => {
	const response = await axios.get(`/league/info/${name}/clans?client_id=1`)
	return response
}