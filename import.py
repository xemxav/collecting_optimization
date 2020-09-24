from FileLoader import FileLoader
import sys
from Movement import Tour, Outlet, Inlet, Client, Network

ID = "ID"
INLET = "Inlet"
ILA = "Inlet_Latitude"
ILO = "Inlet_Longitude"
MONTH = "Month"
DATE = "Execution_date"
DRIPLATE = "Immatriculation"
DRIVER = "Driver"
CNAME = "Client_name"
CADR = "Client_adress"
CLA = "Client_Latitude"
CLO = "Client_Longitude"
MATERIAL = "Transport_type"
OUTLET = "Outlet"
OLO = "Outlet_Longitude"
OLA = "Outlet_latitude"


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
    # if "(vide)" in df[CLO].values() :
    #     print(f"a client longitude is not unique for ID {id}")
    #     ret = False
    # if "(vide)" in df[CLA].values() :
    #     print(f"a client latitude is not unique for ID {id}")
    #     ret = False
    return ret

def create_netwok(df):
    network = Network()
    for id in df[ID].unique():
        rows = df[df[ID] == id]
        if (check_tour_data(id, rows) == False):
            continue
        general_info = rows.iloc[0]
        outlet = network.get_outlet(general_info[OUTLET])
        inlet = network.get_outlet(general_info[INLET])
        if outlet == None:
            outlet = Outlet(name=general_info[OUTLET],
                            longitude=general_info[OLO],
                            latitude=general_info[OLA])
            network.add_outlet(outlet)
        if inlet == None:
            inlet = Inlet(name=general_info[INLET],
                          longitude=general_info[ILO],
                          latitude=general_info[ILA])
            network.add_inlet(inlet)
        new_tour = Tour(id=id,
                        inlet=inlet,
                        outlet=outlet,
                        driver=general_info[DRIVER],
                        material=general_info[MATERIAL],
                        licence_plate=general_info[DRIPLATE])
        for _,row in rows.iterrows():
            lat = None
            lon = None
            try:
                lat = float(row[CLA])
                lon = float(row[CLO])
            except ValueError:
                print(f"ID = {id} -- Client {row[CNAME]} not included because no coordinates")
            if lat and lon:
                new_client = Client(name=row[CNAME],
                                    longitude=lon,
                                    latitude=lat,
                                    adress=row[CADR])
                network.add_client(new_client)
                new_tour.add_client(new_client)
    return network

def main(path):
    loader = FileLoader()
    df = loader.load(path)
    network = create_netwok(df)


# todo : faire une class Network regroupant les inlet, outlet et clients pour savoir si deja enregistré

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        path = './retraitement.xlsx'
    else:
        path = sys.argv[1]
    main(path)
