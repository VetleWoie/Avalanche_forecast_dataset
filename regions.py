from pydantic import TypeAdapter
import requests
from models import Region
import json
from typing import List


def getRegions() -> List[Region]:
    url = "https://api01.nve.no/hydrology/forecast/avalanche/v6.3.0/api/Archive/Region/json"
    res = requests.get(url)
    
    regions = TypeAdapter(List[Region]).validate_json(res.text)

    return regions

if __name__ == "__main__":
    regions = getRegions()
    print(TypeAdapter(List[Region]).dump_json(regions, indent=2).decode())
