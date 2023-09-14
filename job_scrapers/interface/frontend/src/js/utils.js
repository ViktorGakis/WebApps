export function capitalizeString(string) {
	return string.charAt(0).toUpperCase() + string.slice(1);
}

const currentDateTime = new Date();
const options = {
	year: "numeric",
	month: "long",
	day: "numeric",
	hour: "numeric",
	minute: "numeric",
	second: "numeric",
	timeZone: "UTC",
};
export const formattedDateTime = currentDateTime.toLocaleString(
	"en-US",
	options
);
