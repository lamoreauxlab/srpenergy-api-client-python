from datetime import datetime, timedelta
import os

from dotenv import load_dotenv

from srpenergy.client import SrpEnergyClient

# Load environment variables from .env file
load_dotenv()

# Read values from environment
accountid = os.getenv("SRP_BILLING_ACCOUNT")
username = os.getenv("SRP_USER_NAME")
password = os.getenv("SRP_PASSWORD")

# Optional: fail fast if something is missing
if not all([accountid, username, password]):
    raise ValueError("Missing one or more required environment variables.")

end_date = datetime.now()
start_date = datetime.now() - timedelta(days=2)

client = SrpEnergyClient(accountid, username, password)
usage = client.usage(start_date, end_date)

date, hour, isodate, kwh, cost = usage[0]

print(f"Date: {date}, Hour: {hour}, ISO: {isodate}, kWh: {kwh}, Cost: {cost}")
