async function fetchData(url, params = {}, payload = {}, method = "GET") {
	try {
		console.log(`url: ${url}`);
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
			console.error(`url: ${url}. \nError fetching data`);
			throw new Error(data.message || "Error fetching data");
		}

		return data;
	} catch (error) {
		console.error(`url: ${url}. \nError fetching data:`, error);
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

export async function handleFormRequest(e, formRef, options = {}) {
	e.preventDefault();

	const formData = new FormData(formRef.current);
	const queryParameters = new URLSearchParams(formData).toString();

	const { url = null, formEndpoint = null, page = null } = options;

	if (url) {
		return await fetchAPI(url);
	}
	let apiUrl = formEndpoint;

	if (queryParameters) {
		apiUrl += `?${queryParameters}`;
	}

	if (page !== null) {
		apiUrl += `&page=${page}`;
	}

	return await fetchAPI(apiUrl);
}
