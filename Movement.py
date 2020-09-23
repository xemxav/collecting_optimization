import datetime


class Place:
    longitude = 0.0
    latitude = 0.0
    name = ""

    def __init__(self, name, longitude=0.0, latitude=0.0):
        self.name = name
        self.longitude = longitude
        self.latitude = latitude

    def get_coordinates(self):
        return self.longitude, self.latitude

    def set_coordinates(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude


class Inlet(Place):
    def __init__(self):
        return


class Outlet(Place):
    def __init__(self):
        return


class Client(Place):
    def __init__(self):
        return

class Network:

    def __init__(self,inlets=None,outlets=None,clients=None,):
        self.inlets = list()
        if isinstance(list):
            self.inlets = inlets
        elif isinstance(Inlet):
            self.inlets.append(inlets)

        self.outlets = list()
        if isinstance(list):
            self.outlets = outlets
        elif isinstance(Outlet):
            self.outlets.append(outlets)

        self.clients = list()
        if isinstance(list):
            self.clients = clients
        elif isinstance(Client):
            self.clients.append(clients)

    def client_in_network(self, client=None, client_name=""):
        if client == None and client_name != "":
            for c in self.clients:
                if c.name == client_name:
                    return True
            return False
        elif client != None and client in self.clients:
            return True
        return False

    def inlet_in_network(self, inlet=None, inlet_name=""):
        if inlet == None and inlet_name != "":
            for i in self.inlets:
                if i.name == inlet_name:
                    return True
            return False
        elif inlet != None and inlet in self.inlets:
            return True
        return False

    def outlet_in_network(self, outlet=None, outlet_name=""):
        if outlet == None and outlet_name != "":
            for o in self.outlets:
                if o.name == outlet_name:
                    return True
            return False
        elif outlet != None and outlet in self.outlets:
            return True
        return False

    def get_client(self, client_name):
        for c in self.clients:
            if c.name == client_name:
                    return c
        return None

    def get_inlet(self, inlet_name=""):
        for i in self.inlets:
            if i.name == inlet_name:
                return i
        return None

    def get_outlet(self, outlet=None, outlet_name=""):
        for o in self.outlets:
            if o.name == outlet_name:
                return o
        return False

    def add_client(self, client):
        self.clients.append(client)

    def add_inlet(self, inlet):
        self.inlets.append(inlet)

    def add_outlet(self, outlet):
        self.outlets.append(outlet)

class Movement:

    def __init__(self, id, inlet, outlet, driver="",junk_type="", licence_plate="", clients=None, date=""): #todo : changer date defaut
        self.id = id
        self.inlet = inlet
        self.outlet = outlet
        self.driver = driver
        self.junk_type = junk_type
        self.licence_plate = licence_plate
        self.clients = clients
        self.date = date
        return

    def add_client(self, client):
        self.clients.append(client)
