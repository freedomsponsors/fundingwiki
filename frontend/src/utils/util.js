export function imageUrl(image) {
    const staticUrl = import.meta.env.VITE_STATIC_URL || import.meta.env.BASE_URL || '/'
    const base = staticUrl.endsWith('/') ? staticUrl.slice(0, -1) : staticUrl
    const path = image.startsWith('/') ? image : `/${image}`

    return `${base}${path}`
}

export function relativeTimeFrom(value) {
    if (!value) {
        return ''
    }

    const date = value instanceof Date ? value : new Date(value)
    if (Number.isNaN(date.getTime())) {
        return String(value)
    }

    const now = new Date()
    const diffSeconds = Math.round((date.getTime() - now.getTime()) / 1000)
    const absSeconds = Math.abs(diffSeconds)

    if (absSeconds < 5) {
        return 'just now'
    }

    const units = [
        { unit: 'year', seconds: 31536000 },
        { unit: 'month', seconds: 2592000 },
        { unit: 'week', seconds: 604800 },
        { unit: 'day', seconds: 86400 },
        { unit: 'hour', seconds: 3600 },
        { unit: 'minute', seconds: 60 },
        { unit: 'second', seconds: 1 },
    ]

    const { unit, seconds } = units.find((item) => absSeconds >= item.seconds) || units[units.length - 1]
    const valueCount = Math.round(diffSeconds / seconds)
    const formatter = new Intl.RelativeTimeFormat('en', { numeric: 'auto' })

    return formatter.format(valueCount, unit)
}
