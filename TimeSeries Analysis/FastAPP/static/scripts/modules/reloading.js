/**
 * Applies cache busting to the `src` or `href` attribute of a URL based on the specified technique.
 *
 * @param {URL} url - The URL to apply cache busting to.
 * @param {string} cacheBustingTechnique - The cache busting technique to apply. Can be "queryParam", "fileName", or "none".
 * @returns {void}
 * @throws {TypeError} If the `url` parameter is not a valid `URL` object.
 * @throws {Error} If the `cacheBustingTechnique` parameter is unknown.
 */
function applyCacheBusting(url, cacheBustingTechnique) {
	if (!(url instanceof URL)) {
		throw new TypeError(`Invalid URL object: ${url}`);
	}

	if (cacheBustingTechnique === "none") {
		return;
	}

	if (cacheBustingTechnique === "queryParam") {
		url.searchParams.set("cacheBust", Date.now());
	} else if (cacheBustingTechnique === "fileName") {
		const fileName = url.pathname.split("/").pop().split(".");
		const newFileName = `${fileName[0]}-${Date.now()}.${fileName[1]}`;
		url.pathname = url.pathname.replace(fileName.join("."), newFileName);
	} else {
		throw new Error(
			`Unknown cache busting technique: ${cacheBustingTechnique}`
		);
	}
}

/**
 * Copies the attributes of an old resource to a new resource while applying cache busting techniques to any `src` or `href` attributes.
 *
 * @param {Element} oldResource - The old resource element to copy attributes from.
 * @param {Element} newResource - The new resource element to copy attributes to.
 * @param {string} cacheBustingTechnique - The cache busting technique to apply. Can be "queryParam", "fileName", or "none".
 * @returns {void}
 */
function copyAttributesWithCacheBusting(
	oldResource,
	newResource,
	cacheBustingTechnique
) {
	Array.from(oldResource.attributes).forEach((attribute) => {
		if (attribute.name === "src" || attribute.name === "href") {
			const url = new URL(attribute.value, window.location.href);
			applyCacheBusting(url, cacheBustingTechnique);
			newResource.setAttribute(attribute.name, url.toString());
		} else {
			newResource.setAttribute(attribute.name, attribute.value);
		}
	});
}

/**
 * Copies the content of an inline script from an old resource to a new resource, if the `reloadInlineScripts` flag is set to `true`.
 *
 * @param {Element} oldResource - The old resource element to copy the inline script content from.
 * @param {Element} newResource - The new resource element to copy the inline script content to.
 * @param {boolean} reloadInlineScripts - Flag indicating whether to reload inline scripts by copying their content.
 * @returns {void}
 */

function copyInlineScriptContent(
	oldResource,
	newResource,
	reloadInlineScripts
) {
	if (
		reloadInlineScripts &&
		oldResource.tagName.toLowerCase() === "script" &&
		oldResource.textContent
	) {
		newResource.textContent = oldResource.textContent;
	}
}

/**
 * Creates a new resource element based on an old resource element, while applying cache busting techniques and optionally copying the content of any inline scripts.
 *
 * @param {Element} oldResource - The old resource element to base the new resource element on.
 * @param {boolean} reloadInlineScripts - Flag indicating whether to reload inline scripts by copying their content.
 * @param {string} cacheBustingTechnique - The cache busting technique to apply. Can be "queryParam", "fileName", or "none".
 * @returns {Element} The new resource element.
 */

async function createNewResourceElement(
	oldResource,
	reloadInlineScripts,
	cacheBustingTechnique
) {
	const newResource = document.createElement(oldResource.tagName);
	copyAttributesWithCacheBusting(
		oldResource,
		newResource,
		cacheBustingTechnique
	);
	copyInlineScriptContent(oldResource, newResource, reloadInlineScripts);
	return newResource;
}

/**
 * Generates an array of CSS selectors based on the specified resource types.
 *
 * @param {Array<string>} resourceTypes - An array of resource types to generate selectors for. Can include "script" and/or "link".
 * @returns {Array<string>} An array of CSS selectors for the specified resource types.
 */

function getResourceSelectors(resourceTypes) {
	return resourceTypes
		.map((type) => {
			if (type === "script") return "script";
			if (type === "link") return 'link[rel="stylesheet"]';
			return "";
		})
		.filter((selector) => selector);
}

/**
 * Reloads a single resource element by creating a new element with cache busting applied, copying any inline script content, and replacing the old element with the new element.
 *
 * @param {Element} oldResource - The old resource element to be replaced.
 * @param {boolean} reloadInlineScripts - Flag indicating whether to reload inline scripts by copying their content.
 * @param {string} cacheBustingTechnique - The cache busting technique to apply. Can be "queryParam", "fileName", or "none".
 * @returns {Promise<void>} A Promise that resolves when the new resource element has been loaded and the old resource element has been removed.
 */
async function reloadResource(
	oldResource,
	reloadInlineScripts,
	cacheBustingTechnique
) {
	const newResource = await createNewResourceElement(
		oldResource,
		reloadInlineScripts,
		cacheBustingTechnique
	);

	newResource.onload = async () => {
		oldResource.remove();
	};

	newResource.onerror = async () =>
		console.error(
			`Failed to reload resource: ${newResource.src || newResource.href}`
		);

	oldResource.parentNode.insertBefore(newResource, oldResource);
	await new Promise((resolve) => setTimeout(resolve, 0));
}

/**
 * Filters resources containing the specified keyword in their "src" or "href" attribute.
 *
 * @param {Array<Element>} resources - An array of resource elements.
 * @param {string} keyword - The keyword to filter resources by.
 * @returns {Array<Element>} An array of filtered resource elements.
 */
function filterResourcesByKeyword(resources, keyword) {
	return resources.filter((tag) => {
		const srcOrHref = tag.getAttribute("src") || tag.getAttribute("href");
		return srcOrHref && srcOrHref.includes(keyword);
	});
}

/**
 * Reloads all resource elements of a specified type by calling `reloadResource` for each element.
 *
 * @param {boolean} [reloadInlineScripts=false] - Flag indicating whether to reload inline scripts by copying their content.
 * @param {Array<string>} [resourceTypes=["script", "link"]] - An array of resource types to reload. Can include "script" and/or "link".
 * @param {string} [cacheBustingTechnique="fileName"] - The cache busting technique to apply. Can be "queryParam", "fileName", or "none".
 * @param {string} [filterKeyword="localhost"] - A string keyword to filter resources by. Resources with the specified keyword in their "src" or "href" attribute will be reloaded.
 * @returns {Promise<void>} A Promise that resolves when all resource elements have been reloaded.
 */
async function reloadAllResources(
	reloadInlineScripts = false,
	resourceTypes = ["script", "link"],
	cacheBustingTechnique = "queryParam",
	filterKeyword = "localhost"
) {
	const resourceSelectors = getResourceSelectors(resourceTypes);
	const resourceTags = document.querySelectorAll(
		resourceSelectors.join(", ")
	);

	const resourcesToReload = filterKeyword
		? filterResourcesByKeyword(Array.from(resourceTags), filterKeyword)
		: Array.from(resourceTags);

	await Promise.all(
		resourcesToReload.map((oldResource) =>
			reloadResource(
				oldResource,
				reloadInlineScripts,
				cacheBustingTechnique
			)
		)
	);
}

export { reloadAllResources };
