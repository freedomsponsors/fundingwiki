import {post, get, delete_by_id} from '../utils/request.js'

export async function saveSolutionComment(solution_id, content) {
    let data = {
        solution_id: solution_id,
        content: content
    }
    var response = await post('vueapi/tech_solution_comment', data)
    return response
}