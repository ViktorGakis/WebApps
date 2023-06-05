export { fetchAPI };

async function fetchData(url, params = {}, payload = {}, method = "GET") {
	try {
		const urlWithParams = new URL(url);
		Object.keys(params).forEach((key) =>
			urlWithParams.searchParams.append(key, params[key])
		);

		const requestOptions = {
			method,
			headers: {
				"Content-Type": "application/json",
			},
		};

		if (method !== "GET") {
			requestOptions.body = JSON.stringify(payload);
		}

		const response = await fetch(urlWithParams.href, requestOptions);
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

async function fetchAPI(endpoint, params = {}, payload = {}, method = "GET") {
	const apiUrl = `http://localhost:8000/${endpoint}`;
	const response = await fetchData(apiUrl, params, payload, method);
	return response;
}
