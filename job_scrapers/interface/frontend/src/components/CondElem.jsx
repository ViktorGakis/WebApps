import React from "react";

function CondElem({ tagName, attributes, data, key }) {
	if (!data) {
		return null; // Return null if data is null or undefined
	}

	let content = data;

	if (key && data[key] !== null && data[key] !== undefined) {
		content = `${key}: ${data[key]}`;
	}

	const filteredAttributes = {};

	// Filter attributes to remove null or undefined values
	for (const attrKey in attributes) {
		if (attributes[attrKey] !== null && attributes[attrKey] !== undefined) {
			filteredAttributes[attrKey] = attributes[attrKey];
		}
	}

	if (Object.keys(filteredAttributes).length === 0) {
		return null; // Return null if all attributes are null or undefined
	}

	return React.createElement(tagName, filteredAttributes, content);
}

export default CondElem;
