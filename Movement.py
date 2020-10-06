import datetime
from reference import *
import openrouteservice
import folium

class Place:

    def __init__(self, name, longitude, latitude):  # todo : ajouter exception si longitude pas des float
        self.name = name
        self.longitude = float(longitude)
        self.latitude = float(latitude)
        return

    def getCoordinateslalo(self): #todo : verifier lequel openroute veut en premier
        return [self.latitude, self.longitude]

    def getCoordinateslola(self): #todo : verifier lequel openroute veut en premier
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


class High_up(Place):
    pass

class Tour:

    def __init__(self, id, inlet, outlet, date, driver="", material="", licence_plate="", clients=None):  # todo : changer date defaut + verifier que isinstance pour inlet / outlet
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
        self.matrix = None
        return

    def addClient(self, client):
        self.clients.append(client)

    def get_distance_highups(self):
        pass

    def get_duration_highups(self):
        pass

    def getClientsCoord(self):
        coord = list()
        for c in self.clients:
            coord.append(c.getCoordinates())
        return coord

    def getAllCoord(self):
        coord = list()
        coord.append(self.inlet.getCoordinateslola())
        for c in self.clients:
            coord.append(c.getCoordinateslola())
        coord.append(self.outlet.getCoordinateslola())
        return coord

    def __str__(self):
        #todo : ajoutet check sur presence données
        str = f"ID = {self.id}\n" \
              f"Date = {self.date.strftime('%d/%m/%Y')}\n" \
              f"Inlet = {self.inlet.name}\n" \
              f"Outlet = {self.outlet.name}\n" \
              f"Nombre de clients = {len(self.clients)}\n"
        return str

    def calculateMatrix(self, client, dry_rune=False):
        coords = self.getAllCoord()
        print("len : ", len(coords), "coords:", coords)
        destinations = [i + 1 for i,v in enumerate(coords[1:])]
        print("destinations:", destinations)
        matrix = client.distance_matrix(
            locations=coords,
            sources=[0,],
            destinations=destinations,
            profile='driving-hgv',
            metrics=['distance', 'duration'],
            validate=True,
            optimized=True,
            dry_run=dry_rune,
        )
        self.matrix = matrix
        return self.matrix

    def getMinDistance(self):
        if (self.matrix == None):
            print(f"No matrix calculated yet for Tour {self.id}")
            return
        return min(self.matrix['distances'])

    def getMinDuration(self):
        if (self.matrix == None):
            print(f"No matrix calculated yet for Tour {self.id}")
            return
        return min(self.matrix['duration'])

    def createMap(self):
        m = folium.Map(location=self.inlet.getCoordinateslalo(), zoom_start=10)
        folium.Marker(location=self.inlet.getCoordinateslalo(),
                      popup=self.inlet.name).add_to(m)
        folium.Marker(location=self.outlet.getCoordinateslalo(),
                      popup=self.inlet.name).add_to(m)
        for c in self.clients:
            folium.Marker(location=c.getCoordinateslalo(),
                          popup=c.name).add_to(m)
        m.save(f'map_tour{self.id}.html')

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

    def summaryInFile(self, path=""):
        if path == "":
            path = "network_summary"
        f = open(path, 'w')
        f.write(self.__str__())
        f.close()

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

