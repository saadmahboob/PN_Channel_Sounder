import numpy as np





def lla_to_ecef(lat, lon, alt):
    # Returns the ECEF (Earth Centered Earth Fixed) coordinates in meters
    # of the given latitude (lat), longitude (lon), and altitude (alt).
    # lat and lon must be in radians and alt must be in meters.
    
    rad = np.float64(6378137.0)        # Radius of the Earth (in meters)
    f = np.float64(1.0/298.257223563)  # Flattening factor WGS84 Model
    cosLat = np.cos(lat)
    sinLat = np.sin(lat)
    FF     = (1.0-f)**2 # Semi-minor radius
    C      = 1/np.sqrt(cosLat**2 + FF * sinLat**2)
    S      = C * FF

    x = (rad * C + alt)*cosLat * np.cos(lon)
    y = (rad * C + alt)*cosLat * np.sin(lon)
    z = (rad * S + alt)*sinLat

    return (x, y, z)


def cartesianDistance(lat1, lon1, alt1, lat2, lon2, alt2):
    # Determines the Cartesian distance between 2 points defined as
    # latitude, longitude, and altitude. Latitudes and longitudes are assumed
    # to be in degrees.
    (x1, y1, z1) = lla_to_ecef(lat1*np.pi/180.0, lon1*np.pi/180.0, alt1)
    (x2, y2, z2) = lla_to_ecef(lat2*np.pi/180.0, lon2*np.pi/180.0, alt2)
    return np.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)

def haversineDistance(lat1, lon1, lat2, lon2):
    # Determines the great circle distance between two points defined by
    # latitude and longitude coordinates on the surface of a sphere with the
    # average radius of the Earth.
    # Input:
    #   lat1 = latitude of the first point (deg)
    #   lon1 = longitude of the first point (deg)
    #   lat2 = latitude of the second point (deg)
    #   lon2 = longitude of the second point (deg)
    # 
    # Output:
    #  d = great circle distance between (lat1, lon1) and (lat2, lon2)
    #
    # reference: https://en.wikipedia.org/wiki/Haversine_formula
    
    # Average Earth radius
    R = 6371000.0 # (m)
    
    # Convert latitudes and longitudes to radians.
    lat1 *= np.pi/180.0
    lon1 *= np.pi/180.0
    lat2 *= np.pi/180.0
    lon2 *= np.pi/180.0
    
    # Haversine distance (m)
    d = 2.0*R*np.arcsin(np.sqrt(np.sin((lat2-lat1)/2.0)**2 + np.cos(lat1)*np.cos(lat2)*np.sin((lon2-lon1)/2.0)**2))
    return d


def elevationAngles(distance, height1, height2):
    # Returns the elevation angles from height1 to height2 and height2 to 
    # height1.
    # The zero of the elevation angle is taken to be the horizontal plane
    # between height1 and height2.
    # distance, height1, and height2 must all be the same unit of distance.
    # Angles are returned in degrees.
    
    if height1 >= height2:
        arg = (height1-height2)/distance
        
        theta1 = -np.arccos(arg)*180.0/np.pi
        theta2 = +np.arcsin(arg)*180.0/np.pi
    else:
        arg = (height2-height1)/distance
        
        theta1 = +np.arcsin(arg)*180.0/np.pi
        theta2 = -np.arccos(arg)*180.0/np.pi
        
    return (theta1, theta2)
        

























