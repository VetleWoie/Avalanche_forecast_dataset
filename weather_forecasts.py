import xarray as xr
import numpy as np
from pathlib import Path

def extract_meps_forecast_at_location(
    meps_file_path: str,
    lat_target: float,
    lon_target: float,
    variables: list = None,
) -> dict:
    """
    Extract weather forecast time series at a given location from a MEPS NetCDF file.

    Parameters:
        meps_file_path (str): Path to the .nc or .ncml file (e.g., meps_det_sfc_20250210T06Z.nc)
        lat_target (float): Latitude of the location (in degrees)
        lon_target (float): Longitude of the location (in degrees)
        variables (list): Optional list of variable names to extract

    Returns:
        dict: Dictionary mapping variable name to time series (numpy arrays)
    """
    ds = xr.open_dataset(meps_file_path, engine="netcdf4")

    # Find the closest grid point
    lat = ds.latitude
    lon = ds.longitude

    abs_diff_lat = np.abs(lat - lat_target)
    abs_diff_lon = np.abs(lon - lon_target)
    total_diff = abs_diff_lat + abs_diff_lon
    idx = np.unravel_index(np.argmin(total_diff), lat.shape)

    # Select default variables if none specified
    if variables is None:
        variables = [
            "air_temperature_2m",
            "wind_speed_10m",
            "precipitation_amount",
            "wind_from_direction_10m"
        ]

    # Extract time series at the closest grid point
    forecast_data = {}
    for var in variables:
        if var in ds.variables:
            data = ds[var].isel(x=idx[1], y=idx[0])  # Adjust for coordinate order
            forecast_data[var] = data.values
        else:
            print(f"⚠️ Variable '{var}' not found in dataset")

    # Optionally extract forecast times too
    if "time" in ds.coords:
        forecast_data["time"] = ds["time"].values

    ds.close()
    return forecast_data


if __name__=="__main__":
    forecast = extract_meps_forecast_at_location(
    meps_file_path="dods://thredds.met.no/thredds/dodsC/meps25epsarchive/2025/06/12/meps_det_sfc_20250612T18Z.ncml",
    lat_target=61.28,
    lon_target=7.80,
)

    for var, values in forecast.items():
        print(f"{var}: {values[:5]}")