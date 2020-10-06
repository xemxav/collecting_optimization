from reference import *


class Place:

    def __init__(self, name, longitude, latitude):  # todo : ajouter exception si longitude pas des float
        self.name = name
        self.longitude = float(longitude)
        self.latitude = float(latitude)
        return

    def getCoordinateslalo(self):  # todo : verifier lequel openroute veut en premier
        return [self.latitude, self.longitude]

    def getCoordinateslola(self):  # todo : verifier lequel openroute veut en premier
        return [self.longitude, self.latitude]

    def setCoordinates(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude


class Inlet(Place):
    lat_header = ILA
    lon_header = ILO
    name_header = INLET

    def __str__(self):
        return f"Inlet {self.name} at {self.longitude},{self.latitude}"


class Outlet(Place):
    lat_header = OLA
    lon_header = OLO
    name_header = OUTLET

    def __str__(self):
        return f"Outlet {self.name} at {self.longitude},{self.latitude}"


class Client(Place):
    lat_header = CLA
    lon_header = CLO
    name_header = CNAME
    adr_header = CADR

    def __init__(self, name, longitude, latitude, adress):
        super().__init__(name, longitude, latitude)
        self.adress = adress

    def __str__(self):
        return f"Client {self.name} at {self.longitude},{self.latitude}"
