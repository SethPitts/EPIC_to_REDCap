from .datapull_sql import arrival_date_time, discharge_date_time
from .datapullclasses import ADT

def get_arrival_info(coordinator, redcap_label, redcap_raw, subject_id, conn):
    """Stores subjects arrival info in dictionaies to use for file writing
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

    arrival_info = ADT(*arrival_date_time(subject_id, conn))
    coordinator['Arrival Date'] = arrival_info.date
    coordinator['Arrival Time'] = arrival_info.time
    redcap_label['edenrollchart_arrivaldate'] = arrival_info.date
    redcap_label['edenrollchart_arrivaltime'] = arrival_info.time[:5]
    redcap_raw['edenrollchart_arrivaldate'] = arrival_info.date
    redcap_raw['edenrollchart_arrivaltime'] = arrival_info.time[:5]

    return coordinator, redcap_label, redcap_raw


def get_discharge_info(coordinator, redcap_label, redcap_raw, subject_id, conn):
    """Stores subjects discharge info in dictionaies to use for file writing
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
    discharge_info = ADT(*discharge_date_time(subject_id, conn))
    coordinator['Discharge Date'] = discharge_info.date
    coordinator['Discharge Time'] = discharge_info.time
    redcap_label['edenrollchart_departtime'] = discharge_info.time[:5]
    redcap_label['edenrollchart_departdate'] = discharge_info.date
    redcap_raw['edenrollchart_departtime'] = discharge_info.time[:5]
    redcap_raw['edenrollchart_departdate'] = discharge_info.date

    return coordinator, redcap_label, redcap_raw


def get_dispo_info(coordinator, redcap_label, redcap_raw, subject_id, conn):
    """Stores subjects disposition info in dictionaies to use for file writing
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
    dispo_info = ADT(*arrival_date_time(subject_id, conn))
    coordinator['Disposition'] = dispo_info.dispo
    if dispo_info.dispo == "Discharge":
        redcap_label['edenrollchart_dispo'] = dispo_info.dispo
        redcap_raw['edenrollchart_dispo'] = '2'
        return coordinator, redcap_label, redcap_raw
    if dispo_info.dispo == "Hospitalized Observation":
        redcap_label['edenrollchart_dispo'] = 'Admit'
        redcap_raw['edenrollchart_dispo'] = '1'
        redcap_label['edenrollchart_observation'] = 'Yes'
        redcap_raw['edenrollchart_observation'] = '1'
        return coordinator, redcap_label, redcap_raw
    if dispo_info.dispo == 'Eloped':
        redcap_label['edenrollchart_dispo'] = dispo_info.dispo
        redcap_raw['edenrollchart_dispo'] = "3"
        return coordinator, redcap_label, redcap_raw
    if dispo_info.dispo == 'Admit':
        redcap_label['edenrollchart_dispo'] = dispo_info.dispo
        redcap_raw['edenrollchart_dispo'] = "1"
        return coordinator, redcap_label, redcap_raw

    redcap_label['edenrollchart_dispo'] = 'Other'
    redcap_label['edenrollchart_dispo_specify'] = dispo_info.dispo
    redcap_raw['edenrollchart_dispo'] = '4'
    redcap_raw['edenrollchart_dispo_specify'] = dispo_info.dispo

    return coordinator, redcap_label, redcap_raw