import axios from 'axios'
import { getCookie } from './cookies'

async function post(url, data) {
    var response = await axios.post('http://127.0.0.1:8000/' + url, data,{
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })

    return response.data
}

async function get(url, data) {
    var response = await axios.get('http://127.0.0.1:8000/' + url, {
        params: data,
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })

    return response.data
}

async function delete_by_id(url, id) {
    var response = await axios.delete('http://127.0.0.1:8000/' + url, {
        params: {id:id},
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })

    return response.data
}

export { post, get, delete_by_id }