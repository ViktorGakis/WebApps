import { reloadJsCssDE, plotlyDE,  } from "./modules/eventListeners.js";

// Create an object to store event listeners references
const eventListeners = {
	reloadJsCssde: null,
	plotlyde: null
};

async function main() {
	eventListeners.reloadJsCssde = await reloadJsCssDE(".reloadjscss");
	eventListeners.plotlyde = await plotlyDE(".plotly")

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
