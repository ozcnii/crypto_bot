export type Task = {
	id: number
	name: string
	description: string
	progress: number
	target_value: number
	reward: number
	completed: boolean
	task_type: string
}

export type TaskState = {
	tasks: Task[],
	status: string,
	error: string | null
}