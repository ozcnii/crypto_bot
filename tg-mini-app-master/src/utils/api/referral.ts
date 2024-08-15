import axios from '@/utils/axios'

export const getUserReferralsRequest = async () => {
	return await axios.get(`/users/current_user/fellows?client_id=1`)
}