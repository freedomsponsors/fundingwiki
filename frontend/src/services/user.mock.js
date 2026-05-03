import { delay } from '@/utils/mock.js'

export async function getCurrentUserInfo() {
    await delay()
    return { logged_in: 1, username: 'mockuser' }
}

export async function isUserLogin() {
    await delay()
    return true
}
