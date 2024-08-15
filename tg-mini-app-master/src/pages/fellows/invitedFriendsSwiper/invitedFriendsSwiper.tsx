import { FC } from 'react'
import { FreeMode } from 'swiper/modules'
import { Swiper } from 'swiper/react'
import css from './invitedFriendsSwiper.module.css'

interface InvitedFriendsSwiperProps {
	friends: { id: number, username: string, avatar_url: string, salary: number }[]
}

export const InvitedFriendsSwiper: FC<InvitedFriendsSwiperProps> = ({ friends }: InvitedFriendsSwiperProps) => {
	return (
		<Swiper
			slidesPerView={'auto'}
			spaceBetween={10}
			className={css.swiper}
			direction='vertical'
			modules={[FreeMode]}
		>
			{friends?.map(item => (
				<div key={item.id} className={css.item}>
					<div className={css.avatarWrapper}>
						<div className={css.icon}>
							<img src={item.avatar_url} alt={item.username} />
						</div>
						<h2>{item.username}</h2>
					</div>
					<div className={css.cost}>
						{item.salary}
						<img src='img/vector.svg' alt='vector' />
					</div>
				</div>
			))}
		</Swiper>
	)
}