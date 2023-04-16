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
		const targetElement = event.target.closest(selector);
		if (targetElement) {
			await handler(event);
		}
	};
}

// Main delegateEvent function
let delegatedEvents = [];

async function delegateEvent(eventTypes, selectors, handlers) {
	const newDelegatedEvents = await Promise.all(
		eventTypes.map(async function (eventType, i) {
			const selector = selectors[i];
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

async function removeDelegatedEvent(eventType, selector) {
	delegatedEvents = await delegatedEvents.filter(async function (
		delegatedEvent
	) {
		if (
			delegatedEvent.eventType === eventType &&
			delegatedEvent.selector === selector
		) {
			document.removeEventListener(eventType, delegatedEvent.listener);
			return false;
		}
		return true;
	});
}

export { delegateEvent, removeDelegatedEvent };
