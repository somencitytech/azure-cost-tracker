import requests, os, json, datetime

token_url = f"https://login.microsoftonline.com/{os.getenv('TENANT_ID')}/oauth2/token"
data = {
  "grant_type": "client_credentials",
  "client_id": os.getenv("CLIENT_ID"),
  "client_secret": os.getenv("CLIENT_SECRET"),
  "resource": "https://management.azure.com/"
}
token = requests.post(token_url, data=data).json()["access_token"]

now = datetime.date.today()
start = now.replace(day=1).isoformat()
end = now.isoformat()

url = f"https://management.azure.com/subscriptions/{os.getenv('SUBSCRIPTION_ID')}/providers/Microsoft.CostManagement/query?api-version=2023-03-01"
headers = {"Authorization": f"Bearer {token}"}
query = {
  "type": "ActualCost",
  "timeframe": "MonthToDate",
  "timePeriod": {"from": start, "to": end},
  "dataset": {
    "granularity": "Daily",
    "aggregation": {"totalCost": {"name": "PreTaxCost", "function": "Sum"}},
    "grouping": [{"type": "Dimension", "name": "ResourceGroupName"}]
  }
}
resp = requests.post(url, headers=headers, json=query).json()

with open("cost_data.json", "w") as f:
    json.dump(resp["properties"]["rows"], f)
