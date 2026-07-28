import {post, get, delete_by_id} from '../utils/request.js'

export async function saveSolutionComment(solution_id, content, editingCommentId = null) {
    let data = {
        solution_id: solution_id,
        content: content
    }
    if (editingCommentId) {
        data.comment_id = editingCommentId
    }
    var response = await post('vueapi/tech_solution_comment', data)
    return response
}

export async function getSolutionComments(solution_id) {
    let data = {
        solution_id: solution_id
    }
    var response = await get('vueapi/tech_solution_comment', data)
    return response
}