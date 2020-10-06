import folium
import statistics as stat
from Places import Inlet, Outlet
import openrouteservice

class Tour:

    def __init__(self, tour_id, inlet, outlet, date, driver="", material="", licence_plate="",
                 clients=None):
        if not isinstance(inlet, Inlet) or not isinstance(outlet, Outlet):
            raise ValueError
        self.tour_id = tour_id
        self.inlet = inlet
        self.outlet = outlet
        self.driver = driver
        self.material = material
        self.licence_plate = licence_plate
        if clients is None:
            self.clients = list()
        else:
            self.clients = clients
        self.date = date
        self.min_distances = 0
        self.min_duration = 0
        self.avg_distances = 0
        self.avg_duration = 0
        self.high_up1 = None
        self.high_up2 = None
        self.matrix = None
        self.sorted_clients = None
        self.routes = None
        self.totaldistance = None
        self.totalduration = None
        return

    def addClient(self, client):
        self.clients.append(client)

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
        # todo : ajouter check sur presence données
        ret = f"tour_id = {self.tour_id}\n" \
              f"Date = {self.date.strftime('%d/%m/%Y')}\n" \
              f"Inlet = {self.inlet.name}\n" \
              f"Outlet = {self.outlet.name}\n" \
              f"Nombre de clients = {len(self.clients)}"
        if self.matrix is not None:
            ret += f"\nhigh_up1 : {self.high_up1['client'].name}\n"
            ret += f"Ordered list based on distance of clients : \n"
            for elem in self.sorted_clients:
                ret += f"\t- {elem['client'].name} dist = {elem['distance']}m\n"
        return ret

    def calculateMatrix(self, client, dry_rune=False):
        coords = self.getAllCoord()
        destinations = [i + 1 for i, v in enumerate(coords[1:])]
        try :
            matrix = client.distance_matrix(
                locations=coords,
                sources=[0, ],
                destinations=destinations,
                profile='driving-hgv',
                metrics=['distance', 'duration'],
                validate=True,
                optimized=True,
                dry_run=dry_rune,
            )
        except openrouteservice.exceptions.ApiError as e:
            print(e.args)
        self.matrix = matrix
        self.CalculateStat()
        self.SortClients()
        self.DefineHighUps()
        return True

    def checkmatrix(self):
        if self.matrix is None:
            print(f"No matrix calculated yet for Tour {self.tour_id}")
            return False
        return True

    def SortClients(self):
        if not self.checkmatrix():
            return False
        self.sorted_clients = list()
        length = len(self.matrix['distances'][0]) - 1
        distances = self.matrix['distances'][0][:length]
        duration = self.matrix['durations'][0][:length]
        for i, client in enumerate(self.clients):
            info = {
                'client': client,
                'duration': duration[i],
                'distance': distances[i],
            }
            self.sorted_clients.append(info)
        self.sorted_clients = sorted(self.sorted_clients, key=lambda elem: elem['distance'])
        return True

    def DefineHighUps(self):
        if not self.checkmatrix():
            return False
        self.high_up1 = self.sorted_clients[0]
        length = len(self.matrix['distances'][0]) - 1
        self.high_up2 = {
            'outlet': self.outlet,
            'duration': self.matrix['durations'][0][length],
            'distance': self.matrix['distances'][0][length],
        }
        return True

    def CalculateStat(self):
        if not self.checkmatrix():
            return False
        print(self.matrix['distances'][0])
        length = len(self.matrix['distances'][0]) - 1
        self.min_distances = min(self.matrix['distances'][0][:length])
        self.min_duration = min(self.matrix['durations'][0][:length])
        self.avg_distances = stat.mean(self.matrix['distances'][0][:length])
        self.avg_duration = stat.mean(self.matrix['durations'][0][:length])
        return True

    def calc_optimization(self, client, dry_run=False):
        if not self.checkmatrix():
            return False
        coords = [c['client'].getCoordinateslola() for c in self.sorted_clients]
        coords.append(self.high_up2["outlet"].getCoordinateslola())
        opti = True if len(coords) > 4 else False
        try:
            self.routes = client.directions(coords,
                                            profile='driving-hgv',
                                            format='geojson',
                                            optimize_waypoints=opti,
                                            dry_run=dry_run)
        except openrouteservice.exceptions.ApiError as e:
            print(e.args)
            return False

        try:
            self.firsttrack = client.directions([self.inlet.getCoordinateslola(),
                                                 self.high_up1['client'].getCoordinateslola()],
                                                profile='driving-hgv',
                                                format='geojson',
                                                dry_run=dry_run,
                                                validate=False)
        except openrouteservice.exceptions.ApiError as e:
            print(e.args)
            return False

        try:
            self.lasttrack = client.directions([self.high_up2['outlet'].getCoordinateslola(),
                                                self.inlet.getCoordinateslola()],
                                               profile='driving-hgv',
                                               format='geojson',
                                               dry_run=dry_run,
                                               validate=False)

        except openrouteservice.exceptions.ApiError as e:
            print(e.args)
            return False

        self.totaldistance = self.routes['features'][0]['properties']['summary']['distance'] \
                             + self.firsttrack['features'][0]['properties']['summary']['distance'] \
                             + self.lasttrack['features'][0]['properties']['summary']['distance']
        self.totalduration = self.routes['features'][0]['properties']['summary']['duration'] \
                             + self.firsttrack['features'][0]['properties']['summary']['duration'] \
                             + self.lasttrack['features'][0]['properties']['summary']['duration']
        return True

    def createMap(self, map=None):
        if map is None:
            map = folium.Map(location=self.inlet.getCoordinateslalo(), zoom_start=15)

        folium.Marker(location=self.inlet.getCoordinateslalo(),
                      popup=self.inlet.name).add_to(map)
        folium.Marker(location=self.outlet.getCoordinateslalo(),
                      popup=self.inlet.name).add_to(map)

        folium.PolyLine(locations=[list(reversed(coord))
                                   for coord in
                                   self.routes['features'][0]['geometry']['coordinates']]).add_to(map)

        folium.PolyLine(locations=[list(reversed(coord))
                                   for coord in
                                   self.firsttrack['features'][0]['geometry']['coordinates']]).add_to(map)

        folium.PolyLine(locations=[list(reversed(coord))
                                   for coord in
                                   self.lasttrack['features'][0]['geometry']['coordinates']]).add_to(map)

        for c in self.clients:
            folium.Marker(location=c.getCoordinateslalo(),
                          popup=c.name).add_to(map)
        map.save(f'map_tour{self.tour_id}.html')
        return map
