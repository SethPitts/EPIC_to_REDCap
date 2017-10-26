from datetime import datetime

from .datapull_sql import generic_pull


def get_lab_info(coordinator, redcap_label, redcap_raw, subject_id, conn):
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

    # Function to find minimums
    # TODO: this can become a for loop for each value to search for
    single_lab_sql = """SELECT ORD_VALUE, SPECIMN_TAKEN_TIME, RESULT_TIME, PROC_NAME, LabComponentName FROM LAB
          WHERE STUDYID = {}
          AND LabComponentName = {}"""

    multi_lab_sql = """SELECT ORD_VALUE, SPECIMN_TAKEN_TIME, RESULT_TIME, PROC_NAME, LabComponentName FROM LAB
          WHERE STUDYID = {}
          AND ({})"""

    def min_lab(x):
        return datetime.strptime(x[1], '%Y-%m-%d %H:%M:%S')
    # PH
    ph_sql = single_lab_sql.format(subject_id, "'PH SPECIMEN'")
    ph_lab = (ph, ph_lab_name) = generic_pull(conn, ph_sql, 'ph')

    # BUN
    bun_compnames = """LabComponentName = 'BLOOD UREA NITROGEN'
                    OR LabComponentName = 'UREA NITROGEN'"""
    bun_sql = multi_lab_sql.format(subject_id, bun_compnames)
    bun_lab = (bun, bun_lab_name) = generic_pull(conn, bun_sql, 'bun')

    # Glucose
    glucose_sql = single_lab_sql.format(subject_id, "'GLUCOSE'")
    glucose_lab = (glucose, glu_lab_name) = generic_pull(conn, glucose_sql, 'lucose')

    # Sodium
    sodium_sql = single_lab_sql.format(subject_id, "'SODIUM'")
    sodium_lab = (sodium, sod_lab_name) = generic_pull(conn, sodium_sql, 'sodium')

    # Hematocrit
    hematocrit_sql = single_lab_sql.format(subject_id, "'HEMATOCRIT'")
    hematocrit_lab = (hematocrit, hema_lab_name) = generic_pull(conn, hematocrit_sql, 'hematocrit')
    # ph = ed.lab(subject_id, conn, "'PH SPECIMEN'")
    all_labs = [ph_lab, bun_lab, glucose_lab, sodium_lab, hematocrit_lab]

    for lab, lab_name in all_labs:
        if lab and min(lab, key=min_lab)[0] != 'see below':
            lab_value = min(lab, key=min_lab)[0]
            coordinator[lab_name] = lab_value
            redcap_label['edenrollchart_{}'.format(lab_name)] = lab_value
            redcap_raw['edenrollchart_{}'.format(lab_name)] = lab_value
        else:
            coordinator[lab_name] = 'Not Done'
            redcap_label['edenrollchart_{}'.format(lab_name)] = 'Not Done'
            redcap_raw['edenrollchart_{}'.format(lab_name)] = '999'
    return coordinator, redcap_label, redcap_raw