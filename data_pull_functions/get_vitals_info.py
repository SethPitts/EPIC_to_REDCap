from datetime import datetime
from .datapull_sql import generic_pull


def get_vitals_info(coordinator, redcap_label, redcap_raw, subject_id, conn):
    """Stores subjects vitals info in dictionaies to use for file writing
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
    # Function to find minimums
    base_sql = """SELECT FlowsheetDisplayName, RECORDED_TIME, FlowsheetValue
            FROM Flowsheets
            WHERE STUDYID = {}
            AND FlowsheetDisplayName = {}"""
    def min_lab(x):
        return datetime.strptime(x[1], '%Y-%m-%d %H:%M:%S')

    # Temp
    temp_sql = base_sql.format(subject_id, "'Temp'")
    temp = generic_pull(conn, temp_sql, 'vitals_temp')
    # temp = ed.vitals(subject_id, conn, "'Temp'")
    if temp:
        temp = min(temp, key=min_lab)[2]
        coordinator['temp'] = temp
        redcap_label['edenrollchart_temperature'] = temp
        redcap_raw['edenrollchart_temperature'] = temp
    else:
        coordinator['temp'] = 'Temperature not recorded'
        redcap_label['edenrollchart_temperature'] = 'Not Recorded'
        redcap_raw['edenrollchart_temperature'] = '999'


    # Resp
    resp_sql = base_sql.format(subject_id, "'Resp'")
    resp = generic_pull(conn, resp_sql, 'vitals_resp')
    # resp = ed.vitals(subject_id, conn, "'Resp'")
    if resp:
        resp = min(resp, key=min_lab)[2]
        coordinator['resp'] = resp
        redcap_label['edenrollchart_respiratoryrate'] = resp
        redcap_raw['edenrollchart_respiratoryrate'] = resp
    else:
        coordinator['resp'] = 'Respirations not recorded'
        redcap_label['edenrollchart_respiratoryrate'] = 'Not Recorded'
        redcap_raw['edenrollchart_respiratoryrate'] = '999'
    # Blood Pressure
    bp_sql = base_sql.format(subject_id, "'BP'")
    bp = generic_pull(conn, bp_sql, 'vitals_bp')
    # bp = ed.vitals(subject_id, conn, "'BP'")
    if bp:
        bp = min(bp, key=min_lab)[2]
        bp = bp.split("/")[0]
        coordinator['bp'] = bp
        redcap_label['edenrollchart_systolicbloodpressure'] = bp
        redcap_raw['edenrollchart_systolicbloodpressure'] = bp
    else:
        coordinator['bp'] = 'Blood Pressure not recorded'
        redcap_label['edenrollchart_systolicbloodpressure'] = 'Not Recorded'
        redcap_raw['edenrollchart_systolicbloodpressure'] = '999'
    # Pulse
    pulse_sql = base_sql.format(subject_id, "'Pulse'")
    pulse = generic_pull(conn, pulse_sql, 'vitals_pulse')
    # pulse = ed.vitals(subject_id, conn, "'Pulse'")
    if pulse:
        pulse = min(pulse, key=min_lab)[2]
        coordinator['pulse'] = pulse
        redcap_label['edenrollchart_pulse'] = pulse
        redcap_raw['edenrollchart_pulse'] = pulse
    else:
        coordinator['pulse'] = 'Pulse not recorded'
        redcap_label['edenrollchart_pulse'] = 'Not Recorded'
        redcap_raw['edenrollchart_pulse'] = '999'
    # O2 SAT
    oxygen_sql = base_sql.format(subject_id, "'SpO2'")
    oxygen_sat = generic_pull(conn, oxygen_sql, 'vitals_spo2')
    # oxygen_sat = ed.vitals(subject_id, conn, "'SpO2'")
    if oxygen_sat:
        oxygen_sat = min(oxygen_sat, key=min_lab)[2]
        coordinator['Oxgyen Saturation'] = oxygen_sat
        redcap_label['edenrollchart_o2sat'] = oxygen_sat
        redcap_raw['edenrollchart_o2sat'] = oxygen_sat
    else:
        coordinator['Oxgyen Saturation'] = 'O2 Sat not recorded'
        redcap_label['edenrollchart_o2sat'] = 'Not Recorded'
        redcap_raw['edenrollchart_o2sat'] = '999'

    return coordinator, redcap_label, redcap_raw