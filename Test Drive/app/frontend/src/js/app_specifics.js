import { fetchAPI } from './utils'

export { fetchChapterQuestions, fetchChapters }

async function fetchChapters() {
    return await fetchAPI('api/chapters')
}

async function fetchChapterQuestions(chapter) {
	return await fetchAPI('api/chapter/questions', {"chapter":chapter})
}