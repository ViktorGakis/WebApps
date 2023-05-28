import { delegateEvent } from "./modules/delegateEvent.js";
import { formHandler } from "./modules/eventListeners.js";
export { preprocessFormDE };

async function createDivElements(rsp, parentElement) {
	// If parentElement is not provided, default to the document body
	parentElement = parentElement || document.body;

	// Iterate over the keys in the rsp dictionary
	let breakLoop = false; // Flag to track breaking the loop
	Object.keys(rsp).forEach(function (key) {
		if (breakLoop) return; // Exit the loop if the flag is true

		// Create a new <div> element
		let divElement = document.createElement("div");

		// Set the id of the div element to the key name
		divElement.id = key;

		// Create an <h3> heading element
		let headingElement = document.createElement("h3");
		// Set the heading text to the key name
		headingElement.textContent = key;

		// Append the heading and value to the div element
		divElement.innerHTML = rsp[key];
		divElement.insertAdjacentHTML("afterbegin", headingElement);

		// Append the div element to the parent element
		parentElement.appendChild(divElement);

		// Set the flag to true to break the loop after the first iteration
		breakLoop = true;
	});
}

// Form with table and checkbox inputs
async function preprocessHandler(event) {
	try {
		let rsp = await formHandler(event);
		console.log("rsp", rsp);
		let container = event.target.parentNode;
		Object.keys(rsp).forEach(function (key) {
			const resp = JSON.parse(rsp[key]);
			const plot_div = document.createElement("div");
			plot_div.id = key;
			plot_div.style.width = "fit-content";
			container.appendChild(plot_div);
			const config = { displayModeBar: false };
			Plotly.newPlot(plot_div, resp.data, resp.layout, config);
		});
	} catch (error) {
		console.error("Error:", error);
	}
}

async function preprocessFormDE(form) {
	const form_str = form ? typeof form === "string" : JSON.stringify(form);
	console.log(`Preprocess Form: [${form_str}] listener initialized!`);
	return await delegateEvent(
		["submit"], // event type
		[form], // selector
		[preprocessHandler]
	);
}
