from ... import db
from .QueryBuilder import QueryBuilder
from .scraper import Scraper

structure_dict = dict(
    scraper=Scraper,
    querybuilder=QueryBuilder,
    request_model=db.models.jobsch.Request,
    sub_request_model=db.models.jobsch.Sub_Request,
    job_model=db.models.jobsch.Job,
    job_id="job_id",
)