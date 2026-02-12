export interface Post {
    id: number
    title: string
    excerpt: string
    content?: string
    tags: string[]
    created_at?: string
}