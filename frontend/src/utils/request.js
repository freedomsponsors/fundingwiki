import axios from 'axios'
import { getCookie } from './cookies'

const api = axios.create({ baseURL: import.meta.env.VITE_API_URL, withCredentials: true })
api.interceptors.request.use(config => {
    config.headers['X-CSRFToken'] = getCookie('csrftoken')
    return config
})

async function post(url, data) {
    return (await api.post(url, data)).data
}

async function get(url, data) {
    return (await api.get(url, { params: data })).data
}

async function delete_by_id(url, id) {
    return (await api.delete(url, { params: { id } })).data
}

export { post, get, delete_by_id }
