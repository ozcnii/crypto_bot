import MainCoin from '@/assets/coins/coin'
import { openConfirmBoostModal } from '@/store/modalsSlice'
import { FC } from 'react'
import { useDispatch } from 'react-redux'
import css from './boosterSwiperCard.module.css'

interface BoosterSwiperCardProps {
	item: {
		id: number,
		name: string,
		img: string,
		cost: number,
		lvl: number
	}
}

export const BoosterSwiperCard: FC<BoosterSwiperCardProps> = ({ item }: BoosterSwiperCardProps) => {
	const dispatch = useDispatch()
	
	const handleOnClick = () => {
		dispatch(openConfirmBoostModal({
			isConfirmed: false,
			boost: item
		}))
	}

	return (
		<div className={css.boosterCard} onClick={handleOnClick}>
			<div className={css.boosterInfo}>
				<div className={css.boosterImg}>
					<span>{item.img}</span>
				</div>
				<div className={css.boosterName}>
					<h1>{item.name}</h1>
					<p className={css.boosterCost}>
					<MainCoin width={13} height={13} />
						<span>{item.cost}</span>  | {item.lvl} lvl
					</p>
				</div>
			</div>
			<button type="button" className={css.confirmButton}>
			<img src='img/boosterVector.svg' alt='booster' />
			</button>
		</div>
	)
}