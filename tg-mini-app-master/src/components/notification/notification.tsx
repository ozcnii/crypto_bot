import Button from '@/assets/task/button'
import { RootState } from '@/store'
import { hideNotification } from '@/store/notificationSlice'
import { postEvent } from '@telegram-apps/sdk'
import { useEffect } from 'react'
import ReactDOM from 'react-dom'
import { useDispatch, useSelector } from 'react-redux'
import { CSSTransition } from 'react-transition-group'
import css from './notification.module.css'

const notifications = document.getElementById('notifications') as HTMLDivElement;

export const Notification: React.FC = () => {
    const dispatch = useDispatch();
    const { message, logo, visible, type } = useSelector((state: RootState) => state.notifications);

    useEffect(() => {
        if (visible) {
            const timer = setTimeout(() => {
                dispatch(hideNotification());
            }, 3000);

            return () => clearTimeout(timer);
        }
    }, [visible, dispatch]);

    useEffect(() => {
        if (visible) {
            postEvent('web_app_trigger_haptic_feedback', {
                type: 'notification',
                notification_type: type === 'success' ? 'success' : 'error',
            })
        }
    }, [visible, type]);

    return ReactDOM.createPortal(
        <CSSTransition
            in={visible}
            timeout={300}
            classNames={{
				enter: css['bottom-notification-animation-enter-from'],
				enterActive: css['bottom-notification-animation-enter-active'],
				exit: css['bottom-notification-animation-leave-to'],
				exitActive: css['bottom-notification-animation-leave-active'],
			}}
            unmountOnExit
        >
            <div className={css.kitBottomAlert}>
    	        <div className={css.message}>
                    <div className={css.icon}>
                        <img src={logo} alt='logo' />
                    </div>
                    {message}
                </div>
                <Button color={type === 'success' ? '#EEEEEE' : '#EA3E3E'} onClick={() => dispatch(hideNotification())} />
            </div>
        </CSSTransition>,
        notifications
    );
};