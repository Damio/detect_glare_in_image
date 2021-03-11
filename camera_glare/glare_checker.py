import astropy.coordinates as coord
from astropy.time import Time
import astropy.units as u


class GlareCheck:
    """
    This class consists of a method to calculate the relative azimuth and Altitude 
    of the sun, given the
        - “lat”: a float between -90 to 90 that shows the latitude in which the image was taken
        - “lon”: a float between -180 to 180 that shows the longitude in which the image was taken
        - “epoch”: Linux epoch in second
        - “orientation”: a float between -180 to 180 the east-ward orientation of car travel 
        from true north. 0 means north. 90 is east and -90 is west
    This can be expanded to accomodate different methods
    to calculate azimuth and altitute. possibly to compare
    the different methods.
    """
    
    def __init__(self, lat, lon, epoch, orientation):
        self.lat = lat
        self.lon = lon
        self.epoch = epoch
        self.orientation = orientation

    def altittude_azimuth(self):
        # can add heihght parameter for more acurate result height= x * u.m
        loc = coord.EarthLocation(lon=self.lon * u.deg,
                          lat=self.lat * u.deg)
        
        # convert to astropy time format
        time = Time(self.epoch, format='unix')
        # get the altitude and azimuth
        altaz = coord.AltAz(location=loc, obstime=time)
        sun = coord.get_sun(time)
        az = sun.transform_to(altaz).az.deg
        alt = sun.transform_to(altaz).alt.deg

        # get the relative azimuth for the car,
        # i.e compensate for the car's orientation
        #################################
        # convert from 0to360 into -180to180
        az = (az + 180) % 360 - 180
        #needs more work
        relative_az = abs(self.orientation - az)
        ##################################
        # return the azimuth and altitude
        return relative_az, alt
