import numpy as np
from z_rotation_matrix import z_rotation_matrix
from x_rotation_matrix import x_rotation_matrix
from calc_julian_date import calc_julian_date

def GEItoGSE(RA, dec, distance, year, month, day, hour):
    #function to convert from RA, dec, and Earth-moon distance to GSE coordinates for a given time 
    #RA and dec should be in radians
    #returns vector of shape (3,1)
    
    JD = calc_julian_date(year, month, day, 0) #integer part, the value at 00:00UT on the day of interest
    T_0 = (JD - 2451545)/36525. #time in Julian centuries from 12:00UT Jan. 1, 2000 (epoch J2000)
    epsilon = 23.439 - 0.013*T_0 #obliquity of the ecliptic
    
    UT = hour #time within the day as Universal time in hours
    M = 357.528 + 35999.050*T_0 + 0.04107*UT #Sun's mean anomaly
    A = 280.460 + 36000.772*T_0 + 0.04107*UT #Sun's mean longitude
    lambda_sun = A + (1.915-0.0048*T_0)*np.sin(np.radians(M)) + 0.020*np.sin(np.radians(2*M)) #sun's ecliptic longitude
    
    T = np.matmul(z_rotation_matrix(np.radians(lambda_sun)), x_rotation_matrix(np.radians(epsilon))) #transformation matrix
    
    R = distance #radial distance between earth and moon, km
    x_GEI = R*np.cos(dec)*np.cos(RA) #get GEI in cartesian components
    y_GEI = R*np.cos(dec)*np.sin(RA)
    z_GEI = R*np.sin(dec)
    GEI = np.array([[x_GEI], [y_GEI], [z_GEI]])
    
    GSE = np.dot(T, GEI) #apply the rotations to convert GEI to GSE

    return GSE

