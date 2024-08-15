import { Coin } from '@/utils/types/coin'
import { Boost, Modal } from '@/utils/types/modals'
import { createSlice } from '@reduxjs/toolkit'

const initialState: Modal = {
	isOpen: false,
	modalType: '',
	confirmBoostModal: {
		boost: {} as Boost,
		isConfirmed: false
	},
	cryptoTradeModal: {
		isOpen: false,
		crypto: {} as Coin,
		isClosing: false
	}
}

export const modalsSlice = createSlice({
	name: 'modals',
	initialState,
	reducers: {
		closeModal: (state) => {
			state.modalType = ''
			state.isOpen = false
			state.confirmBoostModal = {
				boost: {} as Boost,
				isConfirmed: false
			},
			state.cryptoTradeModal = {
				isOpen: false,
				crypto: {} as Coin,
				isClosing: false
			}
		},
		openConfirmBoostModal: (state, action) => {
			state.modalType = 'CONFIRMBOOST'
			state.isOpen = true
			state.confirmBoostModal = action.payload
		},
		confirmBoost: (state, action) => {
			state.confirmBoostModal.isConfirmed = action.payload
		},
		openCryptoTradeModal: (state, action) => {
			state.modalType = 'TRADECRYPTO'
			state.isOpen = true
			state.cryptoTradeModal.isOpen = true
			state.cryptoTradeModal.crypto = action.payload
		},
		closeCryptoTradeModal: (state) => {
			state.cryptoTradeModal.isClosing = true
		},
		openCreateClanModal: (state) => {
			state.modalType = 'CREATECLAN'
			state.isOpen = true
		}
	}
})

export const {
	closeModal,
	openConfirmBoostModal,
	confirmBoost,
	openCryptoTradeModal,
	closeCryptoTradeModal,
	openCreateClanModal
} = modalsSlice.actions

export default modalsSlice.reducer