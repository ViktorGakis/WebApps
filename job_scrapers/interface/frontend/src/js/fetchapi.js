async function fetchData(url, params = {}, payload = {}, method = "GET") {
	try {
		const urlWithParams = new URL(url);
		Object.keys(params).forEach((key) =>
			urlWithParams.searchParams.append(key, params[key])
		);

		const requestOptions = {
			method,
			headers: {
				Accept: "application/json",
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

export default async function fetchAPI(
	endpoint,
	params = {},
	payload = {},
	method = "GET"
) {
	return await fetchData(endpoint, params, payload, method);
}
