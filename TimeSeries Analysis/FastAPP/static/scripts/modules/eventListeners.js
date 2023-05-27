import { delegateEvent } from "./delegateEvent.js";
import { submitForm } from "./requests.js";
import { reloadAllResources } from "./reloading.js";

export { submitFormDE, reloadJsCssDE, plotlyDE, formHandler };

//
async function formHandler(event) {
	event.preventDefault();
	const form = event.target;
	// let rsp_data = await submitForm(form);
	// return JSON.stringify(rsp_data, null, 2);
	return await submitForm(form);
}

async function handlePlots(obj) {
	const container = document.getElementById("anal_plots");
	// let obj = JSON.parse(plots)
	if (typeof obj === "object" && obj !== null) {
		const entries = Object.entries(obj);
		console.log('entries', entries);
		if (entries.length > 0) {
			if (obj.hasOwnProperty("data")) {
				container.innerHTML = obj.error;
			} else {
				entries.forEach(([key, val]) => {
					const resp = JSON.parse(val);
					const plot_div = document.createElement("div");
					plot_div.id = key;
					plot_div.style.width = "fit-content";
					container.appendChild(plot_div);
					const config = { displayModeBar: false };
					Plotly.newPlot(plot_div, resp.data, resp.layout, config);
				});
			}
		} else {
			container.innerHTML = "Object is empty";
		}
	} else if (typeof obj === "string") {
		container.innerHTML = "Object is a string";
	} else {
		container.innerHTML = "Object is neither an object nor a string";
	}
}

async function plotlyHandler(event) {
	try {
		let rsp  = await formHandler(event);
		console.log('rsp', rsp);
		await handlePlots(rsp);
	} catch (error) {
		console.error("Error:", error);
	}
}

async function plotlyDE(selector) {
	console.log(`plotlyDE listener initialized!`);
	return await delegateEvent(
		["submit"],
		[selector],
		[
			async (event) => {
				event.preventDefault();
				await plotlyHandler(event);
			},
		]
	);
}

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


// Form with table and checkbox inputs
async function handleCheckboxChange(chkBox) {
    // grab the TR containing the checkbox
    var parentRow = chkBox.closest('tr');
    
    // get all checkboxes inside this row
    var checkboxes = parentRow.querySelectorAll('input[type="checkbox"]');
    
    // reset all checkbox name and checked attributes in this row
    for (const element of checkboxes) {
        // remove '_checked' suffix from name if exists
        element.name = element.name.replace('_checked', '');
        // remove checked attribute
        element.checked = false;
    }

    // if this checkbox was initially checked, leave it unchecked
    if(chkBox.checked == false) {
        return;
    }
    
    // set the '_checked' suffix and 'checked' attribute to the changed checkbox
    chkBox.name += '_checked';
    chkBox.checked = true;
}
async  function checkboxHandlerDE(selector) {
	console.log(`checkboxHandlerDE listener initialized!`);

	return await delegateEvent(
		["click"],
		[selector],
		[
			async (event) => {
				event.preventDefault();
				await handleCheckboxChange(event);
			},
		]
	);	
}