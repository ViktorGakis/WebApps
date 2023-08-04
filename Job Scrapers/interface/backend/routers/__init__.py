'''Routes'''
# the import route order is kept also at register level
from .main import router as main
from .seeker import router as seeker
from .collector import router as collector
from .locator import router as locator
from .jobs import router as jobs