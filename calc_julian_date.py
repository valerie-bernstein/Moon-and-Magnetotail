
def calc_julian_date(year, month, day, hour):
    #function to return the julian date
    #conversion formula from: http://aa.usno.navy.mil/faq/docs/JD_Formula.php
    julian_day = 367*year - int((7*(year+int((month+9.)/12.)))/4.) + int((275*month)/9.) + day + 1721013.5 + hour/24. 
    return julian_day

