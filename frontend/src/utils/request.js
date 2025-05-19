import axios from 'axios'
import { getCookie } from './cookies'

const BASE_URL = import.meta.env.VITE_API_URL

async function post(url, data) {
    var response = await axios.post(BASE_URL + url, data,{
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })

    return response.data
}

async function get(url, data) {
    var response = await axios.get(BASE_URL + url, {
        params: data,
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })

    return response.data
}

async function delete_by_id(url, id) {
    var response = await axios.delete(BASE_URL + url, {
        params: {id:id},
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })

    return response.data
}

export { post, get, delete_by_id }