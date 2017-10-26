from data_pull_functions.datapull_sql import generic_pull
from data_pull_functions.datapullclasses import Medication, EdMedication


def get_antiviral_info(coordinator, redcap_label, redcap_raw, subject_id, conn, dc_time):
    """Stores subjects antiviral info in dictionaies to use for file
    writing

    Args:
        coordinator (:obj: `OrderedDefaultDict`): collection of coordinator readable data
            to write to file
        redcap_label (:obj: `OrderedDefaultDict`): collection of redcap_label readable
        data to write to file
        redcap_raw (:obj: `OrderedDefaultDict`): collection of redcap_raw machine readable data to write to file
        subject_id (str): id of subject
        conn (:obj: `database connection`): connection to the database that
            contains the patient data
        dc_time (str): subjects discharge time

    Returns:
        :obj: `OrderedDefaultDict`):
        returns two ordered default dictionaries - coordinator and redcap_label that
        contain data to write to file
    """
    # ED Antivirals
    base_sql = """SELECT MedIndexName, TimeActionTaken, MedRoute
          FROM MedAdminName
          WHERE STUDYID = {} AND THERACLASS = {}"""
    antiviral_sql = base_sql.format(subject_id,"'ANTIVIRALS'")
    ed_antiviral_count = 0
    ed_antivirals = generic_pull(subject_id, antiviral_sql, "antivirals")
    if ed_antivirals:
        med_route_codes = {'IV' : '3',
                           'Intravenous' : '3',
                           'Oral' : '1',
                           'PO' : '1',
                           'IM' : '2',
                           'Intramuscular' : '2'
                           }

        for antiviral in ed_antivirals:
            antiviral_lab = Medication(*antiviral)
            med_route = antiviral_lab.route
            #Skip meds without proper routes and give after dishcarge from the ED
            if antiviral_lab.check_time(dc_time) is True and med_route_codes.get(med_route):
                ed_antiviral_count += 1
                if ed_antiviral_count < 3:
                    redcap_label['edenrollchart_antiviral'] = 'Yes'
                    redcap_raw['edenrollchart_antiviral'] = '1'
                    # Record number of Antivrals
                    redcap_label['edenrollchart_numberantivirals'] = ed_antiviral_count
                    redcap_raw['edenrollchart_numberantivirals'] = ed_antiviral_count
                if ed_antiviral_count >= 3:
                    break

                med_name = antiviral_lab.name.split(" ")[0]
                order_date_time = antiviral_lab.date_time
                order_date, order_time = order_date_time.split(" ")
                coordinator["ED Antiviral #{}".format(
                    ed_antiviral_count)] = "{} {}".format(med_name, med_route)
                redcap_label['edenrollchart_antiviral{}_name'.format(ed_antiviral_count)] = med_name
                redcap_label['edenrollchart_antiviral{}_route'.format(ed_antiviral_count)] = med_route
                redcap_label['edenrollchart_antiviral{}_date'.format(ed_antiviral_count)] = order_date
                redcap_label['edenrollchart_antiviral{}_time'.format(ed_antiviral_count)] = order_time[:5]

                redcap_raw['edenrollchart_antiviral{}_name'.format(ed_antiviral_count)] = med_name
                redcap_raw['edenrollchart_antiviral{}_route'.format(ed_antiviral_count)] = med_route_codes[med_route]
                redcap_raw['edenrollchart_antiviral{}_date'.format(ed_antiviral_count)] = order_date
                redcap_raw['edenrollchart_antiviral{}_time'.format(ed_antiviral_count)] = order_time[:5]
    else:
        coordinator['ED Antivirals'] = 'No antivirals given in the ED'
        redcap_label['edenrollchart_antiviral'] = 'No'
        redcap_raw['edenrollchart_antiviral'] = '0'

    return coordinator, redcap_label, redcap_raw


def get_dc_antiviral_info(coordinator, redcap_label, redcap_raw, subject_id, conn, dc_time, dispo):
    """Stores subjects discharge antiviral info in dictionaies to use for file
    writing

    Args:
        coordinator (:obj: `OrderedDefaultDict`): collection of coordinator readable data
            to write to file
        redcap_label (:obj: `OrderedDefaultDict`): collection of redcap_label readable
        data to write to file
        redcap_raw (:obj: `OrderedDefaultDict`): collection of redcap_raw machine readable data to write to file
        subject_id (str): id of subject
        conn (:obj: `database connection`): connection to the database that
            contains the patient data
        dc_time (str): subjects discharge time
        dispo (str): subjects final disposition

    Returns:
        :obj: `OrderedDefaultDict`):
        returns two ordered default dictionaries - coordinator and redcap_label that
        contain data to write to file
    """
    base_sql = """SELECT MedIndexName, TimeOrdered, MedRoute, THERACLASS,
          OrderingMode FROM EdMedication
          WHERE STUDYID = {} AND THERACLASS = {}
          AND OrderingMode = {}"""
    if dispo != "Discharge":
        redcap_label['edenrollchart_antiviraldischarge'] = 'NA subject not discharged'
        redcap_raw['edenrollchart_antiviraldischarge'] = '97'
        return coordinator, redcap_label, redcap_raw

    # Discharge Antivirals
    discharge_antiviral_count = 0
    med_sql = base_sql.format(subject_id, "'ANTIVIRALS'", "'Outpatient'")
    discharge_antivirals = generic_pull(conn, med_sql, 'discharge_antivirals')
    if discharge_antivirals:
        for antiviral in discharge_antivirals:
            dc_antiviral_lab = EdMedication(*antiviral)
            if dc_antiviral_lab.check_time(dc_time) is True:
                discharge_antiviral_count += 1
                if discharge_antiviral_count < 3:
                    redcap_label['edenrollchart_antiviraldischarge'] = 'Yes'
                    redcap_raw['edenrollchart_antiviraldischarge'] = '1'
                    # Record number of Dishcarged Antivirals
                    redcap_label['edenrollchart_numberantiviralsdischarge'] = discharge_antiviral_count
                    redcap_raw['edenrollchart_numberantiviralsdischarge'] = discharge_antiviral_count
                if discharge_antiviral_count >= 3:
                    break
                med_name = dc_antiviral_lab.name.split(" ")[0]
                med_route = dc_antiviral_lab.route
                coordinator["Discharge Antiviral #{}".format(discharge_antiviral_count)] = "{} {}".format(
                    med_name, med_route)
                redcap_label['edenrollchart_antiviraldischarge{}'.format(discharge_antiviral_count)] = med_name
                redcap_raw['edenrollchart_antiviraldischarge{}'.format(discharge_antiviral_count)] = med_name

    else:
        coordinator['Discharged Antiviral'] = 'No antivirals given at Discharge'
        redcap_label['edenrollchart_antiviraldischarge'] = 'No'
        redcap_raw['edenrollchart_antiviraldischarge'] = '0'

    return coordinator, redcap_label, redcap_raw