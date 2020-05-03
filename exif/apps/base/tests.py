# Create your tests here.
from django.test import TestCase
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3
# Create your tests here.

class TestGps(TestCase):

    def get_coordinates(self, info):
        for key in ['Latitude', 'Longitude']:
            if 'GPS'+key in info and 'GPS'+key+'Ref' in info:
                e = info['GPS'+key]
                ref = info['GPS'+key+'Ref']
                info[key] = ( str(e[0][0]/e[0][1]) + '°' +
                              str(e[1][0]/e[1][1]) + '′' +
                              str(e[2][0]/e[2][1]) + '″ ' +
                              ref )

        if 'Latitude' in info and 'Longitude' in info:
            print([info['Latitude'], info['Longitude']])
        else:
            print('no gs info')

    def test_picture_(self):
        image2 = Image.open("./test1.jpg")
        exif = image2._getexif()
        if exif is not None:
            for key, value in exif.items():
                name = TAGS.get(key, key)
                exif[name] = exif.pop(key)

                if 'GPSInfo' in exif:
                    for key in exif['GPSInfo'].keys():
                        name = GPSTAGS.get(key,key)
                        exif['GPSInfo'][name] = exif['GPSInfo'].pop(key)
            info = exif['GPSInfo']
            print(info)
            for key in ['Latitude', 'Longitude']:
                if 'GPS'+key in info and 'GPS'+key+'Ref' in info:
                    e = info['GPS'+key]
                    ref = info['GPS'+key+'Ref']
                    info[key] = ( e[0][0]/e[0][1] +
                                  e[1][0]/e[1][1] / 60 +
                                  e[2][0]/e[2][1] / 3600
                                ) * (-1 if ref in ['S','W'] else 1)

            if 'Latitude' in info and 'Longitude' in info:
                coord = [info['Latitude'],info['Longitude']]
                print('coord',coord , type(coord), type(coord[0]), type(coord[1]))
                return self.get_coordonate(coord)

    def get_coordonate(self, coord):
        geolocator = Nominatim()
        print(coord)
        location = geolocator.geocode(coord)
        print(location.raw)