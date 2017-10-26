from collections import defaultdict
from .datapull_sql import generic_pull
from .datapullclasses import Lab


def get_othervir_info(coordinator, redcap_label, redcap_raw, subject_id, conn, dc_time):
    """Stores subjects other virus info in dictionaies to use for file
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
    # Other Virus Testing

    multi_lab_sql = """SELECT ORD_VALUE, SPECIMN_TAKEN_TIME, RESULT_TIME, PROC_NAME, LabComponentName FROM LAB
          WHERE STUDYID = {}
          AND ({})"""

    othervirus_compnames = """LabComponentName = 'PARAINFLUENZAE 3 NAT'
                  OR LabComponentName = 'ADENOVIRUS NAT'
                  OR LabComponentName = 'RHINOVIRUS NAT'
                  OR LabComponentName = 'PARAINFLUENZAE 2 NAT'
                  OR LabComponentName = 'METAPNEUMO NAT'
                  OR LabComponentName = 'RSV NAT'
                  OR LabComponentName = 'ADENOVIRUS PCR'
                  OR LabComponentName = 'RHINOVIRUS PCR'
                  OR LabComponentName = 'PARAINFLUENZAE 2 PCR'
                  OR LabComponentName = 'METAPNEUMOVIRUS PCR'
                  OR LabComponentName = 'RSV PCR'"""

    other_virus_sql = multi_lab_sql.format(subject_id, othervirus_compnames)
    other_virus_tests = generic_pull(conn, other_virus_sql, 'other_viruses')
    if other_virus_tests:
        othervirus_testing = defaultdict(str)
        for test_result in other_virus_tests:
            othervirus_lab = Lab(*test_result)
            if othervirus_lab.check_time(dc_time) is True:
                redcap_label['edenrollchart_otherrespviruses'] = 'Yes'
                redcap_raw['edenrollchart_otherrespviruses'] = '1'
                result = othervirus_lab.value
                collect_time = othervirus_lab.collect_date_time
                result_type = othervirus_lab.componentname
                if result in ('No RNA Detected', 'No DNA Detected'):
                    result = 'negative'
                if result in ('DNA Detected', 'RNA Detected'):
                    result = result_type + " {}".format(result)
                result_id = "{}|{}".format(result_type, collect_time)
                # Negative Results
                if result == 'negative':
                    if not othervirus_testing.get(result_id):
                        othervirus_testing[result_id] = result
                        continue
                    if othervirus_testing[result_id] != 'negative':
                        continue
                # Positive Results
                if result:
                    if othervirus_testing.get(result_id) == 'negative':
                        othervirus_testing[result_id] = result
                        continue
                    else:
                        othervirus_testing[result_id] += " {}".format(result)
                        continue

        # Write Other Virus Tested Results to file
        for othervirus_result_name, othervirus_result in othervirus_testing.items():
            coordinator[othervirus_result_name] = othervirus_result
            test_name, order_time = othervirus_result_name.split("|")
            redcap_label_link = {'RSV NAT': 'edenrollchart_rsv',
                            'RHINOVIRUS NAT': 'edenrollchart_rhinovirus',
                            'ADENOVIRUS NAT': 'edenrollchart_adenovirus',
                            'PARAINFLUENZAE 3 NAT': 'edenrollchart_parainfluenza',
                            'PARAINFLUENZAE 2 NAT': 'edenrollchart_parainfluenza',
                            'METAPNEUMO NAT': 'edenrollchart_metapneumovirus',
                            'RSV PCR': 'edenrollchart_rsv',
                            'RHINOVIRUS PCR': 'edenrollchart_rhinovirus',
                            'ADENOVIRUS PCR': 'edenrollchart_adenovirus',
                            'PARAINFLUENZAE 3 PCR': 'edenrollchart_parainfluenza',
                            'PARAINFLUENZAE 2 PCR': 'edenrollchart_parainfluenza',
                            'METAPNEUMOVIRUS PCR': 'edenrollchart_metapneumovirus'
                            }
            if othervirus_result == 'negative':
                redcap_label[redcap_label_link[test_name]] = 'Negative'
                redcap_raw[redcap_label_link[test_name]] = '0'
            if othervirus_result == 'positive':
                redcap_label[redcap_label_link[test_name]] = 'Positive'
                redcap_raw[redcap_label_link[test_name]] = '1'
    else:
        coordinator['Other Virus Tested'] = 'Not tested for Other Viruses'
        redcap_label['edenrollchart_otherrespviruses'] = 'No'
        redcap_raw['edenrollchart_otherrespviruses'] = '0'

    return coordinator, redcap_label, redcap_raw