from Places import Inlet, Outlet, Client
import pandas as pd
from reference import ID, OUTLET, INLET, MATERIAL
import time


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
        ret = ""
        for tour in self.tours:
            ret = ret + tour.__str__() + "\n"
        return ret

    def summary_in_file(self, path=""):
        if path == "":
            path = "network_summary"
        f = open(path, 'w')
        f.write(self.__str__())
        f.close()

    def client_in_network(self, client=None, client_name=""):
        if client is None and client_name != "":
            for c in self.clients:
                if c.name == client_name:
                    return True
            return False
        elif client is None and client in self.clients:
            return True
        return False

    def inlet_in_network(self, inlet=None, inlet_name=""):
        if inlet is None and inlet_name != "":
            for i in self.inlets:
                if i.name == inlet_name:
                    return True
            return False
        elif inlet is not None and inlet in self.inlets:
            return True
        return False

    def calc_network(self, client):
        data = []
        for tour in self.tours:
            print(f"Begin Calculation for ID {tour.tour_id}")
            if tour.calculate_matrix(client) and tour.calc_optimization(client):
                data.append([tour.tour_id,
                             tour.inlet.name,
                             tour.outlet.name,
                             tour.material,
                             len(tour.clients),
                             tour.totaldistance,
                             tour.totalduration
                             ])
            time.sleep(5)
        df = pd.DataFrame(data, columns=[ID, INLET, OUTLET, MATERIAL, "NB_CLIENTS", "DISTANCE_TOTALE", "DUREE_TOTALE"])
        print('\a')
        return df

    def outlet_in_network(self, outlet=None, outlet_name=""):
        if outlet is None and outlet_name != "":
            for o in self.outlets:
                if o.name == outlet_name:
                    return True
            return False
        elif outlet is not None and outlet in self.outlets:
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

    def get_outlet(self, outlet_name=""):
        for o in self.outlets:
            if o.name == outlet_name:
                return o
        return None

    def add_client(self, client):
        self.clients.append(client)

    def add_inlet(self, inlet):
        self.inlets.append(inlet)

    def add_outlet(self, outlet):
        self.outlets.append(outlet)

    def add_tour(self, tour):
        self.tours.append(tour)

    def get_tour_by_id(self, tour_id):
        for tour in self.tours:
            if tour.tour_id == tour_id:
                return tour
        return None
