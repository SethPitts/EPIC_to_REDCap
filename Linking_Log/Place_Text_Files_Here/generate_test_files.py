import csv

def create_test_tables():
    tables = dict()
    tables['ADT'] = [['STUDYID', 'EventType', 'in_dttm', 'out_dttm', 'adt_department_id', 'adt_department_name',
                     'adt_room_id', 'adt_room_nm_wid', 'adt_loc_name']
                     ]

    tables['Flowsheets'] = [['studyid', 'FLO_MEAS_ID', 'RECORDED_TIME', 'FlowsheetInternalName', 'FlowsheetDisplayName',
                            'FlowsheetValue', 'FLT_ID']
                            ]

    tables['Lab'] = [['STUDYID', 'ORDER_PROC_ID', 'LabComponentName', 'PROC_NAME', 'ORD_VALUE', 'ORN_NUM_VALUE',
                     'REFERENCE_UNIT', 'COMPONENT_COMMENT', 'RESULT_TIME', 'SPECIMN_TAKEN_TIME'
                     ]]

    tables['Diagnosis'] = [['STUDYID', 'EpicInternalDiagnosisName', 'ICD10Code', 'PRIMARY_DX_YN',
                           'ANNOTATION', 'COMMENTS', 'DX_ED_YN'
                           ]]
    tables['Procedures'] = [['STUDYID', 'PROC_NAME', 'ORDER_TIME', 'PROC_START_TIME', 'OrderStatus', 'TimeCancelled',
                            'LabStatus'
                            ]]
    tables['Medication'] = [['STUDYID', 'MEDICATION_ID', 'display_name', 'MedIndexName', 'TimeOrdered', 'MedRoute',
                            'Dose', 'MedUnit', 'MIN_DISCRETE_DOSE', 'THERACLASS', 'PHARMCLASS', 'PHARMSUBCLASS',
                            'OrderSTatus', 'OrderClass', 'OrderingMode', 'ORDER_MED_ID'
                            ]]

    tables['MedAdmins'] = [['STUDYID', 'ORDER_MED_ID', 'MEDICATION_ID', 'TimeActionTaken', 'ActionTaken',
                           'MAR_ORIG_DUE_TM', 'SCHEDULED_TIME', 'Dose', 'AdminSite', 'INFUSION_RATE',
                           'InfusionRateUnit', 'DurationToInfuse', 'Duration_Infuse_Unit'
                           ]]
    study_id_info = [['study_id', 'enrollment_date', 'mrn', 'data_pull_complete'],
                     ['0001', '01/01/2017', '00000001', 'no'],
                     ['0002', '02/02/2017', '00000002', 'no'],
                     ['0003', '03/03/2017', '00000003', 'no']
                     ]

    for table_title, table_fields in tables.items():
        with open('{}.txt'.format(table_title), 'w') as fin:
            csv_writer = csv.writer(fin, delimiter='\t')
            for row in table_fields:
                csv_writer.writerow(row)

    with open('study_ids_to_pull.csv', 'w') as fin:
        csv_writer = csv.writer(fin)
        for row in study_id_info:
            csv_writer.writerow(row)

def main():
    create_test_tables()


if __name__ == '__main__':
    main()
