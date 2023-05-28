let cacheBust = Date.now();

const eventListenersUrl = `./modules/eventListeners.js?${cacheBust}`;
const checkboxformsUrl = `./checkboxforms.js?${cacheBust}`;
const preprocessdeUrl = `./preprocessde.js?${cacheBust}`;
const estimatordeUrl = `./estimator.js?${cacheBust}`;

// Create an object to store event listeners references
const eventListeners = {
	reloadJsCssde: null,
	plotlyde: null,
	checkboxHandlerde: null,
	sliderUpdatede: null,
	selectUpdatede: null,
	submitFormde: null,
	preprocessde: null,
	estimatorde: null,
};

async function main() {
	const eventListenersModule = await import(eventListenersUrl);
	const checkboxformsModule = await import(checkboxformsUrl);
	const preprocessdeModule = await import(preprocessdeUrl);
	const estimatorModule = await import(estimatordeUrl);

	eventListeners.reloadJsCssde = await eventListenersModule.reloadJsCssDE(".reloadjscss");
	eventListeners.plotlyde = await eventListenersModule.plotlyDE(".plotly");
	eventListeners.checkboxHandlerde = await checkboxformsModule.checkboxHandlerDE('input[type="checkbox"]');
	eventListeners.sliderUpdatede = await checkboxformsModule.sliderUpdateDE('input');
	eventListeners.selectUpdatede = await checkboxformsModule.sliderUpdateDE('select');
	eventListeners.estimatorde = await estimatorModule.estimatorFormDE('.estimator');

	// eventListeners.submitFormde = await submitFormDE('form')
	eventListeners.preprocessde = await preprocessdeModule.preprocessFormDE('#preprocess-form');
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

	// Reset cache busting for next load
	cacheBust = Date.now();
}

// Expose the init and destroy functions globally
window.myScript = { init, destroy };

// Initialize the script
(async () => {
    await init();
})();
