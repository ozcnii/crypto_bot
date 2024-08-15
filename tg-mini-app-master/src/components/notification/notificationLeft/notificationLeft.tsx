import { FC } from 'react'
import css from './notificationLeft.module.css'

interface NotificationWindowProps {
	status: string
}
export const NotificationLeft: FC<NotificationWindowProps> = ({ status }) => {
	return (
		<>
			<div className={css.logoWrapper}>
				<img src='img/bear.png' alt='bear' />
			</div>
			<h1>{status}</h1>
			<button className={css.arrowRight} type="button"><img src='img/arrowRight.svg' alt='arrowRight' /></button>
		</>
	)
}