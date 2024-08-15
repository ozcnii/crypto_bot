import axios from '@/utils/axios'
import { Coin } from '../types/coin'

export const getCoinBySymbol = async (contract_address: string, network: string): Promise<Coin> => {
	const response = await axios.post(`/coin/getCoinInfo?client_id=1`, {
		contract_address,
		network
	});
	return response.data
}