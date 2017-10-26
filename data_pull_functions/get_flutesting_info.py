from collections import defaultdict

from .datapull_sql import generic_pull
from .datapullclasses import Lab


def get_flutesting_info(coordinator, redcap_label, redcap_raw, subject_id, conn, dc_time):
    """Stores subjects flu testing info in dictionaies to use for file writing
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
    # Influenza Testing

    multi_lab_sql = """SELECT ORD_VALUE, SPECIMN_TAKEN_TIME, RESULT_TIME, PROC_NAME, LabComponentName FROM LAB
          WHERE STUDYID = {}
          AND ({})"""

    influenza_count = 0
    influenza_compnames = """LabComponentName = 'INFLUENZA A NAT'
                  OR LabComponentName = 'INFLUENZA B NAT'
                  OR LabComponentName = 'INFLUENZA A PCR'
                  OR LabComponentName = 'INFLUENZA B PCR'"""

    influenza_sql = multi_lab_sql.format(subject_id, influenza_compnames)
    influenza_tests, lab_name = generic_pull(conn, influenza_sql, 'influenza')
    influenza_testing = defaultdict(str)
    if influenza_tests:
        for test_result in influenza_tests:
            influenza_lab = Lab(*test_result)
            if influenza_lab.check_time(dc_time) is True:
                influenza_count += 1
                if influenza_count < 5:
                    # Find first test for patient
                    redcap_label['edenrollchart_flutest'] = 'Yes'
                    redcap_raw['edenrollchart_flutest'] = '1'
                    # Record Number of Influenza Test Done
                    redcap_label['edenrollchart_numberflutests'] = influenza_count
                    redcap_raw['edenrollchart_numberflutests'] = influenza_count
                if influenza_count >= 5:
                    break
                result = influenza_lab.value
                test_name = influenza_lab.labname
                result_type = influenza_lab.componentname
                collect_time = influenza_lab.collect_date_time
                result_time = influenza_lab.result_date_time
                if result in ('No RNA Detected', 'No DNA Detected'):
                    result = 'negative'
                if result in ('DNA Detected', 'RNA Detected'):
                    result = "{} {}".format(result_type, result)
                result_id = "{}|{}|{}".format(test_name, collect_time, result_time)
                # Negative Results
                if result == 'negative':
                    if not influenza_testing.get(result_id):
                        influenza_testing[result_id] = result
                        continue
                    if influenza_testing[result_id] != 'negative':
                        continue
                # Positive Results
                if result:
                    if influenza_testing.get(result_id) == 'negative':
                        influenza_testing[result_id] = result
                        continue
                    else:
                        influenza_testing[result_id] += "{}".format(result)
                        continue

        # Write Influenza Results to dictionaries
        influenza_count = 0
        for influenza_result_name, influenza_result in influenza_testing.items():
            test_name, collect_info, result_info = influenza_result_name.split("|")
            collect_date, collect_time = collect_info.split(" ")
            result_date, result_time = result_info.split(" ")
            influenza_count += 1
            testing_type = 'pcr'
            if influenza_result == 'negative':
                test_result = 'negative'
                redcap_label['edenrollchart_flutest{}_result'.format(influenza_count)] = 'Negative'
                redcap_raw['edenrollchart_flutest{}_result'.format(influenza_count)] = '1'
            else:
                test_result = 'positive'
                redcap_label['edenrollchart_flutest{}_typing'.format(influenza_count)] = 'Yes'
                redcap_label['edenrollchart_flutest{}_typing_specify'.format(influenza_count)] = influenza_result.split(" ")[1]
                redcap_label['edenrollchart_flutest{}_result'.format(influenza_count)] = 'Positive'

                redcap_raw['edenrollchart_flutest{}_typing'.format(influenza_count)] = '1'
                redcap_raw['edenrollchart_flutest{}_typing_specify'.format(influenza_count)] = influenza_result.split(" ")[1]
                redcap_raw['edenrollchart_flutest{}_result'.format(influenza_count)] = '2'

            coordinator[influenza_result_name] = influenza_result
            redcap_label['edenrollchart_flutest{}_name'.format(influenza_count)] = test_name
            redcap_label['edenrollchart_flutest{}_type'.format(influenza_count)] = testing_type
            redcap_label['edenrollchart_flutest{}_collectiondate'.format(influenza_count)] = collect_date
            redcap_label['edenrollchart_flutest{}_collectiontime'.format(influenza_count)] = collect_time[:5]
            redcap_label['edenrollchart_flutest{}_resultdate'.format(influenza_count)] = result_date
            redcap_label['edenrollchart_flutest{}_resulttime'.format(influenza_count)] = result_time[:5]

            redcap_raw['edenrollchart_flutest{}_name'.format(influenza_count)] = test_name
            redcap_raw['edenrollchart_flutest{}_type'.format(influenza_count)] = '1'
            redcap_raw['edenrollchart_flutest{}_collectiondate'.format(influenza_count)] = collect_date
            redcap_raw['edenrollchart_flutest{}_collectiontime'.format(influenza_count)] = collect_time[:5]
            redcap_raw['edenrollchart_flutest{}_resultdate'.format(influenza_count)] = result_date
            redcap_raw['edenrollchart_flutest{}_resulttime'.format(influenza_count)] = result_time[:5]

    else:
        coordinator['Influenza Testing'] = 'No Influenza Testing Done'
        redcap_label['edenrollchart_flutest'] = 'No'
        redcap_raw['edenrollchart_flutest'] = '0'

    return coordinator, redcap_label, redcap_raw