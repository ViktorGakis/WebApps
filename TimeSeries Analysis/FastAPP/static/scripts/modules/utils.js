function toDict(data, keyFunc, valueFunc) {
	const iterableData = getIterableData(data);
	const dict = {};

	for (const [key, value] of iterableData) {
		dict[keyFunc ? keyFunc(key) : key] = valueFunc
			? valueFunc(value)
			: value;
	}

	return dict;
}

function getIterableData(data) {
	if (
		data instanceof Map ||
		Array.isArray(data) ||
		typeof data === "string"
	) {
		return data.entries();
	} else if (typeof data === "object" && data !== null) {
		return Object.entries(data);
	} else if (typeof data[Symbol.iterator] === "function") {
		return data;
	}

	throw new Error("Invalid data structure");
}

async function injectHTML(sourceUrl, targetSelector, callback) {
	try {
		const response = await fetch(sourceUrl);
		const html = await response.text();
		const parser = new DOMParser();
		const sourceDoc = parser.parseFromString(html, "text/html");
		const targetElement = document.querySelector(targetSelector);

		if (!targetElement) {
			throw new Error(
				`Target element with selector ${targetSelector} not found.`
			);
		}

		targetElement.innerHTML = sourceDoc.body.innerHTML;

		if (callback) {
			callback();
		}
	} catch (error) {
		throw new Error(`Error injecting HTML: ${error.message}`);
	}
}

function flattenValues(input, mapper) {
	if (!isIterable(input)) {
		return input;
	}

	const isArray = Array.isArray(input);
	const values = isArray ? input : [...input.values()];
	const isSingleValue = values.every(
		(value) => !isIterable(value) || getIterableLength(value) === 1
	);

	if (isSingleValue) {
		const output = isArray ? [] : {};

		for (const [i, value] of Object.entries(values)) {
			const key = isArray ? parseInt(i) : [...input.keys()][i];
			output[key] = isIterable(value)
				? (mapper || ((value) => value))(getFirstIterableValue(value))
				: (mapper || ((value) => value))(value);
		}

		return output;
	} else {
		return input;
	}
}

function isIterable(obj) {
	return obj != null && typeof obj[Symbol.iterator] === "function";
}

function getIterableLength(iterable) {
	let length = 0;
	for (const _ of iterable) {
		length++;
	}
	return length;
}

function getFirstIterableValue(iterable) {
	for (const value of iterable) {
		if (value === "") {
			return undefined;
		}
		return isIterable(value) ? getFirstIterableValue(value) : value;
	}
	return undefined;
}

export { toDict, injectHTML, flattenValues };
