import {post, get, delete_by_id} from '../utils/request.js'

export async function saveSolution(issue_id, content) {
    let data = {
        issue_id: issue_id,
        content: content
    }
    var response = await post('vueapi/tech_solution', data)
    return response
}