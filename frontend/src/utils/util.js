export function imageUrl(image) {
    const staticUrl = import.meta.env.VITE_STATIC_URL || import.meta.env.BASE_URL || '/'
    const base = staticUrl.endsWith('/') ? staticUrl.slice(0, -1) : staticUrl
    const path = image.startsWith('/') ? image : `/${image}`

    return `${base}${path}`
}
