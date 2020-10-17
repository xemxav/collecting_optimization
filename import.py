from FileLoader import FileLoader
import sys
from Places import Outlet, Inlet, Client
from Tour import Tour
from Network import Network
from reference import *
import openrouteservice


def check_tour_data(tour_id, df):  # todo : enregister les valeurs posant problemes
    ret = True
    if len(df[OUTLET].unique()) > 1:
        print(f"The Outlet is not unique for ID {tour_id}")
        ret = False
    if len(df[INLET].unique()) > 1:
        print(f"The Inlet is not unique for ID {tour_id}")
        ret = False
    if len(df[DRIVER].unique()) > 1:
        print(f"The Driver is not unique for ID {tour_id}")
        ret = False
    if len(df[MATERIAL].unique()) > 1:
        print(f"The Driver is not unique for ID {tour_id}")
        ret = False
    return ret


def create_place(row, ptype):
    try:
        lon = float(row[ptype.lon_header])
        lat = float(row[ptype.lat_header])
    except ValueError:  # todo : faire un enregistrement des logs erreurs
        print(f"ID = {row[ID]} -- {ptype.__name__} {row[ptype.name_header]} not included because no coordinates")
        return None
    if not (lon and lat):
        return None
    if ptype == Client:
        return ptype(row[ptype.name_header], lon, lat, row[ptype.adr_header])
    else:
        return ptype(row[ptype.name_header], lon, lat)


def create_netwok(df):
    network = Network()
    for tour_id in df[ID].unique():
        rows = df[df[ID] == tour_id]
        if check_tour_data(tour_id, rows) is False:
            continue
        general_info = rows.iloc[0]
        outlet = network.get_outlet(general_info[OUTLET])
        inlet = network.get_inlet(general_info[INLET])
        if outlet is None:
            outlet = create_place(general_info, Outlet)
        if inlet is None:
            inlet = create_place(general_info, Inlet)
        if inlet and outlet:
            new_tour = Tour(tour_id=tour_id,
                            inlet=inlet,
                            outlet=outlet,
                            date=general_info[DATE],
                            driver=general_info[DRIVER],
                            material=general_info[MATERIAL],
                            licence_plate=general_info[DRIPLATE])
        else:
            continue
        for _, row in rows.iterrows():
            client = create_place(row, Client)
            if client:
                network.add_client(client)
                new_tour.add_client(client)
        network.add_tour(new_tour)
    return network


def main(file_path):
    df = FileLoader.load(file_path)
    FileLoader.display(df, 10)
    network = create_netwok(df)
    network.summary_in_file(f"{file_path}_net_summary")
    client = openrouteservice.Client(key=APIKEY)
    output = network.calc_network(client)
    network.tours[0].create_map()
    # #todo : faire un df qui fait un calcul sur le df et mettre en 2eme sheet
    output.to_excel("output.xlsx")


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        path = './retraitement.xlsx'
    else:
        path = sys.argv[1]
    main(path)
