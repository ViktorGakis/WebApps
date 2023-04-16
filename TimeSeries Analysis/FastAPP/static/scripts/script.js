import {
	DarkModeDE,
	submitFormDE,
	reloadJsCssDE,
	testDE,
} from "./modules/eventListeners.js";
import { injectHTML } from "./modules/utils.js";

// Keep track of which scripts have been loaded
const loadedScripts = new Set();

// INJECT HTML
export function run(
	src = "http://localhost:8000/static/js_notes/0_Datastructures.html"
) {
	const div = document.createElement("div");
	div.id = "Datastructures";
	div.classList.add("container");
	div.innerHTML = "<h1>Js Datastructures</h1>";
	const div_child = document.createElement("div");
	div_child.classList.add("content");
	div.appendChild(div_child);
	document.body.appendChild(div);
	const sourceUrl = src;
	console.log("sourceUrl:", sourceUrl);
	const targetSelector = "#Datastructures .content";

	injectHTML(sourceUrl, targetSelector);
}

// Create an object to store event listeners references
const eventListeners = {
	darkMode: null,
	test: null,
	reloadJsCss: null,
	formGet: null,
	formPost: null,
};

async function main() {
	// ADD LISTENERS
	// ----------------------------------------------------------------
	// Dark mode listener
	eventListeners.darkMode = await DarkModeDE();
	eventListeners.test = await testDE();

	// Js Css Reloader
	eventListeners.reloadJsCss = await reloadJsCssDE("#reloadjscss");

	// ----------------------------------------------------------------
	// Form listener
	eventListeners.formGet = await submitFormDE("#my-form-get");
	eventListeners.formPost = await submitFormDE("#my-form-post");
}

// Initialize your script
async function init() {
	if (window.myScript && typeof window.myScript.destroy === "function") {
		window.myScript.destroy();
	}
	await main();
}

// Clean up before reloading
function destroy() {
	// Remove all event listeners
	for (const key in eventListeners) {
		if (eventListeners[key]) {
			eventListeners[key]();
		}
	}
}

// Expose the init and destroy functions globally
window.myScript = { init, destroy };

// Initialize the script
init();
