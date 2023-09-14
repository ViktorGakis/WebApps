// Utility functions
function isDocumentReady(target) {
	return ["complete", "interactive"].includes(target.readyState);
}

function callWhenReady(target, onReady) {
	if (isDocumentReady(target)) {
		onReady();
	} else {
		target.addEventListener("DOMContentLoaded", onReady);
	}
}

async function createEventListener(selector, handler) {
	return async function (event) {
		if (selector) {
			const targetElement = event.target.closest(selector);
			if (targetElement) {
				await handler(event);
			}
		} else {
			// If no selector is passed, call the handler for all events
			await handler(event);
		}
	};
}

// Main delegateEvent function
let delegatedEvents = [];

async function delegateEvent(eventTypes, selectors = [], handlers) {
	if (selectors === null) {
		selectors = [];
	}

	const newDelegatedEvents = await Promise.all(
		eventTypes.map(async function (eventType, i) {
			const selector = selectors.length > i ? selectors[i] : null;
			const handler = handlers[i];

			const existingListener = delegatedEvents.find(
				(de) => de.eventType === eventType && de.selector === selector
			);

			if (existingListener) {
				console.log(
					"Removing existing listener:",
					existingListener.eventType,
					existingListener.selector
				);
				document.removeEventListener(
					existingListener.eventType,
					existingListener.listener
				);
				delegatedEvents = delegatedEvents.filter(
					(de) => de !== existingListener
				);
			}

			const listener = await createEventListener(selector, handler);

			callWhenReady(document, () => {
				document.addEventListener(eventType, listener);
			});

			return { eventType, selector, listener };
		})
	);

	delegatedEvents.push(...newDelegatedEvents.filter(Boolean));

	return function () {
		newDelegatedEvents.forEach((delegatedEvent) => {
			if (delegatedEvent) {
				document.removeEventListener(
					delegatedEvent.eventType,
					delegatedEvent.listener
				);
			}
		});
	};
}

async function removeDelegatedEvent(eventType, selector = null) {
	delegatedEvents = await delegatedEvents.filter(async function (
		delegatedEvent
	) {
		const selectorMatches = selector
			? delegatedEvent.selector === selector
			: true;
		if (delegatedEvent.eventType === eventType && selectorMatches) {
			document.removeEventListener(eventType, delegatedEvent.listener);
			return false;
		}
		return true;
	});
}

export { delegateEvent, removeDelegatedEvent };
