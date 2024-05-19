from api.frontend_api import FrontendApi
from src.overmind import Overmind
import asyncio

if __name__ == "__main__":
    overmind = Overmind()
    asyncio.run(overmind.think())
    frontend_api = FrontendApi()