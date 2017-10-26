from .datapull_sql import generic_pull
from .datapullclasses import Medication, EdMedication


def get_antibiotic_info(coordinator, redcap_label, redcap_raw, subject_id, conn, dc_time):
    """Stores subjects antibiotic info in dictionaies to use for file
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
    # ED Antibiotics
    base_sql = """SELECT MedIndexName, TimeActionTaken, MedRoute
          FROM MedAdminName
          WHERE STUDYID = {} AND THERACLASS = {}"""
    antibiotic_sql = base_sql.format(subject_id,"'ANTIBIOTICS'")
    ed_antibiotics_count = 0
    ed_antibiotics = generic_pull(conn, antibiotic_sql, 'antibiotics')
    if ed_antibiotics:
        med_route_codes = {'IV' : '3',
                           'Intravenous' : '3',
                           'Oral' : '1',
                           'PO' : '1',
                           'IM' : '2',
                           'Intramuscular' : '2'
                           }

        for antibiotic in ed_antibiotics:
            abx_med = Medication(*antibiotic)
            med_route = abx_med.route
            if abx_med.check_time(dc_time) is True and med_route_codes.get(med_route):
                # Record number of ED Antibiotics
                ed_antibiotics_count += 1
                if ed_antibiotics_count < 5:
                    redcap_label['edenrollchart_antibiotic'] = 'Yes'
                    redcap_label['edenrollchart_numberantibiotics'] = ed_antibiotics_count
                    redcap_raw['edenrollchart_antibiotic'] = '1'
                    redcap_raw['edenrollchart_numberantibiotics'] = ed_antibiotics_count
                if ed_antibiotics_count >= 5:
                    break

                med_name = abx_med.name.split(" ")[0]
                order_date_time = abx_med.date_time
                order_date, order_time = order_date_time.split(" ")
                coordinator["ED Antibiotics #{}".format( ed_antibiotics_count)] = "{} {} {} {}".format(
                    med_name, med_route, order_date, order_time)
                redcap_label['edenrollchart_antibiotic{}_name'.format(ed_antibiotics_count)] = med_name
                redcap_label['edenrollchart_antibiotic{}_date'.format(ed_antibiotics_count)] = order_date
                redcap_label['edenrollchart_antibiotic{}_time'.format(ed_antibiotics_count)] = order_time[:5]
                redcap_label['edenrollchart_antibiotic{}_route'.format(ed_antibiotics_count)] = med_route

                redcap_raw['edenrollchart_antibiotic{}_name'.format(ed_antibiotics_count)] = med_name
                redcap_raw['edenrollchart_antibiotic{}_date'.format(ed_antibiotics_count)] = order_date
                redcap_raw['edenrollchart_antibiotic{}_time'.format(ed_antibiotics_count)] = order_time[:5]
                redcap_raw['edenrollchart_antibiotic{}_route'.format(ed_antibiotics_count)] = med_route_codes[med_route]
    else:
        coordinator['ED Antibiotics' ] = 'No antibiotics given in the ED'
        redcap_label['edenrollchart_antibiotic'] = 'No'
        redcap_raw['edenrollchart_antibiotic'] = '0'

    return coordinator, redcap_label, redcap_raw


def get_dc_abx_info(coordinator, redcap_label, redcap_raw, subject_id, conn, dc_time, dispo):
    """Stores subjects discharge antibiotic info in dictionaies to use for file
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

    if dispo != "Discharge":
        redcap_label['edenrollchart_antibioticdischarge'] = 'NA subject not discharged'
        redcap_raw['edenrollchart_antibioticdischarge'] = '98'
        return coordinator, redcap_label, redcap_raw

    base_sql = """SELECT MedIndexName, TimeOrdered, MedRoute, THERACLASS,
          OrderingMode FROM EdMedication
          WHERE STUDYID = {} AND THERACLASS = {}
          AND OrderingMode = {}"""
    # Discharge Antibiotics
    discharge_antibiotics_count = 0
    dc_abx_sql = base_sql.format(subject_id, "'ANTIBIOTICS'", "'Outpatient'")
    discharge_antibiotics = generic_pull(conn, dc_abx_sql, "dc_abx")
    if discharge_antibiotics:

        for antibiotic in discharge_antibiotics:
            dc_abx_med = EdMedication(*antibiotic)
            if dc_abx_med.check_time(dc_time) is True:
                discharge_antibiotics_count += 1
                if discharge_antibiotics_count < 3:
                    redcap_label['edenrollchart_antibioticdischarge'] = 'Yes'
                    redcap_raw['edenrollchart_antibioticdischarge'] = '1'
                    # Record number of Discharge Abx
                    redcap_label['edenrollchart_numberantibioticsdischarge'] = discharge_antibiotics_count
                    redcap_raw['edenrollchart_numberantibioticsdischarge'] = discharge_antibiotics_count
                if discharge_antibiotics_count >= 3:
                    break
                med_name = dc_abx_med.name.split(" ")[0]
                time_ordered = dc_abx_med.date_time
                med_route = dc_abx_med.route
                coordinator["Discharge Antibiotics #{}".format(discharge_antibiotics_count)] = "{} {} {}".format(
                    med_name, med_route, time_ordered)
                redcap_label['edenrollchart_antibioticdischarge{}_name'.format(discharge_antibiotics_count)] = med_name
                redcap_raw['edenrollchart_antibioticdischarge{}_name'.format(discharge_antibiotics_count)] = med_name

    else:
        coordinator['Discharge Antibiotics'] = 'No antibiotics given at discharge'
        redcap_label['edenrollchart_antibioticdischarge'] = 'No'
        redcap_raw['edenrollchart_antibioticdischarge'] = '0'

    return coordinator, redcap_label, redcap_raw