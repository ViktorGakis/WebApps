import { delegateEvent, removeDelegatedEvent } from "./delegateEvent.js";
import { toggleDarkMode } from "./darkmode.js";
import { submitForm } from "./requests.js";
import { reloadAllResources } from "./reloading.js";

// Listen for clicks on the dark mode toggle button
async function DarkModeDE() {
	console.log("DarkModeED initialized!");
	return await delegateEvent(
		["click"], // event type
		["#toggle-theme"], // selector
		[toggleDarkMode] // handler
	);
}

//
async function formHandler(event) {
	event.preventDefault();
	const form = event.target;
	let rsp_data = await submitForm(form);
	console.log(`rsp_data:`, rsp_data);
	const div = document.createElement("div");
	div.innerHTML = `<h1>Form Response: id: [#${form.id}], method: [${form.method}]</h1>`;
	const rsp = document.createElement("pre");
	rsp.textContent = JSON.stringify(rsp_data, null, 2);
	console.log(`rsp.textContent: ${rsp.textContent}`);
	div.appendChild(rsp);
	document.body.appendChild(div);
}

// Listen for clicks on the dark mode toggle button
async function submitFormDE(form, handler = formHandler) {
	const form_str = form ? typeof form === "string" : JSON.stringify(form);
	console.log(`Form: [${form_str}] listener initialized!`);
	return await delegateEvent(
		["submit"], // event type
		[form], // selector
		[handler]
	);
}

// ReloadJsCssDE
async function reloadJsCssDE(selector) {
	console.log(`ReloadJsCssDE listener initialized!`);

	return await delegateEvent(
		["click"],
		[selector],
		[
			async (event) => {
				event.preventDefault();
				await reloadAllResources();
			},
		]
	);
}

async function testDE(selector = "#my-list li") {
	console.log(`testDE listener initialized!`);
	console.log("testDE", Date.now());
	return await delegateEvent(
		["click"],
		[selector],
		[
			async (event) => {
				console.log(event.target.innerHTML);
			},
		]
	);
}

export { DarkModeDE, submitFormDE, reloadJsCssDE, testDE };
