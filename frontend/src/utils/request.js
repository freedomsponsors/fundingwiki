import axios from 'axios'
import { getCookie } from './cookies'

// const BASE_URL = 'http://127.0.0.1:8000/'
const BASE_URL = 'https://alfinal.eu.pythonanywhere.com/'

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