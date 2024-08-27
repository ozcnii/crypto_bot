import { configureStore } from '@reduxjs/toolkit';
import clansReducer from './clanSlice';
import coinReducer from './coinSlice';
import leagueReducer from './leagueSlice';
import modalsReducer from './modalsSlice';
import notificationsReducer from './notificationSlice';
import ordersReducer from './ordersSlice';
import referralReducer from './referralSlice';
import tasksReducer from './tasksSlice';
import userReducer from './userSlice';

export const store = configureStore({
  reducer: {
    user: userReducer,
    clans: clansReducer,
    coin: coinReducer,
    modals: modalsReducer,
    tasks: tasksReducer,
    notifications: notificationsReducer,
    league: leagueReducer,
    referral: referralReducer,
    orders: ordersReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
