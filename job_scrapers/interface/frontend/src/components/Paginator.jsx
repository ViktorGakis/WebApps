import React, { useState } from "react";

function Paginator({ data, onPageChange }) {
	return (
		<div className="paginator">
			{/* Previous Button */}
			<button
				onClick={() => onPageChange(data.prev_num)}
				disabled={!data.has_prev}>
				Prev
			</button>

			{/* Page Numbers */}
			{Array.isArray(data.iter_pages) &&
				data.iter_pages.map((num) => (
					<button
						key={num}
						onClick={() => onPageChange(num)}
						className={num === data.page ? "active" : ""}>
						{num}
					</button>
				))}

			{/* Next Button */}
			<button
				onClick={() => onPageChange(data.next_num)}
				disabled={!data.has_next}>
				Next
			</button>
		</div>
	);
}

const Paginator = ({ data, endpoint, onPageChange }) => {
	const [page, setPage] = useState(data.page);
	const [hasPrev, setHasPrev] = useState(data.has_prev);
	const [prevNum, setPrevNum] = useState(data.prev_num);
	const [hasNext, setHasNext] = useState(data.has_next);
	const [nextNum, setNextNum] = useState(data.next_num);
	const [iterPages, setIterPages] = useState(data.iter_pages);
	const [perPage, setPerPage] = useState(data.per_page);
	const [total, setTotal] = useState(data.total);

	const handlePageChange = async (pageNum) => {
		try {
			const newData = await fetchAPI(`${endpoint}?page=${pageNum}`);
			setPage(newData.data.page);
			setHasPrev(newData.data.has_prev);
			setPrevNum(newData.data.prev_num);
			setHasNext(newData.data.has_next);
			setNextNum(newData.data.next_num);
			setIterPages(newData.data.iter_pages);
			setPerPage(newData.data.per_page);
			setTotal(newData.data.total);
		} catch (error) {
			console.error("Error fetching new page data:", error);
		}
	};

	const handlePageClick = (page) => {
		setPage(page);
		if (onPageChange) {
			onPageChange(page);
		}
	};

	return (
		<div id="pagination">
			<nav>
				<h4>
					Per_page: {perPage}, Results: {total}
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
