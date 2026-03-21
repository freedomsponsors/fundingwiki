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

/**
 * TODO: align the methods exported here with the shape of operations in the API DNA
 * This practice alone will naturally allow the whole software to evolve in a consistent and predictable way.
 */
export { post, get, delete_by_id }
