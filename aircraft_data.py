# aircraft_data.py
# Base de datos de aviones (BADA) extraída de los parámetros del simulador

aircraft_db = {
    'B767-300ER': {
        'MLW': 145150,
        'S': 283.50,
        'CD0_app': 0.01400,
        'CD2_app': 0.04900,
        'CD0_clean': 0.01740,
        'CD2_clean': 0.04590,
        'hp_desc': 26418,
        'CT_desc_high': 0.064359,
        'CT_desc_low': 0.055988,
        'CT_desc_app': 0.12475,
        'CT1': 351670.0,
        'CT2': 44673.0,
        'CT3': 0.10129e-9
    },
    'B777-300': {
        'MLW': 237680,
        'S': 428.04,
        'CD0_app': 0.01730,
        'CD2_app': 0.04840,
        'CD0_clean': 0.01570,
        'CD2_clean': 0.04200,
        'hp_desc': 36122,
        'CT_desc_high': 0.044239,
        'CT_desc_low': 0.041065,
        'CT_desc_app': 0.092921,
        'CT1': 425770.0,
        'CT2': 48987.0,
        'CT3': 0.66146e-10
    },
    'B737': {
        'MLW': 51710,
        'S': 124.65,
        'CD0_app': 0.02700,
        'CD2_app': 0.04410,
        'CD0_clean': 0.02350,
        'CD2_clean': 0.04450,
        'hp_desc': 30152,
        'CT_desc_high': 0.036336,
        'CT_desc_low': 0.053395,
        'CT_desc_app': 0.16440,
        'CT1': 145730.0,
        'CT2': 55638.0,
        'CT3': 0.14200e-10
    },
    'A320-212': {
        'MLW': 64500,
        'S': 122.60,
        'CD0_app': 0.02420,
        'CD2_app': 0.04690,
        'CD0_clean': 0.02400,
        'CD2_clean': 0.03750,
        'hp_desc': 12398,
        'CT_desc_high': 0.045711,
        'CT_desc_low': 0.027207,
        'CT_desc_app': 0.13981,
        'CT1': 136050.0,
        'CT2': 52238.0,
        'CT3': 0.26637e-10
    },
    'A319-131': {
        'MLW': 61000,
        'S': 122.60,
        'CD0_app': 0.02840,
        'CD2_app': 0.03760,
        'CD0_clean': 0.02800,
        'CD2_clean': 0.03100,
        'hp_desc': 27726,
        'CT_desc_high': 0.083084,
        'CT_desc_low': 0.051765,
        'CT_desc_app': 0.14767,
        'CT1': 139000.0,
        'CT2': 58900.0,
        'CT3': 0.57200e-14
    }
}

def get_aircraft_data(model):
    return aircraft_db.get(model, None)