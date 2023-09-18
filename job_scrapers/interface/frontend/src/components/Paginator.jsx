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
		// const url = `${formEndpoint}&page=${page}`;
		const url = `${page}`;
		// console.log(`Paginator: url ${formEndpoint}`);
		return url;
	};

	const handlePageClick = async (e) => {
		e.preventDefault();
		const options = {
			page: e.target.getAttribute("data-page"),
			formEndpoint: formEndpoint,
		};
		console.log(`handlePageClick: page: ${options.page}`);
		console.log(`handlePageClick: formEndpoint: ${options.formEndpoint}`);
		const rsp = await handleFormRequest(e, formRef, options);
		onUpdateData(rsp.data);
	};

	return (
		<div id="pagination">
			<nav>
				<h4>
					Per_page: {data.per_page}, Results: {data.total}
				</h4>
				<div className="pagination">
					<div className="page-item">
						{data.has_prev ? (
							<a
								className="page-link"
								data-page={data.prev_num}
								href={createPageLink(data.prev_num)}
								aria-label="Previous"
								onClick={handlePageClick}>
								&laquo;
							</a>
						) : (
							<span aria-hidden="true">&laquo;</span>
						)}
					</div>

					{data.iter_pages.map((pageNum) => (
						<div
							className="page-item"
							aria-current="page"
							key={pageNum}>
							{pageNum ? (
								<a
									className="page-link"
									data-page={pageNum}
									href={createPageLink(pageNum)}
									onClick={handlePageClick}>
									{pageNum}
								</a>
							) : (
								"..."
							)}
						</div>
					))}

					<div className="page-item">
						{data.has_next ? (
							<a
								className="page-link"
								data-page={data.next_num}
								href={createPageLink(data.next_num)}
								aria-label="Next"
								onClick={handlePageClick}>
								&raquo;
							</a>
						) : (
							<span aria-hidden="true">&raquo;</span>
						)}
					</div>
				</div>
			</nav>
		</div>
	);
}
