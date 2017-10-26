from .datapull_sql import generic_pull

def get_diagnosis_info(coordinator, redcap_label, redcap_raw, subject_id, conn):
    """Stores subjects diagnosis info in dictionaies to use for file
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

    Returns:
        :obj: `OrderedDefaultDict`):
        returns two ordered default dictionaries - coordinator and redcap_label that
        contain data to write to file
    """

    #Initial all values to be no
    redcap_label['edenrollchart_dxinfluenza'] = 'No'
    redcap_label['edenrollchart_dxviralsyndrome'] = 'No'
    redcap_label['edenrollchart_dxpneumonia'] = 'No'
    redcap_label['edenrollchart_dxmyocardialinfarction'] = 'No'
    redcap_label['edenrollchart_dxstroke'] = 'No'

    redcap_raw['edenrollchart_dxinfluenza'] = '0'
    redcap_raw['edenrollchart_dxviralsyndrome'] = '0'
    redcap_raw['edenrollchart_dxpneumonia'] = '0'
    redcap_raw['edenrollchart_dxmyocardialinfarction'] = '0'
    redcap_raw['edenrollchart_dxstroke'] = '0'

    # Final Diagnoses
    base_sql = """SELECT EpicInternalDiagnosisName FROM Diagnosis
          WHERE STUDYID = {}"""

    diagnosis_sql = base_sql.format(subject_id)
    diagnosis_count = 0
    diagnoses = generic_pull(conn, diagnosis_sql, 'diagnosis')
    coordinator['Diagnoses'] = diagnoses
    for diagnosis in diagnoses:
        diagnosis_count += 1
        # Record Diagnosis Number
        redcap_label['edenrollchart_numberdx'] = diagnosis_count
        redcap_raw['edenrollchart_numberdx'] = diagnosis_count
        if diagnosis_count > 3:
            redcap_label['edenrollchart_numberdx'] = 'More than three'
            redcap_raw['edenrollchart_numberdx'] = '4'
            break
        redcap_label['edenrollchart_dx{}'.format(diagnosis_count)] = diagnosis[0]
        if diagnosis[0].lower().find('influenza') != -1:
            redcap_label['edenrollchart_dxinfluenza'] = 'Yes'
            redcap_raw['edenrollchart_dxinfluenza'] = '1'
        if diagnosis[0].lower().find('viral syndrome') != -1 or diagnosis[0].lower().find('viral infection') != -1:
            redcap_label['edenrollchart_dxviralsyndrome'] = 'Yes'
            redcap_raw['edenrollchart_dxviralsyndrome'] = '1'
        if diagnosis[0].lower().find('pneumonia') != -1:
            redcap_label['edenrollchart_dxpneumonia'] = 'Yes'
        if diagnosis[0].lower().find('myocardial infarction') != -1:
            redcap_label['edenrollchart_dxmyocardialinfarction'] = 'Yes'
            redcap_raw['edenrollchart_dxmyocardialinfarction'] = '1'
        if diagnosis[0].lower().find('stroke') != -1:
            redcap_label['edenrollchart_dxstroke'] = 'Yes'
            redcap_raw['edenrollchart_dxstroke'] = '1'

    return coordinator, redcap_label, redcap_raw
