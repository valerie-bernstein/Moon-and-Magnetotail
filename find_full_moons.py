import numpy as np
import datetime as dt

def find_full_moons(dates, moon_phases):
    #function to find indices of full moon times
    #dates input is an array of datetime objects
    #moon_phases input is an array of moon surface illumination percentages
    start_date = dates[0]
    end_date = dates[-1]
    full_moon_indices = []
    while start_date <= end_date:
        end_date_local = start_date + dt.timedelta(days=30) #loop through every 30 days, or approximately every month, to find the full moon of that month
        interval_idx = [idx for idx in range(len(dates)) if dates[idx] >= start_date and dates[idx] <= end_date_local]
        
        phase_interval = moon_phases[interval_idx[0]:interval_idx[-1]+1]
        full_moon_value = max(phase_interval)
        full_moon_index = np.where(moon_phases == full_moon_value)[0][0]
        full_moon_indices.append(full_moon_index)
        
        start_date += dt.timedelta(days=30)
        
    return(full_moon_indices)
