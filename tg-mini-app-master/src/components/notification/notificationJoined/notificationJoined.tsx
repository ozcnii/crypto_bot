import { FC } from 'react'
import css from './notificationJoined.module.css'

interface NotificationJoinedProps {
	status: string
}

export const NotificationJoined: FC<NotificationJoinedProps> = ({ status }) => {
	return (
		<>
			<div className={css.logoWrapper}>
				<img src='img/house.png' alt='bear' />
			</div>
			<h1>{status}</h1>
			<button className={css.arrowRight} type="button"><img src='img/arrowRight.svg' alt='arrowRight' /></button>
		</>
	)
}