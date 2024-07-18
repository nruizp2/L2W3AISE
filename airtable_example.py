import os
from dotenv import load_dotenv, find_dotenv
from pyairtable import Api

load_dotenv(find_dotenv())
airtable_api_key = os.getenv("AIRTABLE_API_KEY")

api = Api(airtable_api_key)
table = api.table('appUZQbUwuCLJjRqW', 'tblGxB1JlkiMhSmD7')
print(table.all())
