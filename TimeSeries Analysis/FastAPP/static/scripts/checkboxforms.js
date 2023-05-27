import { delegateEvent } from "./modules/delegateEvent.js";

export {checkboxHandlerDE, sliderUpdateDE};

// Form with table and checkbox inputs
async function handleCheckboxChange(chkBox) {
    // grab the TR containing the checkbox
    let parentRow = chkBox.closest('tr');
    
    // get all checkboxes inside this row
    let checkboxes = parentRow.querySelectorAll('input[type="checkbox"]');
    
    // reset all checkbox name and checked attributes in this row
    for (const element of checkboxes) {
        // if this checkbox is not the one that changed, uncheck it
        if(element !== chkBox) {
            // remove '_checked' suffix from name if exists
            element.name = element.name.replace('_checked', '');
            // remove checked attribute
            element.checked = false;
            element.removeAttribute('checked');
        }
    }

    // if this checkbox is checked, add _checked suffix
    if(chkBox.checked == true) {
        chkBox.name += '_checked';
        chkBox.setAttribute('checked', '');
    } else { // if it's not checked, remove _checked suffix
        chkBox.name = chkBox.name.replace('_checked', '');
        chkBox.removeAttribute('checked');
    }
}



async function checkboxHandlerDE(selector) {
	console.log(`checkboxHandlerDE listener initialized!`);
	return await delegateEvent(
		["change"],
		[selector],
		[
			async (event) => {
				event.preventDefault();
				await handleCheckboxChange(event.target);
			},
		]
	);
}


// SLIDER LISTENER
async function updateValue(inputField) {
    let checkbox = inputField.previousElementSibling;
    while (checkbox && checkbox.type !== "checkbox") {
        checkbox = checkbox.previousElementSibling;
    }
    if (checkbox) {
        checkbox.value = inputField.value;
    }

    const valueElement = inputField.nextElementSibling;
    if (valueElement && valueElement.tagName === "SPAN") {
        valueElement.textContent = inputField.value;
    }
}

async function sliderUpdateDE(selector) {
	console.log(`sliderUpdateDE listener initialized!`);
	return await delegateEvent(
		["input"],
		[selector],
		[
			async (event) => {
				event.preventDefault();
				await updateValue(event.target);
			},
		]
	);
}