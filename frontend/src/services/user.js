import {post, get} from '../utils/request.js'

export async function getCurrentUserInfo() {
    var response = await get('vueapi/user', {})
    return response
}

export async function isUserLogin() {
    var response = await get('vueapi/user', {})
    return response.logged_in == 1
}