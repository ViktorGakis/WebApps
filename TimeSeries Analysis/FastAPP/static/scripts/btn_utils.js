export { addCloseButton }

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