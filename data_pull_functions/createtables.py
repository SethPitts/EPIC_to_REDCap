import csv
import os
import sqlite3


def create_table(conn, table_title, table_fields, table_data):
    """
    Create a sqlite3 table using the given data
    :param conn: database connection to the database to store the table
    :param table_title: title of table
    :param table_fields: list of the table fields
    :param table_data: list of the table rows
    :return: No return
    """
    cur = conn.cursor()

    # Create Table Statement
    # We drop tables so that we are always working with most up to date data
    table_fields = ",".join(table_fields)
    drop_table_sql = """DROP TABLE IF EXISTS {}""".format(table_title)
    create_table_sql = """CREATE TABLE {} ({})""".format(
        table_title, table_fields)
    print("Creating table {}".format(table_title))
    cur.execute(drop_table_sql)
    cur.execute(create_table_sql)

    # Insert Values Statement
    for table_row in table_data:
        transform = "'{}'"
        data_as_text = ",".join(
            [transform.format(item.replace("'", "").replace(",", "")) for item in table_row])
        insert_sql = """INSERT INTO {} VALUES ({})""".format(
            table_title, data_as_text)
        cur.execute(insert_sql)
    # Commit the changes
    conn.commit()
    print("Done Creating table {}".format(table_title))


def get_sql_data_from_file(filename, delimiter='\t'):
    """
    Gets sql data from a txt or csv file
    :param filename: file name
    :param delimiter: delimiter that separates values in file
    :return: tuple containing title of table, fields for the table, and data to write into table
    """
    with open(filename, 'r') as fin:
        # Most files we will be working with will be tsv
        csv_reader = csv.DictReader(fin, delimiter=delimiter)
        # Assume file has headers
        # TODO: make option to provide headres for files that don't have headers
        table_fields = csv_reader.fieldnames
        table_data = [row.values()
                      for row in csv_reader
                      ]
        # Files with either be in csv or txt format
        table_title = os.path.basename(filename.replace(".txt", "").replace(".csv", ""))
        return table_title, table_fields, table_data


def med_admin_table_info(conn):
    cur = conn.cursor()
    # Create MedAdminName Table from EdMedication Table and MedicationAdmin tables
    medication_sql = 'SELECT DISTINCT MEDICATION_ID, MedIndexName, MedRoute, THERACLASS FROM Medication'
    cur.execute(medication_sql)
    medication_info = dict()
    medications = cur.fetchall()
    for medication in medications:
        med_id = medication[0]
        med_name = medication[1]
        med_route = medication[2]
        med_class = medication[3]
        if med_route:
            medication_info[med_id] = {'name': med_name,
                                       'route': med_route,
                                       'class': med_class
                                       }
    # TODO: Instead of using * list the fields so its easier to see what fields are used
    medication_admin_sql = 'SELECT MEDICATION_ID, ACTIONTAKEN, DOSE FROM MEDADMINS'
    cur.execute(medication_admin_sql)
    medication_admins = cur.fetchall()
    medication_admins_with_name_and_route = list()
    for medication_admin in medication_admins:
        try:
            med_id = medication_admin[0]
            action_taken = medication_admin[1]
            med_dose = medication_admin[2]
            med_route = medication_info[med_id]['route']  # Some meds won't have a route because they weren't given
            med_name = medication_info[med_id]['name']
            med_class = medication_info[med_id]['class']
            # Do to the way we produce the list. These medications don't have class information in the table
            if med_name.lower().find('ampicillin-sulbactam') != -1 or med_name.lower().find('azithromycin') != -1:
                med_class = 'ANTIBIOTICS'
                med_route = 'IV'
            if med_name.lower().find('peramivir') != -1:
                med_class = 'ANTIVIRALS'
                med_route = 'IV'

            # add name, route , and class fields to medication_admin fields
            # Med doses that are empty or 0 are are entries in the tables that don't represent a given medication
            if action_taken not in ("Canceled Entry", "Missed", "Refused") and med_dose not in ("", "0"):
                medication_admin = list(medication_admin) + [med_name] + [med_route] + [med_class]
                medication_admins_with_name_and_route.append(medication_admin)
        except KeyError:
            # Skip meds that don't have route information
            print("did not have a route for {}".format(medication_admin))
            continue

    medication_admin_name_table_fields = ['medication_id', 'ActionTaken', 'Dose', 'medindexname', 'medroute',
                                          'theraclass'
                                          ]
    table_title = "MedAdminName"
    table_fields = medication_admin_name_table_fields
    table_data = medication_admins_with_name_and_route
    return table_title, table_fields, table_data


def get_data_from_sql_table(conn, sql):
    """
    Executes a given sql command on a given database
    :param conn: connection to database to execute command
    :param sql: sql to execute
    :return: iterer of tuple containing the data return from command
    """

    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


def create_tables(conn, base_dir):
    # create_tables(conn)
    # base_dir = os.path.dirname(__file__)
    data_file_path = os.path.join(base_dir, 'Linking_Log', 'Place_Text_Files_Here')
    study_id_path = os.path.join(base_dir, 'Linking_Log', 'study_ids_to_pull.csv')
    data_files = [os.path.join(data_file_path, filename)
                  for filename in os.listdir(data_file_path)
                  if filename.endswith("txt")]
    # Create Study ID table
    table_title, table_fields, table_data = get_sql_data_from_file(study_id_path, delimiter=',')
    create_table(conn, table_title, table_fields, table_data)
    # Create Tables from data pulled from EPIC
    for filename in data_files:
        table_title, table_fields, table_data = get_sql_data_from_file(filename)
        create_table(conn, table_title, table_fields, table_data)

    # Create Table MedAdminName which combines given medications with their name and route information
    table_title, table_fields, table_data = med_admin_table_info(conn)
    create_table(conn, table_title, table_fields, table_data)


def main():
    conn = sqlite3.connect(
        '/home/beliefs22/PycharmProjects/EDEnrollmentDataNormalization-working/test.db')
    create_tables(conn)


if __name__ == "__main__":
    main()
