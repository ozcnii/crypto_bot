import { Coin } from './coin'

export interface Boost {
	id: number;
	lvl: number;
	cost: number;
	name: string;
	img: string;
}

export type Modal = {
	isOpen: boolean;
	modalType: string;
	confirmBoostModal: {
		boost: Boost;
		isConfirmed: boolean;
	};
	cryptoTradeModal: {
		isOpen: boolean;
		crypto: Coin;
		isClosing: boolean;
	}
}