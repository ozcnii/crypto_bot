import 'swiper/css'
import { FreeMode } from 'swiper/modules'
import { Swiper, SwiperSlide } from 'swiper/react'
import { BoosterSwiperCard } from './boosterSwiperCard'
import css from './boostersSwiper.module.css'

export const items = [
	{
		id: 1,
		img: '🪙',
		name: 'Range',
		cost: 100,
		lvl: 3
	},
	{
		id: 2,
		img: '⚖️',
		name: 'Leverage',
		cost: 100,
		lvl: 3
	},
	{
		id: 3,
		img: '⚡',
		name: 'Leverage',
		cost: 100,
		lvl: 3
	},
	{
		id: 4,
		img: '🤖',
		name: 'Leverage',
		cost: 100,
		lvl: 3
	},
]

export const BoostersSwiper = () => {
	return (
		<Swiper
			spaceBetween={12.5}
			slidesPerView={'auto'}
			direction='vertical'
			modules={[FreeMode]}
			className={css.swiper}
		>
			{items.map(item => (
				<SwiperSlide key={item.id} className={css.swiperSlide}>
					<BoosterSwiperCard item={item} />
				</SwiperSlide>
			))}
		</Swiper>
	)
}