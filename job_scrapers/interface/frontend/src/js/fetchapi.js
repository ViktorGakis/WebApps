async function fetchData(url, params = {}, payload = {}, method = "GET") {
	try {
		// console.log(`fetchData: url: ${url}`);
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
			console.error(`fetchData: url: ${url}. \nError fetching data`);
			throw new Error(data.message || "Error fetching data");
		}

		return data;
	} catch (error) {
		console.error(`fetchData: url: ${url}. \nError fetching data:`, error);
		throw error;
	}
}

export default async function fetchAPI(
	endpoint,
	params = {},
	payload = {},
	method = "GET"
) {
	// console.log(`fetchAPI: url: ${endpoint}`);
	return await fetchData(endpoint, params, payload, method);
}

export async function handleFormRequest(e, formRef, options = {}) {
	e.preventDefault();

	const formData = new FormData(formRef.current);
	const queryParameters = new URLSearchParams(formData).toString();

	const { url = null, formEndpoint = null, page = null } = options;

	if (url) {
		console.log(`handleFormRequest: url: ${url}`);
		return await fetchAPI(url);
	}
	let apiUrl = formEndpoint;
	console.log(`handleFormRequest: ${apiUrl}`);

	if (queryParameters) {
		apiUrl += `&${queryParameters}`;
		console.log(`handleFormRequest: ${apiUrl}`);
	}

	if (page !== null) {
		apiUrl += `&page=${page}`;
		console.log(`handleFormRequest: ${apiUrl}`);
	}
	console.log(`handleFormRequest: apiUrl: ${apiUrl}`);
	return await fetchAPI(apiUrl);
}
