import asyncio
from rnet import Impersonate, Client


async def main():
    # Build a client
    client = Client(impersonate=Impersonate.Firefox139)

    # Use the API you're already familiar with
    resp = await client.get("https://tls.peet.ws/api/all")
    
    # Print the response
    print(await resp.text())


if __name__ == "__main__":
    asyncio.run(main())