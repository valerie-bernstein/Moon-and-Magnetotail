import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import ephem
import sys
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Circle, PathPatch
import mpl_toolkits.mplot3d.art3d as art3d
from GEItoGSE import GEItoGSE
from find_full_moons import find_full_moons

def main(start_date, end_date):
    #start_date is a datetime object
    #end_date is a datetime object

    #create an array of dates for the analysis, with a cadence of 1 hour
    dates = []
    while start_date <= end_date:
        dates.append(start_date)
        start_date += dt.timedelta(hours=1)

    dates = np.array(dates)

    moon_phase = []
    moon_ra = [] #radians
    moon_dec = [] #radians
    moon_dist = [] #km
    moon_GSE = np.zeros((3,len(dates)))
    for date, i in zip(dates, range(len(dates))): #loop through the dates and compute the phase and position information for the moon 
        m = ephem.Moon(date)
        moon_phase.append(m.moon_phase)
        m_ra = float(repr(m.ra)) #to get in radians
        moon_ra.append(m_ra)
        m_dec = float(repr(m.dec)) #to get in radians
        moon_dec.append(m_dec)
        distance = m.earth_distance * 1.495978707e8 #km
        moon_dist.append(distance)
    
        GSE_coords = GEItoGSE(m_ra, m_dec, distance, date.year, date.month, date.day, (date.hour+(date.minute/60.))) 
        moon_GSE[:,i] = GSE_coords.reshape(3)

    moon_phase = np.array(moon_phase)*100 #percentage
    full_moon_indices = find_full_moons(dates, moon_phase) #get indices of the full moons


    #make the moon phase plot
    plt.rcParams.update({'font.size': 16})
    fig,ax = plt.subplots(figsize=(20,8))
    ax.plot(dates, moon_phase)
    counter = 0
    for idx in full_moon_indices:
        counter += 1
        if counter == 1:
            ax.plot(dates[(idx-72):(idx+73)], moon_phase[(idx-72):(idx+73)], c='red', label='Magnetotail') #highlight 6 days around the full moon time, since the moon spends ~6 days inside the magnetotail
        else:
            ax.plot(dates[(idx-72):(idx+73)], moon_phase[(idx-72):(idx+73)], c='red')
    ax.set_title('Moon Phase over Time (100% = Full Moon)')
    ax.set_xlabel('Date (Year-Month)')
    ax.set_ylabel('% of Surface Illuminated')
    plt.legend(loc='best')
    plt.show()


    #make the moon orbit plot
    plt.rcParams.update({'font.size': 16})

    R = 30 * 6378 #km #radius of the magnetotail
    R_bow = 50 * 6378 #km #radius of the bowshock
    n = -60 * 6378 #km #approximate moon orbit
    Vsw = 400 #km/s #approximate average velocity of the solar wind
    deltaY= np.abs(moon_GSE[0,:])*(29/Vsw) #compute aberration in the +y direction

    idx_tail = []
    idx_bow = []
    for k in range(len(moon_GSE[0,:])):
        if moon_GSE[0,k] < 0:
            p = Circle((0+deltaY[k], 0), R, fill=None) #magnetotail circle
            p_bow = Circle((0+deltaY[k], 0), R_bow, fill=None)
            yz_coords = (moon_GSE[1,k], moon_GSE[2,k]) #tuple
        
            #check if (y,z) is contained in the magnetotail circle
            if p.contains_point(yz_coords):
                idx_tail.append(k)
            
            if p_bow.contains_point(yz_coords):
                idx_bow.append(k)

    idx_tail_arr = np.array(idx_tail)
    idx_bow_arr = np.array(idx_bow)
    fig= plt.figure(figsize=(15,15))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(moon_GSE[0,:], moon_GSE[1,:], moon_GSE[2,:], '.', c='C0')
    ax.plot(moon_GSE[0,idx_bow_arr-(3*24)], moon_GSE[1,idx_bow_arr-(3*24)], moon_GSE[2,idx_bow_arr-(3*24)], '.', c='violet')
    ax.plot(moon_GSE[0,idx_bow], moon_GSE[1,idx_bow], moon_GSE[2,idx_bow], '.', c='gold')
    ax.plot(moon_GSE[0,idx_tail], moon_GSE[1,idx_tail], moon_GSE[2,idx_tail], '.', c='red')
    ax.scatter(0,0,0, c = "b") #represent Earth's location
    ax.set_xlabel(r'GSE$_x$ (km)', labelpad=40)
    ax.set_ylabel(r'GSE$_y$ (km)', labelpad=40)
    ax.set_zlabel(r'GSE$_z$ (km)', labelpad=40)
    ax.ticklabel_format(axis='x', style='sci', scilimits=(0,0))
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.ticklabel_format(axis='z', style='sci', scilimits=(0,0))
    ax.set_title("Moon Position")
    ax.set_ylim(-400000, 400000)
    ax.set_zlim(-400000, 400000)

    #create a representative circle to visualize the bounds of the magnetotail (not including a delta_y component)
    p = Circle((0, 0), R, fill=None)
    ax.add_patch(p)
    art3d.pathpatch_2d_to_3d(p, z=n, zdir="x")

    #create a representative circle to visualize the bounds of the bow shock (not including a delta_y component)
    p_bow = Circle((0, 0), R_bow, fill=None)
    ax.add_patch(p_bow)
    art3d.pathpatch_2d_to_3d(p_bow, z=n, zdir="x")

    plt.show()



    #make the moon orbit plot viewed from a different rotation angle
    plt.rcParams.update({'font.size': 12})

    moon_GSE_RE = np.zeros((3,len(dates)))
    moon_GSE_RE[0,:] = moon_GSE[0,:] / 6378. #in units of earth radii
    moon_GSE_RE[1,:] = moon_GSE[1,:] / 6378. #in units of earth radii
    moon_GSE_RE[2,:] = moon_GSE[2,:] / 6378. #in units of earth radii

    R = 30 #earth radii #radius of the magnetotail
    R_bow = 50 #earth radii #radius of the bowshock
    n = -60 #earth radii #approximate moon orbit
    Vsw = 400. / (6378.) #R_E/s
    deltaY= np.abs(moon_GSE_RE[0,:])*(29/Vsw) #compute aberration in the +y direction


    fig= plt.figure(figsize=(12,12))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(moon_GSE_RE[0,:], moon_GSE_RE[1,:], moon_GSE_RE[2,:], '.', c='C0')
    ax.plot(moon_GSE_RE[0,idx_bow], moon_GSE_RE[1,idx_bow], moon_GSE_RE[2,idx_bow], '.', c='gold')
    ax.plot(moon_GSE_RE[0,idx_tail], moon_GSE_RE[1,idx_tail], moon_GSE_RE[2,idx_tail], '.', c='red')
    ax.scatter(0,0,0, c = "b") #represent Earth's location
    ax.set_xlabel(r'X ($R_E$)', labelpad=20)
    #ax.set_ylabel(r'Y ($R_E$)', labelpad=20)
    ax.set_zlabel(r'Z ($R_E$)', labelpad=20)
    #ax.ticklabel_format(axis='x', style='sci', scilimits=(0,0))
    #ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    #ax.ticklabel_format(axis='z', style='sci', scilimits=(0,0))
    ax.set_title("Moon Position")
    ax.set_ylim(-400000/6378., 400000/6378.)
    ax.set_zlim(-400000/6378., 400000/6378.)
    ax.yaxis.set_tick_params(
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False) # labels along the bottom edge are off


    #create a representative circle to visualize the bounds of the magnetotail (not including a delta_y component)
    p = Circle((0, 0), R, fill=None)
    ax.add_patch(p)
    art3d.pathpatch_2d_to_3d(p, z=n, zdir="x")

    #create a representative circle to visualize the bounds of the bow shock (not including a delta_y component)
    p_bow = Circle((0, 0), R_bow, fill=None)
    ax.add_patch(p_bow)
    art3d.pathpatch_2d_to_3d(p_bow, z=n, zdir="x")

    # Get current rotation angle
    #print(ax.azim) #default is -60

    # Set rotation angle to 30 degrees
    ax.view_init(azim=90)

    plt.show()


    #find indices where the moon enters/exits the 3-day window, bow shock, and magnetotail in order to make the tables

    idx_tail_arr = np.array(idx_tail) #indices in the dates array where the moon is inside the magnetotail
    idx_bow_arr = np.array(idx_bow) #indices in the dates array where the moon is inside the bowshock
    idx_3day_tail = idx_tail_arr - (3*24) #magnetotail indices are shifted to 3 days earlier
    idx_3day_bow = idx_bow_arr - (3*24) #bowshock indices are shifted to 3 days earlier


    idx_3day_bow_start = [idx_3day_bow[0]] #this is a list of indices where 3 days before the bowshock starts ('no' times)
    for i in range(len(idx_3day_bow)-1):
        if (idx_3day_bow[i+1] - idx_3day_bow[i]) > 1:
            idx_3day_bow_start.append(idx_3day_bow[i+1])

    idx_bow_start = [idx_bow_arr[0]] #this is a list of indices where the bowshock starts
    idx_bow_ends = [0] #this is a list of indices where the bowshock ends ('yes' times)
    for i in range(len(idx_bow_arr)-1):
        if (idx_bow_arr[i+1] - idx_bow_arr[i]) > 1:
            idx_bow_start.append(idx_bow_arr[i+1])
            idx_bow_ends.append(idx_bow_arr[i])
        
    idx_3day_tail_start = [idx_3day_tail[0]] #this is a list of indices where 3 days before the magnetotail starts ('no' times)
    for i in range(len(idx_3day_tail)-1):
        if (idx_3day_tail[i+1] - idx_3day_tail[i]) > 1:
            idx_3day_tail_start.append(idx_3day_tail[i+1])

    idx_tail_start = [idx_tail_arr[0]] #this is a list of indices where the magnetotail starts
    idx_tail_ends = [0] #this is a list of indices where the magnetotail ends ('yes' times)
    for i in range(len(idx_tail_arr)-1):
        if (idx_tail_arr[i+1] - idx_tail_arr[i]) > 1:
            idx_tail_start.append(idx_tail_arr[i+1])
            idx_tail_ends.append(idx_tail_arr[i])
        
        
    #table 1: avoid the bowshock
    print('Table 1 no dates: ', dates[idx_3day_bow_start])
    print('Table 1 yes dates: ', dates[idx_bow_ends])

    #table 2: avoid the magnetotail
    print('Table 2 no dates: ', dates[idx_3day_tail_start])
    print('Table 2 yes dates: ', dates[idx_tail_ends])

    plt.rcParams.update({'font.size': 16})

    #plot of illuminance with additions
    fig,ax = plt.subplots(figsize=(20,8))
    ax.plot(dates, moon_phase)
    ax.plot(dates[idx_bow_arr-(3*24)], moon_phase[idx_bow_arr-(3*24)], '.', c='violet', label='3-day window before entering')
    ax.plot(dates[idx_bow_arr], moon_phase[idx_bow_arr], '.', c='gold', label='Bowshock')
    ax.plot(dates[idx_tail_arr], moon_phase[idx_tail_arr], '.', c='red', label='Magnetotail')
    ax.set_title('Moon Phase over Time (100% = Full Moon)')
    ax.set_xlabel('Date (Year-Month)')
    ax.set_ylabel('% of Surface Illuminated')
    plt.legend(loc='best')
    plt.show()

    #plot of illuminance zoomed-in on one month
    fig,ax = plt.subplots(figsize=(20,8))
    ax.plot(dates, moon_phase)
    ax.plot(dates[idx_bow_arr-(3*24)], moon_phase[idx_bow_arr-(3*24)], '.', c='violet', label='3-day window before entering')
    ax.plot(dates[idx_bow_arr], moon_phase[idx_bow_arr], '.', c='gold', label='Bowshock')
    ax.plot(dates[idx_tail_arr], moon_phase[idx_tail_arr], '.', c='red', label='Magnetotail')
    for idx_b in idx_3day_bow_start:
        ax.axvline(dates[idx_b], c='violet')
    for idx_b in idx_bow_start:
        ax.axvline(dates[idx_b], c='gold')
    for idx_b in idx_tail_start:
        ax.axvline(dates[idx_b], c='red')
    for idx_b in idx_tail_ends:
        ax.axvline(dates[idx_b], c='gold')
    for idx_b in idx_bow_ends:
        ax.axvline(dates[idx_b], c='C0')
    ax.set_title('Moon Phase, one month')
    ax.set_xlabel('Date (Year-Month-Day)')
    ax.set_ylabel('% of Surface Illuminated')
    plt.legend(loc='best')
    ax.set_xlim(dates[0], dates[0] + dt.timedelta(days=31))
    plt.show()


start_date_str = sys.argv[1]
end_date_str = sys.argv[2]
start_date = dt.datetime.strptime(start_date_str, '%b %d %Y')
end_date = dt.datetime.strptime(end_date_str, '%b %d %Y')
main(start_date, end_date)

