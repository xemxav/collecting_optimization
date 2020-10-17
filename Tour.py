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
        self.firsttrack = None
        self.lasttrack = None
        return

    def add_client(self, client):
        self.clients.append(client)

    def get_clients_coord(self):
        coord = list()
        for c in self.clients:
            coord.append(c.getCoordinates())
        return coord

    def get_all_coord(self):
        coord = list()
        coord.append(self.inlet.get_coordinates_lola())
        for c in self.clients:
            coord.append(c.get_coordinates_lola())
        coord.append(self.outlet.get_coordinates_lola())
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

    def calculate_matrix(self, client, dry_rune=False):
        print(f"Start matrix for ID {self.tour_id}")
        coords = self.get_all_coord()
        destinations = [i + 1 for i, v in enumerate(coords[1:])]
        matrix = None
        try:
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
        self.calculate_stat()
        self.sort_clients()
        self.define_highups()
        return True

    def checkmatrix(self):
        if self.matrix is None:
            print(f"No matrix calculated yet for Tour {self.tour_id}")
            return False
        return True

    def sort_clients(self):
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

    def define_highups(self):
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

    def calculate_stat(self):
        if not self.checkmatrix():
            return False
        length = len(self.matrix['distances'][0]) - 1
        self.min_distances = min(self.matrix['distances'][0][:length])
        self.min_duration = min(self.matrix['durations'][0][:length])
        self.avg_distances = stat.mean(self.matrix['distances'][0][:length])
        self.avg_duration = stat.mean(self.matrix['durations'][0][:length])
        return True

    def calc_optimization(self, client, dry_run=False):
        print(f"Start optimization for ID {self.tour_id}")
        if not self.checkmatrix():
            return False
        coords = [c['client'].get_coordinates_lola() for c in self.sorted_clients]
        coords.append(self.high_up2[
                          "outlet"].get_coordinates_lola())
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
            self.firsttrack = client.directions([self.inlet.get_coordinates_lola(),
                                                 self.high_up1['client'].get_coordinates_lola()],
                                                profile='driving-hgv',
                                                format='geojson',
                                                dry_run=dry_run,
                                                validate=False)
        except openrouteservice.exceptions.ApiError as e:
            print(e.args)
            return False

        try:
            self.lasttrack = client.directions([self.high_up2['outlet'].get_coordinates_lola(),
                                                self.inlet.get_coordinates_lola()],
                                               profile='driving-hgv',
                                               format='geojson',
                                               dry_run=dry_run,
                                               validate=False)

        except openrouteservice.exceptions.ApiError as e:
            print(e.args)
            return False

        self.totaldistance = self.routes['features'][0]['properties']['summary']['distance'] + \
                             self.firsttrack['features'][0]['properties']['summary']['distance'] + \
                             self.lasttrack['features'][0]['properties']['summary']['distance']
        self.totalduration = self.routes['features'][0]['properties']['summary']['duration'] + \
                             self.firsttrack['features'][0]['properties']['summary']['duration'] + \
                             self.lasttrack['features'][0]['properties']['summary']['duration']
        return True

    def create_map(self, initialmap=None):
        if initialmap is None:
            initialmap = folium.Map(location=self.inlet.get_coordinates_lalo(), zoom_start=15)

        folium.Marker(location=self.inlet.get_coordinates_lalo(),
                      popup=self.inlet.name).add_to(initialmap)
        folium.Marker(location=self.outlet.get_coordinates_lalo(),
                      popup=self.inlet.name).add_to(initialmap)

        folium.PolyLine(locations=[list(reversed(coord))
                                   for coord in
                                   self.routes['features'][0]['geometry']['coordinates']]).add_to(initialmap)

        folium.PolyLine(locations=[list(reversed(coord))
                                   for coord in
                                   self.firsttrack['features'][0]['geometry']['coordinates']]).add_to(initialmap)

        folium.PolyLine(locations=[list(reversed(coord))
                                   for coord in
                                   self.lasttrack['features'][0]['geometry']['coordinates']]).add_to(initialmap)

        for c in self.clients:
            folium.Marker(location=c.get_coordinates_lalo(),
                          popup=c.name).add_to(map)
        initialmap.save(f'map_tour{self.tour_id}.html')
        return initialmap
