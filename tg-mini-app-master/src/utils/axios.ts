import axios from 'axios'

import { SERVER_URL } from '@/utils/constants'

const instance = axios.create({
    baseURL: SERVER_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

instance.interceptors.request.use(config => {
  config.headers.Authorization = `Bearer ${localStorage.getItem('api_key')}`
  return config
})

export default instance