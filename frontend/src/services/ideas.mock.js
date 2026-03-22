import { delay } from '@/utils/mock.js'

const mockIdeas = [
    { id: 1, createdByUser: { id: 1, username: 'admin', email: 'admin@localhost' }, content: 'Build a crowdfunding platform for open source projects', date_created: '2026-01-01T10:00:00Z', point: 3, faiss_id: -1, idea_from: 'user' },
    { id: 2, createdByUser: { id: 2, username: 'Mai', email: 'mai@localhost' }, content: 'Create a peer-to-peer code review marketplace', date_created: '2026-01-02T11:00:00Z', point: 1, faiss_id: -1, idea_from: 'user' },
    { id: 3, createdByUser: { id: 3, username: 'Ana', email: 'ana@localhost' }, content: 'Decentralized bug bounty system', date_created: '2026-01-03T12:00:00Z', point: 5, faiss_id: -1, idea_from: 'user' },
]

const myIdeas = [mockIdeas[0]]

export async function saveIdea(idea_content) {
    await delay()
    const idea = { id: Date.now(), createdByUser: { id: 1, username: 'admin', email: 'admin@localhost' }, content: idea_content, date_created: new Date().toISOString(), point: 0, faiss_id: -1, idea_from: 'user' }
    mockIdeas.unshift(idea)
    myIdeas.unshift(idea)
    return { result: 'ok' }
}

export async function getIdeas() {
    await delay()
    return [...mockIdeas]
}

export async function deleteIdeaById(id) {
    await delay()
    const i = mockIdeas.findIndex(x => x.id === id)
    if (i !== -1) mockIdeas.splice(i, 1)
    return { result: 'ok' }
}

export async function getIdeasMine() {
    await delay()
    return [...myIdeas]
}

export async function getIdeasInterested() {
    await delay()
    return mockIdeas.slice(1)
}

export async function getSimilarIdeas() {
    await delay()
    return mockIdeas.slice(0, 2)
}

export async function ideasVote(id, vote_type) {
    await delay()
    return { result: 'ok' }
}

export async function getIdeaById(id) {
    await delay()
    return mockIdeas.find(x => x.id === Number(id)) ?? null
}
