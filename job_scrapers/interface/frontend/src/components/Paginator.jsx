import React, { useState } from "react";
import fetchAPI from "../js/fetchapi";

const Paginator = ({ data, endpoint }) => {
	const [page, setPage] = useState(data.page);
	const [hasPrev, setHasPrev] = useState(data.has_prev);
	const [prevNum, setPrevNum] = useState(data.prev_num);
	const [hasNext, setHasNext] = useState(data.has_next);
	const [nextNum, setNextNum] = useState(data.next_num);
	const [iterPages, setIterPages] = useState(data.iter_pages);
	const [paginationData, setPaginationData] = useState(data);

	const handlePageChange = async (pageNum) => {
		try {
			const newData = await fetchAPI(`${endpoint}?page=${pageNum}`);
			setPage(newData.data.page);
			setHasPrev(newData.data.has_prev);
			setPrevNum(newData.data.prev_num);
			setHasNext(newData.data.has_next);
			setNextNum(newData.data.next_num);
			setIterPages(newData.data.iter_pages);
			setPaginationData(newData.data);
		} catch (error) {
			console.error("Error fetching new page data:", error);
		}
	};

	return (
		<div id="pagination">
			<nav>
				<h4>
					Per_page: {paginationData.per_page}, Results:{" "}
					{paginationData.total}
				</h4>
				<ul className="pagination justify-content-center">
					<li className="page-item">
						{hasPrev ? (
							<a
								className="page-link"
								href="#"
								onClick={(e) => {
									e.preventDefault();
									handlePageChange(prevNum);
								}}
								aria-label="Previous">
								&laquo;
							</a>
						) : (
							<span aria-hidden="true">&laquo;</span>
						)}
					</li>

					{iterPages.map((pageNum) => (
						<li
							key={pageNum}
							className="page-item"
							aria-current="page">
							<a
								className={`page-link ${
									page === pageNum ? "active" : ""
								}`}
								href="#"
								onClick={(e) => {
									e.preventDefault();
									handlePageChange(pageNum);
								}}>
								{pageNum}
							</a>
						</li>
					))}

					<li className="page-item">
						{hasNext ? (
							<a
								className="page-link"
								href="#"
								onClick={(e) => {
									e.preventDefault();
									handlePageChange(nextNum);
								}}
								aria-label="Next">
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
};

export default Paginator;
