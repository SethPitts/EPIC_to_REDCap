from .datapull_sql import generic_pull
from .datapullclasses import Vitals
def get_oxygen_info(coordinator, redcap_label, redcap_raw, subject_id, conn):
    """Stores subjects oxygen info in dictionaies to use for file writing
    Args:
        coordinator (:obj: `OrderedDefaultDict`): collection of coordinator readable data
            to write to file
        redcap_label (:obj: `OrderedDefaultDict`): collection of redcap_label readable
        data to write to file
        redcap_raw (:obj: `OrderedDefaultDict`): collection of redcap_raw machine readable data to write to file
        subject_id (str): id of subject
        conn (:obj: `database connection`): connection to the database that
            contains the patient data

    Returns:
        :obj: `OrderedDefaultDict`):
        returns two ordered default dictionaries - coordinator and redcap_label that
        contain data to write to file
    """
    # Find relevant O2 devices
    oxygen_sql = """SELECT FlowsheetDisplayName, RECORDED_TIME, FlowsheetValue
            FROM Flowsheets
            WHERE STUDYID = {}
            AND FlowsheetDisplayName = {}""".format(subject_id, "'O2 Device'")
    oxygen_info = generic_pull(conn, oxygen_sql, "vitals_oxygen")
    # oxygen_info = ed.vitals(subject_id, conn, "'O2 Device'")
    oxygen_type_codes = {'Nasal cannula' : "1",
                         'High flow nasal cannula' : '1',
                         'Non-rebreather mask' : '2',
                         'Simple Facemask' : '2',
                        'Trach mask' : '2',
                         'Venturi mask' : '2',
                         'BiPAP' : '3',
                         'CPAP' : '3'
                         }

    # Find all oxygen values
    if oxygen_info:
        # Find all oxygen values
        for vital_sign in oxygen_info:
            oxygen = Vitals(*vital_sign)
            if oxygen.value in ('Nasal cannula', 'Non-rebreather mask', 'High flow nasal cannula', 'Simple Facemask',
                                'Trach mask', 'Venturi mask'):
                coordinator['Oxygen Supplmentation in ED'] = "{} Recorded At {}, ".format(oxygen.value, oxygen.date_time)
                redcap_label['edenrollchart_o2supplementanytime'] = 'Yes'
                redcap_label['edenrollchart_o2supplementanytime_route'] = oxygen.value

                redcap_raw['edenrollchart_o2supplementanytime'] = '1'
                redcap_raw['edenrollchart_o2supplementanytime_route'] = oxygen_type_codes[oxygen.value]
    else:
        coordinator['Oxygen Supplementation in ED'] = 'Not Oxygen Supplementation was given while in ED'
        redcap_label['edenrollchart_o2supplementanytime'] = 'No'
        redcap_label['edenrollchart_o2supplementinitial'] = 'No'
        redcap_label['edenrollchart_o2supplementleaving'] = 'No'

        redcap_label['edenrollchart_o2supplementanytime'] = '0'
        redcap_label['edenrollchart_o2supplementinitial'] = '0'
        redcap_label['edenrollchart_o2supplementleaving'] = '0'

    return coordinator, redcap_label, redcap_raw
