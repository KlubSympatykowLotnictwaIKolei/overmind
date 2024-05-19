from src.overmind import Overmind
import asyncio

if __name__ == "__main__":
    overmind = Overmind()
    asyncio.run(overmind.think())