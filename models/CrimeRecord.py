class CrimeRecord:
    def __init__(self, crime_date, address, district, beat, grid,
                 crime_descr, ucr_ncic_code, latitude, longitude):
        self.crimeDate = crime_date
        self.address = address
        self.district = district
        self.beat = beat
        self.grid = grid
        self.crimeDescription = crime_descr
        self.code = ucr_ncic_code
        self.latitude = latitude
        self.longitude = longitude
