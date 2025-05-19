export function imageUrl(image) {
    const BASE_URL = import.meta.env.VITE_STATIC_URL
    return BASE_URL + image
}