import {post, get, delete_by_id} from '../utils/request.js'

export async function saveSolution(issue_id, content, solution_id = null) {
    let data = {
        issue_id: issue_id,
        content: content
    }
    if (solution_id) {
        data.id = solution_id
    }
    var response = await post('vueapi/tech_solution', data)
    return response
}

export async function getSolution(issue_id) {
    let data = {
        issue_id: issue_id
    }
    console.log('getSolution', data)
    var response = await get('vueapi/tech_solution', data)
    return response
}