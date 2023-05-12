import { delegateEvent } from "./delegateEvent.js";
import { submitForm } from "./requests.js";
import { reloadAllResources } from "./reloading.js";

export { submitFormDE, reloadJsCssDE, plotlyDE };

//
async function formHandler(event) {
	event.preventDefault();
	const form = event.target;
	// let rsp_data = await submitForm(form);
	// return JSON.stringify(rsp_data, null, 2);
	return await submitForm(form)
}

async function plotlyHandler(event) {
	console.log("event.target:", event.target);
	try {
		let plots = await formHandler(event);
		console.log("Object.keys(obj)", Object.keys(plots));
		let container = document.getElementById("anal_plots");
		console.log("container", container);

		for (const [k, val] of Object.entries(plots)) {
			console.log("k", k);
			let resp = JSON.parse(val);
			let plot_div = document.createElement("div");
			plot_div.id = k;
			plot_div.width = "fit content";
			container.appendChild(plot_div);
			let config = { displayModeBar: false };
			Plotly.newPlot(plot_div, resp.data, resp.layout, config);
		}
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

$(document).ready(function () {
	$(document).on("click", "button.plotly", function (e) {
		e.preventDefault();
		let btn = $(this);
		let method = btn.attr("formmethod");
		let url = btn.attr("formaction");
		let exec_stat = $("#exec_status");

		let req = $.ajax({
			type: method,
			url: url,
			data: { analytics_type: btn.attr("name") },
			// dataType: 'json',
			// contentType: 'application/json',
			// data: JSON.stringify({'okboi': form_data(form)})
		});

		btn.html(
			'RUNNING...<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>'
		);

		req.done(function (resp_json, status) {
			console.log(resp_json);

			let container = document.getElementById("anal_plots");
			for (const [k, val] of Object.entries(resp_json)) {
				let resp = JSON.parse(val);
				let plot_div = document.createElement("div");
				plot_div.id = k;
				plot_div.width = "fit content";
				container.appendChild(plot_div);
				let config = { displayModeBar: false };
				Plotly.newPlot(plot_div, resp.data, resp.layout, config);
			}
			btn.addClass("btn-success")
				.removeClass("btn-primary")
				.html("COMPLETED");
			btn.css({ color: "white" });
		});

		req.fail(function (resp, status) {
			exec_stat.html("ERROR");
			exec_stat.css("color", "red");
			// alert(`Something went wrong: resp: ${resp}`);
		});
	});
});
