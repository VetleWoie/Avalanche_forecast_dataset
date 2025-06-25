import http
from time import sleep
from typing import List
import requests
from pydantic import TypeAdapter, type_adapter, FilePath
from datetime import datetime
import logging
import os
from tqdm import tqdm
import pytz
from urllib3.exceptions import ProtocolError

from models import AvaForecastDetailed
from regions import getRegions

def get_forecasts(
        regionIDs: List[int] | None = None, 
        from_date: datetime = None,
        to_date: datetime = None,
        out_dir : FilePath = "./",
        language_id : int = 1
        ):
    
    """
    Gets the avalanche forecasts for some specified regions within a
    specified time period, and writes them to a folder.

    @Params
    regionIDs: List[int] - List of regions to fetch forecasts from if not
                           specified all regions are used.

    from_date: datetime - Earliest date to fetch data from, if not 
                          specified earliest forecast for region will be used.

                          TODO: Currently only the year will be used, should check days aswell

    to_date: datetime - Latest date to fetch data from, if not specified
                        today will be used.

                        TODO: Currently only the year will be used, should check days aswell

    out_dir: FilePath - Path to write datafolder, will create if it does not exist.
    """


    url = "https://api01.nve.no/hydrology/forecast/avalanche/v6.3.0/api/AvalancheWarningByRegion/Detail/{region_id}/{language_id}/{from_date}/{to_date}"

    print(regionIDs)
    regions = getRegions()
    if regionIDs is None:
        regionIDs = [region.Id for region in regions]
    else:
        regions = [region for region in regions if region.Id in regionIDs]

    os.makedirs(f"{out_dir}",exist_ok=True)
    for region in tqdm(regions):
        logging.info(f"Fetching forecasts from {region.Name}")
        region.ValidFrom = region.ValidFrom.replace(tzinfo=None)
        region.ValidTo = region.ValidTo.replace(tzinfo=None)
        if from_date is not None:
            if region.ValidTo < from_date:
                logging.INFO(f"No forecasts from region {region.Id} in the specified timeframe, from date: {from_date} valid to: {region.ValidTo}")
                continue
            from_day = from_date
        else:
            from_day = region.ValidFrom

        if to_date is not None:
            if region.ValidFrom > to_date:
                logging.INFO(f"No forecasts from region {region.Id} in the specified timeframe, to date: {to_date} valid from: {region.ValidFrom}")
                continue
            to_day = to_date
        else:
            to_day = region.ValidTo

        
        for year in range(from_day.year, to_day.year):
            #The forecast is only available from December 1st to June 1st
            start = datetime(year,12,1) #Todo: Fix more precise todate dates
            end = datetime(year+1, 6,1)

            fetch_success = False
            while not fetch_success:
                try:
                    fetch_success = True
                    res = requests.get(
                        url=url.format(region_id = region.Id, language_id = language_id, from_date = start.date(), to_date = end.date() )
                    )
                    if res.status_code != 200:
                        logging.error(f"Error when fetching forecast from {region.Name} season {year}-{year+1}: {res.status_code} - {res.text}")
                        continue
                    forecasts = TypeAdapter(List[AvaForecastDetailed]).validate_json(res.text)

                    #Check wether there were any forecasts this season
                    tot = len(forecasts)
                    forecasts = [forecast for forecast in filter(lambda x: x.DangerLevel != 0, forecasts)]
                    actuall = len(forecasts)
                    if actuall == 0:
                        logging.info(f"Found {actuall} forecasts for region {region.Name} season {year}-{year+1}")
                        continue
                    
                    #Write forecasts to file
                    logging.info(f"Writing {region.Name} season {year} - {year+1}:\n\t Found {actuall} number of forcasts out of {tot} days")
                    os.makedirs(f"{out_dir}/{region.Name}",exist_ok=True)

                    with open(f"{out_dir}/{region.Name}/season_{year}_{year+1}",'w') as out:
                        out.write(TypeAdapter(List[AvaForecastDetailed]).dump_json(forecasts, indent=2).decode())
                    
                except http.client.RemoteDisconnected:
                    logging.info("Remote disconnected, trying again in 10 minutes")
                    sleep(10*60)
                    fetch_success = False


if __name__ == "__main__":
    logging.basicConfig(filename='/tmp/avalanche_forecast_fetch.log', filemode='w', level=logging.INFO)
    get_forecasts(out_dir="./forecasts",regionIDs=[i for i in range(3000,3047)], from_date=datetime(2017, 1,1))