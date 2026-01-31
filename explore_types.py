#!/usr/bin/env python3
import requests

# Fetch a sample of Met objects to see what classifications exist
base_url = "https://collectionapi.metmuseum.org/public/collection/v1"
response = requests.get(f"{base_url}/search", params={"hasImages": "true", "q": "art"}, timeout=30)
object_ids = response.json().get("objectIDs", [])[:30]

classifications = set()
object_types = set()
for obj_id in object_ids:
    try:
        obj_response = requests.get(f"{base_url}/objects/{obj_id}", timeout=30)
        data = obj_response.json()
        if data.get("classification"):
            classifications.add(data["classification"])
        if data.get("objectName"):
            object_types.add(data["objectName"])
    except:
        pass

print("Met Museum Classifications:")
for c in sorted(classifications):
    print(f"  - {c}")

print("\nMet Museum Object Types:")
for t in sorted(object_types):
    print(f"  - {t}")
