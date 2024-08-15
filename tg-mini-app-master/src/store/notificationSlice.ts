import { createSlice } from '@reduxjs/toolkit'

interface NotificationState {
    message: string;
    type: 'success' | 'error' | '';
    visible: boolean;
	logo: string;
}

const initialState: NotificationState = {
    message: '',
    type: '',
    visible: false,
	logo: '',
};

const notificationsSlice = createSlice({
    name: 'notifications',
    initialState,
    reducers: {
        showNotification(state, action) {
            state.message = action.payload.message;
            state.type = action.payload.type;
            state.visible = true;
						state.logo = action.payload.logo;
        },
        hideNotification(state) {
            state.visible = false;
        }
    }
});

export const { showNotification, hideNotification } = notificationsSlice.actions;
export default notificationsSlice.reducer;