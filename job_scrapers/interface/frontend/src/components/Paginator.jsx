import React from "react";
import { handleFormRequest } from "../js/fetchapi";
import "./paginator.css";

export default function Paginator({
	data,
	formEndpoint,
	formRef,
	onUpdateData,
}) {
	const createPageLink = (page) => {
		const url = `${formEndpoint}&page=${page}`;
		console.log(`Paginator: url ${formEndpoint}`);
		return url;
	};

	const handlePageClick = async (e) => {
		const options = {
			url: e.target.href,
		};
		console.log(`handlePageClick: url: ${options.url}`);
		const rsp = await handleFormRequest(e, formRef, options);
		onUpdateData(rsp.data);
	};

	return (
		<div id="pagination">
			<nav>
				<h4>
					Per_page: {data.per_page}, Results: {data.total}
				</h4>
				<ul className="pagination">
					<li className="page-item">
						{data.has_prev ? (
							<a
								className="page-link"
								href={createPageLink(data.prev_num)}
								aria-label="Previous"
								onClick={handlePageClick}>
								&laquo;
							</a>
						) : (
							<span aria-hidden="true">&laquo;</span>
						)}
					</li>

					{data.iter_pages.map((pageNum) => (
						<li
							className="page-item"
							aria-current="page"
							key={pageNum}>
							{pageNum ? (
								<a
									className="page-link"
									href={createPageLink(pageNum)}
									onClick={handlePageClick}>
									{pageNum}
								</a>
							) : (
								"..."
							)}
						</li>
					))}

					<li className="page-item">
						{data.has_next ? (
							<a
								className="page-link"
								href={createPageLink(data.next_num)}
								aria-label="Next"
								onClick={handlePageClick}>
								&raquo;
							</a>
						) : (
							<span aria-hidden="true">&raquo;</span>
						)}
					</li>
				</ul>
			</nav>
		</div>
	);
}
