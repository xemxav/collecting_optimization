from FileLoader import FileLoader
import sys
from Movement import Tour, Outlet, Inlet, Client, Network
from reference import *

def check_tour_data(id, df):  # todo : enregister les valeurs posant problemes
    ret = True
    if len(df[OUTLET].unique()) > 1:
        print(f"The Outlet is not unique for ID {id}")
        ret = False
    if len(df[INLET].unique()) > 1:
        print(f"The Inlet is not unique for ID {id}")
        ret = False
    if len(df[DRIVER].unique()) > 1:
        print(f"The Driver is not unique for ID {id}")
        ret = False
    if len(df[MATERIAL].unique()) > 1:
        print(f"The Driver is not unique for ID {id}")
        ret = False
    return ret

def create_place(row, ptype):
    lon = None
    lat = None
    try:
        lon = float(row[ptype.lon_header])
        lat = float(row[ptype.lat_header])
    except ValueError:
        print(f"ID = {row[ID]} -- {ptype.__name__} {row[ptype.name_header]} not included because no coordinates")
        return None
    if not(lon and lat):
        return None
    if ptype == Client:
        return ptype(row[ptype.name_header], lon, lat, row[ptype.adr_header])
    else:
        return ptype(row[ptype.name_header], lon, lat)


def create_netwok(df):
    network = Network()
    for id in df[ID].unique():
        rows = df[df[ID] == id]
        if (check_tour_data(id, rows) == False):
            continue
        general_info = rows.iloc[0]
        outlet = network.getOutlet(general_info[OUTLET])
        inlet = network.getInlet(general_info[INLET])
        if outlet == None:
            outlet = create_place(general_info, Outlet)
        if inlet == None:
            inlet = create_place(general_info, Inlet)
        if inlet and outlet:
            new_tour = Tour(id=id,
                            inlet=inlet,
                            outlet=outlet,
                            date = general_info[DATE],
                            driver=general_info[DRIVER],
                            material=general_info[MATERIAL],
                            licence_plate=general_info[DRIPLATE])
        else:
            continue
        for _,row in rows.iterrows():
            client = create_place(row, Client)
            if client:
                network.addClient(client)
                new_tour.addClient(client)
        network.addTour(new_tour)
    return network

def main(path):
    loader = FileLoader()
    df = loader.load(path)
    network = create_netwok(df)
    print(network)


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        path = './retraitement.xlsx'
    else:
        path = sys.argv[1]
    main(path)
