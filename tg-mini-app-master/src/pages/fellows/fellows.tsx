import MainCoin from '@/assets/coins/coin'
import NotFound from '@/assets/notFound'
import { RootState } from '@/store'
import { getUserReferrals } from '@/store/referralSlice'
import { getByJWTUser } from '@/store/userSlice'
import { ThunkDispatch } from '@reduxjs/toolkit'
import { initUtils } from '@telegram-apps/sdk'
import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import css from './fellows.module.css'
import { InvitedFriendsSwiper } from './invitedFriendsSwiper/invitedFriendsSwiper'

export const items = [
	{
		id: 1,
		avatar: '👨🏻',
		nickname: 'Nickname #1',
		cost: 100
	},
	{
		id: 2,
		avatar: '👨🏻',
		nickname: 'Nickname #2',
		cost: 100
	},
	{
		id: 3,
		avatar: '👨🏻',
		nickname: 'Nickname #3',
		cost: 100
	}
]

export const Fellows = () => {
	const dispatch = useDispatch<ThunkDispatch<RootState, null, any>>()
	const utils = initUtils()
	const { user } = useSelector((state: RootState) => state.user)
	const { referrals } = useSelector((state: RootState) => state.referral)

	useEffect(() => {
		const fetchUser = async () => {
			await dispatch(getByJWTUser())
		}
		const fetchFellows = async () => {
			await dispatch(getUserReferrals())
		}

		fetchFellows()
		fetchUser()
	}, [dispatch])

	const hanldleOnShareClick = () => {
		utils.shareURL(`https://t.me/aenolabsbot?start=${user?.referral_code}`, 'Hello from Aeno Labs! 👋! Go through my link!')
	}

	return (
		<div className={css.main}>
			<div className={css.fellowsHeader}>
				<img src="img/fellows.png" alt="fellows" />
				<h1>Fellows</h1>
				<p>Lorem ipsum dolor sit amet consectetur. Elementum lorem massa consectetur id scelerisque in egestas amet rhoncus.</p>
			</div>
			<div className={css.fellowsLadder}>
				<div className={css.top}>
					<div className={css.topItem}>
						<span>
							<p>{user.balance}</p>
							<MainCoin width={14} height={14} />
						</span>
						<p>TOP #963</p>
					</div>
				</div>
				<div className={css.ladder}>
					<h1>TOP 300 LADDERS</h1>
					<img src="img/boosterVector.svg" alt="ladder" />
				</div>
			</div>
			<div className={css.inviteFellows}>
				<h1>Invite Fellows and get Rewards</h1>
				<div className={css.inviteContainer}>
					<div className={css.defaultFriend}>
						<div className={css.iconWrapper}>
							<div className={css.icon}>
								<span>👤</span>
							</div>
							<p>Invite friend</p>
						</div>
						<div className={css.cost}>
							100
							<MainCoin width={14} height={14} />
						</div>
					</div>
					<div className={css.premiumFriend}>
						<div className={css.iconWrapper}>
							<div className={css.icon}>
								<span>💎</span>
							</div>
							<p>Friend premium-user</p>
						</div>
						<div className={css.cost}>
							1000
							<MainCoin width={14} height={14} />
						</div>
					</div>
				</div>
			</div>
			<div className={css.fellowsListWrapper}>
				<h1>Invited Friends</h1>
				{referrals?.length > 0 ? <InvitedFriendsSwiper friends={referrals} /> : <div className={css.noClans}>
						<NotFound />
						<p>No fellows yet</p>
					</div>}
			</div>
			<button type='button' className={css.floatingButton} onClick={hanldleOnShareClick}>Invite a fellow</button>
		</div>
	)
}