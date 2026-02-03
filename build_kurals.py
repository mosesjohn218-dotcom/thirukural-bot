import requests
import json

API = "https://api-thirukkural.vercel.app/api?num="

kurals = {}

for i in range(1, 1331):
    print("Fetching", i)
    r = requests.get(API + str(i)).json()

    kurals[str(i)] = {
        "ta": r["line1"] + " " + r["line2"],
        "en": r["trans"]
    }

with open("kurals.json", "w", encoding="utf-8") as f:
    json.dump(kurals, f, ensure_ascii=False)

print("Done! kurals.json created")
