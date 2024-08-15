import axios from '@/utils/axios'

export const getUserTasksRequest = async () => {
	return await axios.get(`/tasks?client_id=1`)
}

export const completeUserTaskRequest = async (taskId: number) => {
	return await axios.post(`/tasks/${taskId}/complete?client_id=1`)
}