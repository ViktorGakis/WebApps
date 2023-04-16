from logging import Logger
from typing import Callable, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from fastapi.routing import APIRoute, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pprint import pformat
from .config import APISettings
from .logger import logdef

log: Logger = logdef(__name__)


class AppFactory(FastAPI):
    """
    Creates an app instance which addresses issues of

        1) Scalability (adding more routers, jinja global variables, jinja filters, etc...)

        2) Easy Debugging (setup and access attributes easily)

    ================================================================

    Args:
        jinja_global_vars(dict[str, Any]): A dictionary containing the names and values of all
            variables to be added as global jinja variables.

        jinja_filters(dict[str, Callable]): A dictionary containing the names
            and callables to be added as jinja filters.

        kwds (FastAPI): App instance kwds.

    ================================================================

    Attributes:
        config (APISettings): Config object.

        unregistered_routers (List[APIRouter]): List of all the (unregistered) routers in module routers.

        registered_routers (list[dict[str, str]]): List of dictionaries of the form [{endpoint, name}].

    """

    def __init__(self, **kwds) -> None:
        # sourcery skip: replace-interpolation-with-fstring
        from .config import get_api_settings

        self.config: APISettings = get_api_settings()
        super().__init__(debug=self.config.debug, title=self.config.title, **kwds)
        self.jinja_global_vars: dict[str, Callable] = (
            self.config.jinja_global_vars or {}
        )
        self.jinja_filters: dict[str, Callable] = self.config.jinja_filters or {}
        self.startup()

    def startup(self) -> None:
        self.__register_routers()
        self.__add_static()
        self.__add_templates()
        self.__add_jinja_global_vars()
        self.__add_jinja_filters()
        log.info('UnRegistered Routers: \n%s' % pformat(self.unregistered_routers))
        log.info('Registered Routers: \n%s' % pformat(self.registered_routers))
        self.__add_cors()        

    @property
    def unregistered_routers(self) -> List[APIRouter]:
        """
        List[APIRouter]: Returns a list of all the (unregistered) routers in module routers.
        """
        from . import routers

        return [
            getattr(routers, router_name)
            for router_name in routers.__dir__()
            if isinstance(getattr(routers, router_name), APIRouter)
        ]

    @property
    def registered_routers(self) -> list[dict[str, str]]:
        """
        List of dictionaries of all the registered routes in the app.
        This list of routers will passed into the global jinja variables, in
        order to have the navbar macro in every page.
        Returns:
            list[dict[str, str]]: List of dictionaries of the form [{endpoint, name}].
        """
        return [
            {"endpoint": route.name, "name": route.name.split("_index")[0]}
            for route in self.routes
            if isinstance(route, APIRoute) and route.name.endswith("_index")
        ]

    def __register_routers(self) -> None:
        """
        -------ROUTING CONFIGURATION-----------
        import and register(include) all routers
        """
        for router in self.unregistered_routers:
            self.include_router(router)

    def __add_static(self) -> None:
        """
        ---------STATIC CONFIGURATION-----------
        add static file(css,js,media) folder to the app
        """
        self.mount(
            "/static", StaticFiles(directory=self.config.STATIC_PATH), name="static"
        )

    def __add_templates(self) -> None:
        """
        ---------JINJA INITIALIZATION-----------
        Instantiate  jinja templates
        """
        self.state.templates = Jinja2Templates(directory=self.config.TEMPLATES_PATH)

    def __add_jinja_global_vars(self) -> None:
        """
        REGISTERS JINJA EXTERNAL GLOBAL VARS
        """
        self.state.templates.env.globals |= (
            dict(router_list=self.registered_routers) | self.jinja_global_vars
        )

    def __add_jinja_filters(self) -> None:
        """
        REGISTERS JINJA EXTERNAL FILTERS
        """
        self.state.templates.env.filters |= self.jinja_filters

    def __add_cors(self) -> None:
        """Add middleware for CORS"""
        self.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost", "https://localhost"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        log.info('Added CORS')