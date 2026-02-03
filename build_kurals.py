import requests
import json
import time

API = "https://api-thirukkural.vercel.app/api?num="

kurals = {}

for i in range(1, 1331):
    try:
        r = requests.get(API + str(i), timeout=10)
        data = r.json()

        kurals[str(i)] = {
            "ta": data["line1"] + " " + data["line2"],
            "en": data["trans"]
        }

        print("Saved", i)
        time.sleep(0.3)

    except Exception as e:
        print("Failed:", i, e)

with open("kurals.json", "w", encoding="utf-8") as f:
    json.dump(kurals, f, ensure_ascii=False, indent=2)

print("DONE")
