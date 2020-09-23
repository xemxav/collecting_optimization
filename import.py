from .FileLoader import FileLoader
import sys
from .Movement import Movement, Place, Outlet, Inlet, Client, Network

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
TTYPE = "Transport_type"
OUTLET = "Outlet"
OLO = "Outlet_Longitude"
OLA = "Outlet_latitude"


def check_movement_data(id, df): #todo : enregister les valeurs posant problemes
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
    return ret

def main(path):
    loader = FileLoader()
    df = loader.load(path)
    network = Network()
    for id in df[ID].unique():
        rows = df[df[ID] == id]
        if (check_movement_data(id, rows) == False):
            continue
        general_info = rows.iloc[0]
        if !Network.outlet_in_network(outlate_name=general_info[OUTLET]):

#todo : faire une class Network regroupant les inlet, outlet et clients pour savoir si deja enregistré

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        path = './retraitement.xlsx'
    else:
        path = sys.argv[1]
    main(path)