import { flattenValues } from "./utils.js";

export { getFormData, sendRequest, submitForm, };
/**
 * Sends an HTTP request to the specified endpoint using the specified options.
 * @param {string} endpoint - The endpoint to send the request to.
 * @param {Object} options - The options for the request.
 * @param {string} options.method - The HTTP method for the request (default: 'GET').
 * @param {Object} options.data - The data to send with the request (default: null).
 * @param {Object} options.headers - The headers to include in the request (default: { 'Content-Type': 'application/json' }).
 * @param {string} options.responseType - The expected response type (default: 'json').
 * @param {Object} options.params - The URL parameters to include in the request (default: {}).
 * @returns {Promise} A promise that resolves to the response data if the request is successful, or rejects with an error if the request fails.
 */
async function sendRequest(endpoint, options = {}) {
	const requestOptions = processOptions(options);
	console.log("sendRequest requestOptions:", requestOptions);
	const url = buildUrl(endpoint, requestOptions.params);
	console.log("sendRequest buildUrl:", url);
	try {
		const response = await fetch(url, requestOptions);

		if (!response.ok) {
			throw new Error("Network response was not ok");
		}

		return await parseResponse(response, requestOptions.responseType);
	} catch (error) {
		console.error("Error:", error);
		throw error;
	}
}

/**
 * Processes the options for an HTTP request and returns a new options object with defaults and modifications applied.
 *
 * @param {Object} options - The options to process.
 * @param {string} options.method - The HTTP method to use. Default is "GET".
 * @param {*} options.data - The data to send in the request body. Default is null.
 * @param {Object} options.headers - The headers to send with the request. Default is { "Content-Type": "application/json" }.
 * @param {string} options.responseType - The response type to expect. Default is "json".
 * @param {Object} options.params - The query parameters to append to the URL. Default is {}.
 * @returns {Object} The processed options object.
 */
function processOptions(options) {
	const {
		method = "GET",
		data = null,
		headers = { "Content-Type": "application/json" },
		responseType = "json",
		params = {},
	} = options;

	const methodLowerCase = method.toLowerCase();

	const requestBody =
		methodLowerCase !== "get" && methodLowerCase !== "head"
			? { body: JSON.stringify(data) }
			: {};

	const urlParams =
		methodLowerCase === "get" || methodLowerCase === "head"
			? flattenValues(data, (value) => value[0])
			: params;

	return {
		method,
		...requestBody,
		headers,
		responseType,
		params: urlParams,
	};
}

function buildUrl(endpoint, params) {
	const query = Object.keys(params)
		.map(
			(key) =>
				`${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`
		)
		.join("&");
	return query ? `${endpoint}?${query}` : endpoint;
}

async function parseResponse(response, responseType) {
	if (responseType === "text") {
		return await response.text();
	} else if (responseType === "blob") {
		return await response.blob();
	} else if (responseType === "arrayBuffer") {
		return await response.arrayBuffer();
	} else {
		return await response.json();
	}
}

/**
 * Parses form data into an object or an array of entries.
 * @param {HTMLFormElement} formElement - The HTML form element to get data from.
 * @param {object} options - An options object.
 * @param {boolean} [options.excludeEmptyValues=false] - Whether to exclude empty values from the output.
 * @param {string} [options.outputFormat="object"] - The output format. Can be "object" (default) or "entries".
 * @param {Array} [options.excludedFields=[]] - An array of field names to exclude from the output.
 * @returns {object|Array} - The parsed data.
 */
function getFormData(formElement, options = {}) {
	const {
		excludeEmptyValues = false,
		outputFormat = "object",
		excludedFields = [],
	} = options;

	const formData = new FormData(formElement);
	const data = createOutputData(outputFormat);

	for (const [name, value] of formData.entries()) {
		if (shouldSkipField(name, value, excludeEmptyValues, excludedFields)) {
			continue;
		}

		if (outputFormat === "object") {
			appendToObjectData(data, name, value);
		} else {
			appendToEntriesData(data, name, value);
		}
	}

	return data;
}

function createOutputData(outputFormat) {
	return outputFormat === "object" ? {} : [];
}

function shouldSkipField(name, value, excludeEmptyValues, excludedFields) {
	return (
		(excludeEmptyValues && value.length === 0) ||
		excludedFields.includes(name)
	);
}

function appendToObjectData(data, name, value) {
	data[name] = data[name] || [];
	data[name].push(value);
}

function appendToEntriesData(data, name, value) {
	data.push([name, value]);
}

/**
 * Submits an HTML form element asynchronously using the specified options.
 *
 * @param {HTMLFormElement} formElement - The form element to submit.
 * @param {string} [endpoint=formElement.action] - The URL to submit the form to (default: form.action).
 * @param {Object} [options] - The options for the form submission.
 * @param {string} [options.method] - The HTTP method to use for the form submission (default: form.method or "POST").
 * @param {Object|FormData} [options.data=null] - The data to include in the form submission (default: null).
 * @param {Object} [options.headers={"Content-Type": "application/json"}] - The HTTP headers to include in the form submission (default: {"Content-Type": "application/json"}).
 * @param {string} [options.responseType] - The expected response type for the form submission (default: form.getAttribute("data-type") or "json").
 * @param {Object} [options.params={}] - The URL parameters to include in the form submission (default: {}).
 *
 * @returns {Promise} A Promise that resolves with the response data if the form submission is successful.
 * @throws {Error} Throws an Error if the form submission fails.
 */
async function submitForm(
	formElement,
	endpoint = formElement.action,
	options = {}
) {
	if (!(formElement instanceof HTMLFormElement)) {
		throw new Error("formElement must be an instance of HTMLFormElement");
	}

	if (typeof endpoint !== "string") {
		throw new Error("endpoint must be a string");
	}

	const formData = getFormData(formElement);
	console.log("SUBMITFORM formData", formData);

	const requestOptions = processRequestOptions(
		options,
		formElement.method || "POST",
		formData,
		formElement.getAttribute("data-type") || "json"
	);

	console.log("SUBMITFORM requestOptions", requestOptions);
	try {
		const response = await sendRequest(endpoint, requestOptions);
		return response;
	} catch (error) {
		console.error("Error submitting form:", error);
		throw error;
	}
}

function processRequestOptions(
	options,
	defaultMethod,
	defaultData,
	defaultResponseType
) {
	const {
		method = defaultMethod,
		data = defaultData,
		headers = { "Content-Type": "application/json" },
		responseType = defaultResponseType,
		params = {},
	} = options;

	return { method, data, headers, responseType, params };
}



