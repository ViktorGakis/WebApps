async function lightModeActions(body, darkModeToggle) {
	body.classList.remove("dark-mode");
	body.classList.add("light-mode");
	darkModeToggle.innerHTML = "Dark Mode";
}

async function darkModeActions(body, darkModeToggle) {
	body.classList.add("dark-mode");
	body.classList.remove("light-mode");
	darkModeToggle.innerHTML = "Light Mode";
}

async function toggleDarkMode() {
	const body = document.body;
	const darkModeToggle = document.getElementById("toggle-theme");

	if (body.classList.contains("dark-mode")) {
		await lightModeActions(body, darkModeToggle);
	} else if (body.classList.contains("light-mode")) {
		await darkModeActions(body, darkModeToggle);
	} else {
		await lightModeActions(body, darkModeToggle);
	}
}

export { toggleDarkMode };
