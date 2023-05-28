import { delegateEvent } from "./modules/delegateEvent.js";
import { formHandler } from "./modules/eventListeners.js";
export { estimatorFormDE };

// Function to add a close button to a div element
function addCloseButton(divElement) {
	// Set the position of the divElement to relative
	divElement.style.position = "relative";

	// Create the close button element
	const closeButton = document.createElement("button");
	closeButton.textContent = "X";
	closeButton.classList.add("btn", "btn-outline-danger", "close-button");
	closeButton.type = "button";

	// Add event listener to delete the div when clicked
	closeButton.addEventListener("click", () => {
		divElement.remove();
	});

	// Append the close button to the div element
	divElement.appendChild(closeButton);
}

async function createDivElements(rsp, parentElem) {
	// If parentElement is not provided, default to the document body
	parentElem = parentElem || document.body;

	Object.entries(rsp).forEach(([key, val]) => {
		// Create a new <div> element
		let divElement = document.createElement("div");

		divElement.style.border = "1px solid";
		// Set the id of the div element to the key name
		divElement.id = key;

		// Create an <h3> heading element
		let headingElement = document.createElement("h3");
		// Set the heading text to the key name
		headingElement.textContent = key;

		if (key.endsWith("_plotly")) {
			const resp = JSON.parse(val);
			divElement.style.width = "fit-content";
			const config = { displayModeBar: false };
			Plotly.newPlot(divElement, resp.data, resp.layout, config);
		} else if (key.endsWith("_pre")) {
			// Create a new <pre> element
			let preElement = document.createElement("pre");

			// Set the content of the <pre> element
			preElement.textContent = rsp[key];

			// Append the <pre> element to the <div> element
			divElement.appendChild(preElement);
		} else if (key.endsWith("_html")) {
			divElement.innerHTML = rsp[key];
		} else {
			console.log(`No valid type suffix found in ${key}.`);
			return;
		}

		// Append the heading and value to the div element
		divElement.insertBefore(headingElement, divElement.firstChild);

		addCloseButton(divElement);

		// Append the div element to the parent element
		parentElem.appendChild(divElement);
	});
}

// Form with table and checkbox inputs
async function estimatorHandler(event) {
	try {
		let rsp = await formHandler(event);
		console.log("rsp", rsp);
		let container = event.target.parentNode.parentNode;
		await createDivElements(rsp, container);
	} catch (error) {
		console.error("Error:", error);
	}
}

async function estimatorFormDE(form) {
	const form_str = form ? typeof form === "string" : JSON.stringify(form);
	console.log(`Estimator Form: [${form_str}] listener initialized!`);
	return await delegateEvent(
		["submit"], // event type
		[form], // selector
		[estimatorHandler]
	);
}
