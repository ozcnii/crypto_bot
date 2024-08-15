import { completeUserTaskRequest, getUserTasksRequest } from '@/utils/api/task'
import { Task, TaskState } from '@/utils/types/task'
import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'
import { showNotification } from './notificationSlice'

export const getUserTasks = createAsyncThunk('tasks/getUserTasks', async (_, {rejectWithValue}) => {
	try {
		const response = await getUserTasksRequest();
		if (response.status === 200) {
			return response.data
		}
		return rejectWithValue(response.data)
	} catch(error) {
		return rejectWithValue(error)
	}
})

export const completeUserTask = createAsyncThunk('tasks/completeUserTask', async (taskId: number, { rejectWithValue, dispatch }) => {
	try {
		const response = await completeUserTaskRequest(taskId);
		dispatch(showNotification({ message: 'Task completed', type: 'success', visible: true, logo: 'img/bear.png' }))
		return response.data
	} catch(error) {
		dispatch(showNotification({ message: error.response.data.message, type: 'error', visible: true, logo: 'img/brokenhouse.png' }))
		return rejectWithValue(error)
	}
})

const initialState: TaskState = {
	tasks: [] as Task[],
	error: null,
	status: 'none'
}

const tasksSlice = createSlice({
	name: 'tasks',
	initialState,
	reducers: {},
	extraReducers: (builder) => {
		builder
			.addCase(getUserTasks.pending, (state) => {
				state.status = 'loading'
			})
			.addCase(getUserTasks.fulfilled, (state, action) => {
				state.status = 'succeeded'
				state.tasks = action.payload
			})
			.addCase(getUserTasks.rejected, (state, action) => {
				state.status = 'failed'
				state.error = action.error
			})
			.addCase(completeUserTask.pending, (state) => {
				state.status = 'loading'
			})
			.addCase(completeUserTask.fulfilled, (state, action) => {
				state.status = 'succeeded'
				state.tasks = state.tasks.map((task) => 
					task.id === action.payload.id 
							? { ...task, completed: true }  // Создаем новый объект задачи с обновленным значением completed
							: task  // Оставляем задачу без изменений, если ID не совпадает
				)
			})
			.addCase(completeUserTask.rejected, (state, action) => {
				state.status = 'failed'
				state.error = action.error
			})
	}
})

export default tasksSlice.reducer