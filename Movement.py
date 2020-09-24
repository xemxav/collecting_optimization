import datetime
from reference import *

class Place:

    def __init__(self, name, longitude, latitude):  # todo : ajouter exception si longitude pas des float
        self.name = name
        self.longitude = float(longitude)
        self.latitude = float(latitude)
        return

    def getCoordinates(self):
        return self.longitude, self.latitude

    def setCoordinates(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude


class Inlet(Place):
    lat_header = CLA
    lon_header = CLO
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

class High_up(Place):
    pass

class Tour:

    def __init__(self, id, inlet, outlet, driver="", material="", licence_plate="", clients=None,
                 date=""):  # todo : changer date defaut + verifier que isinstance pour inlet / outlet
        self.id = id
        self.inlet = inlet
        self.outlet = outlet
        self.driver = driver
        self.material = material
        self.licence_plate = licence_plate
        if clients == None:
            self.clients = list()
        else:
            self.clients = clients
        self.date = date
        self.distance = 0
        self.duration = 0
        self.high_up1 = None
        self.high_up2 = None
        return

    def addClient(self, client):
        self.clients.append(client)

    def get_distance_highups(self):
        pass

    def get_duration_highups(self):
        pass

    def __str__(self):
        #todo : ajoutet check sur presence données
        str = f"ID = {self.id}\n" \
              f"Inlet = {self.inlet.name}\n" \
              f"Outlet = {self.outlet.name}\n" \
              f"Nombre de clients = {len(self.clients)}\n"
        return str

class Network:

    def __init__(self, inlets=None, outlets=None, clients=None):
        self.inlets = list()
        if isinstance(inlets, list):
            self.inlets = inlets
        elif isinstance(inlets, Inlet):
            self.inlets.append(inlets)

        self.outlets = list()
        if isinstance(outlets, list):
            self.outlets = outlets
        elif isinstance(outlets, Outlet):
            self.outlets.append(outlets)

        self.clients = list()
        if isinstance(clients, list):
            self.clients = clients
        elif isinstance(clients, Client):
            self.clients.append(clients)
        self.tours = list()

    def __str__(self):
        str = ""
        for tour in self.tours:
            str = str + tour.__str__() + "\n"
        return str

    def clientInNetwork(self, client=None, client_name=""):
        if client == None and client_name != "":
            for c in self.clients:
                if c.name == client_name:
                    return True
            return False
        elif client != None and client in self.clients:
            return True
        return False

    def inletInNnetwork(self, inlet=None, inlet_name=""):
        if inlet == None and inlet_name != "":
            for i in self.inlets:
                if i.name == inlet_name:
                    return True
            return False
        elif inlet != None and inlet in self.inlets:
            return True
        return False

    def outletInNnetwork(self, outlet=None, outlet_name=""):
        if outlet == None and outlet_name != "":
            for o in self.outlets:
                if o.name == outlet_name:
                    return True
            return False
        elif outlet != None and outlet in self.outlets:
            return True
        return False

    def getClient(self, client_name):
        for c in self.clients:
            if c.name == client_name:
                return c
        return None

    def getInlet(self, inlet_name=""):
        for i in self.inlets:
            if i.name == inlet_name:
                return i
        return None

    def getOutlet(self, outlet_name=""):
        for o in self.outlets:
            if o.name == outlet_name:
                return o
        return None

    def addClient(self, client):
        self.clients.append(client)

    def addInlet(self, inlet):
        self.inlets.append(inlet)

    def addOutlet(self, outlet):
        self.outlets.append(outlet)

    def addTour(self, tour):
        self.tours.append(tour)

    def getTourById(self, id):
        for tour in self.tours:
            if tour.id == id:
                return tour
        return None
