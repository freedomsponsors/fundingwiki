import {post, get, delete_by_id} from '../utils/request.js'

export async function saveIdea(idea_content) {
    let data = {
        idea_content:idea_content
    }
    var response = await post('vueapi/ideas', data)
    return response
}

export async function getIdeas(data) {
    var response = await get('vueapi/ideas', data)
    return response
}

export async function deleteIdeaById(id) {
    var response = await delete_by_id('vueapi/ideas', id)
    return response
}

export async function getIdeasMine() {
    var response = await get('vueapi/ideas_my', {})
    return response
}

export async function getIdeasInterested() {
    var response = await get('vueapi/ideas_interested', {})
    return response
}

export async function getSimilarIdeas(id) {
    var response = await get('vueapi/ideas_similar', {id:id})
    return response
}

export async function ideasVote(id, vote_type) {
    var response = await post('vueapi/idea_vote', {id:id, vote_type:vote_type})
    return response
}

export async function getIdeaById(id) {
    var response = await get('vueapi/get_idea_by_id', {id:id})
    return response
}