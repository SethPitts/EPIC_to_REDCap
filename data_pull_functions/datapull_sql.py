import sqlite3

# TODO: Combine the arrival date and time into one pull
def arrival_date_time(subject_id, conn):
    """Gets arrival date and time from the demographics table
    Args:
        subject_id (str): the id of the subject whose data you are searching for
        conn (:obj: `database connection`): connection to the database that
            contains the patient data

    Returns:
        date (str): subjects arrival date
        time (str): subjects arrival time
        arrival (str): used in ADT object to indicate the object is for an
            arrrival
        dispo (str): subjects final disposition
    """
    cur = conn.cursor()
    sql = """SELECT ADT_ARRIVAL_TIME, EDDisposition FROM DEMOGRAPHICS
          WHERE STUDYID = {}""".format(subject_id)
    cur.execute(sql)
    data = cur.fetchall()
    if data:
        date, time = data[0][0].split(" ")
        dispo = data[0][1]
    return date, time, 'arrival', dispo


def discharge_date_time(subject_id, conn):
    """Gets discharge date and time from the demographics table
    Args:
        subject_id (str): the id of the subject whose data you are searching for
        conn (:obj: `database connection`): connection to the database that
            contains the patient data

    Returns:
        date (str): subjects discharge date
        time (str): subjects discharge time
        arrival (str): used in ADT object to indicate the object is for an
            discharge
        dispo (str): subjects final disposition
    """
    cur = conn.cursor()
    sql = """SELECT ED_DEPARTURE_TIME, EDDisposition FROM DEMOGRAPHICS
          WHERE STUDYID = {}""".format(subject_id)
    cur.execute(sql)
    data = cur.fetchall()
    if data[0][0]:  # subjects who were discharged from the ED
        date, time = data[0][0].split(" ")
        dispo = data[0][1]
        return date, time, 'discharge', dispo
    else:  # Subjects who were admitted
        sql = """SELECT HOSP_ADMSN_TIME, EDDisposition FROM DEMOGRAPHICS
          WHERE STUDYID = {}""".format(subject_id)
        cur.execute(sql)
        data = cur.fetchall()
        if data[0][0]:
            date, time = data[0][0].split(" ")
            dispo = data[0][1]
            return date, time, 'discharge', dispo

# TODO: Can we combine multiple functions into one by sending the sql as a parameter
# TODO: can we use pull_name for the arrival and discharge test so we can combine all into one


def generic_pull(conn, sql, pull_name):
    print('Running Sql for {}'.format(pull_name))
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    return data, pull_name



def main():
    conn = sqlite3.connect(r'test.db')
    # Get subject IDs
    cur = conn.cursor()
    sql = """SELECT DISTINCT STUDYID FROM DEMOGRAPHICS"""
    cur.execute(sql)
    subject_ids = cur.fetchall()
    conn.close()


if __name__ == "__main__":
    main()
