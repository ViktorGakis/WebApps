import { reloadJsCssDE, plotlyDE } from "./modules/eventListeners.js";
import { checkboxHandlerDE, sliderUpdateDE } from "./checkboxforms.js";
import { preprocessFormDE } from "./preprocessde.js";

// Create an object to store event listeners references
const eventListeners = {
	reloadJsCssde: null,
	plotlyde: null,
	checkboxHandlerde: null,
	sliderUpdatede: null,
	selectUpdatede: null,
	submitFormde: null,
	preprocessde: null,
};

async function main() {
	eventListeners.reloadJsCssde = await reloadJsCssDE(".reloadjscss");
	eventListeners.plotlyde = await plotlyDE(".plotly")
	eventListeners.checkboxHandlerde = await checkboxHandlerDE('input[type="checkbox"]')
	eventListeners.sliderUpdatede = await sliderUpdateDE('input')
	eventListeners.selectUpdatede = await sliderUpdateDE('select')

	// eventListeners.submitFormde = await submitFormDE('form')
	eventListeners.preprocessde = await preprocessFormDE('#preprocess-form')
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
