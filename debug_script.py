import asyncio
import logging
import os
import ssl

from aiohttp import (
    ClientError,
    ClientSession,
    TCPConnector,
    client_exceptions,
    http_exceptions,
)

# from srpenergy.client import SrpEnergyClient
from async_timeout import timeout
import certifi
from dotenv import load_dotenv

_LOGGER = logging.getLogger(__name__)

BASE_USAGE_URL = "https://myaccount.srpnet.com/myaccountapi/api/"


async def main():
    load_dotenv("local.env")

    sslcontext = ssl.create_default_context(cafile=certifi.where())
    async with timeout(10):
        async with ClientSession(connector=TCPConnector(ssl=sslcontext)) as session:
            username = os.environ.get("SRP_USER_NAME")
            password = os.environ.get("SRP_PASSWORD")

            try:
                url = f"{BASE_USAGE_URL}login/authorize"
                response = await session.post(
                    url=url, data={"username": username, "password": password}
                )
                print(response.status)
                response.raise_for_status()
                data = await response.json()
                valid = data["message"] == "Log in successful."
                print(valid)

            except (ClientError, http_exceptions.HttpProcessingError) as ex:
                _LOGGER.error("aiohttp exception for %s %s", url, ex)
            else:
                # soup = BeautifulSoup(response, "html.parser")
                # month_links = get_month_links(soup, year, month)
                # return month_links
                return False


if __name__ == "__main__":
    asyncio.run(main())
