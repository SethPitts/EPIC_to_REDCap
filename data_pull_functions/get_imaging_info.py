from .datapull_sql import generic_pull
from .datapullclasses import Imaging

def get_imaging_info(coordinator, redcap_label, redcap_raw, subject_id, conn):
    """Stores subjects imaging info in dictionaies to use for file
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
    # Chest Imaging
    base_sql = r"""SELECT PROC_NAME, ORDER_TIME, OrderStatus FROM Procedures
          WHERE STUDYID = {} AND (PROC_NAME LIKE '%CT%'
          OR PROC_NAME LIKE'%XR%')
          AND OrderStatus = 'Completed'"""

    chest_sql = base_sql.format(subject_id)
    chest_xray_ct = generic_pull(conn, chest_sql, 'chestimaging')
    if chest_xray_ct:
        chest_xray_ct = [Imaging(*item) for item in chest_xray_ct]
        coordinator["Chest Imaging"] = chest_xray_ct[0].name
        redcap_label['edenrollchart_chestimaging'] = 'Yes'
        redcap_raw['edenrollchart_chestimaging'] = '1'
    else:
        coordinator['Chest Imagine'] = 'No chest imaging ordered in the ED'
        redcap_label['edenrollchart_chestimaging'] = 'No'
        redcap_raw['edenrollchart_chestimaging'] = '0'

    return coordinator, redcap_label, redcap_raw