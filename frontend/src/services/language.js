import {post, get} from '../utils/request.js'

export async function getLanguages() {
    return await get('vueapi/get_languages', {})
}