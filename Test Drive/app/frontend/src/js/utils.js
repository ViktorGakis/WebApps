export { fetchAPI };

async function fetchData(url, params = {}) {
	try {
		const urlWithParams = new URL(url);
		Object.keys(params).forEach((key) =>
			urlWithParams.searchParams.append(key, params[key])
		);

		const response = await fetch(urlWithParams.href);
		const data = await response.json();

		if (!response.ok) {
			throw new Error(data.message || "Error fetching data");
		}

		return data;
	} catch (error) {
		console.error("Error fetching data:", error);
		throw error;
	}
}

async function fetchAPI(endpoint, params = {}) {
	const apiUrl = `http://localhost:8000/${endpoint}`;
	const response = await fetchData(apiUrl, params);
	return response;
}
