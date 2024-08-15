import { FC } from 'react'
import css from './notificationWrong.module.css'

interface NotificationWrongProps {
	status: string
}

export const NotificationWrong: FC<NotificationWrongProps> = ({ status }) => {
	return (
		<>
			<div className={css.logoWrapper}>
				<img src='img/brokenhouse.png' alt='bear' />
			</div>
			<h1>{status}</h1>
			<button className={css.arrowRight} type="button"><img src='img/arrowRight.svg' alt='arrowRight' /></button>
		</>
	);
}