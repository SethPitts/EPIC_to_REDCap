from datetime import datetime


class ADT:
    """Represents Admit and Discharge Times

    Args:
        date (str): date of arrival or discharge
        time (str): time of arrival or discharge
        status (str): arrival or discharge
        dispo (str): patients final disposition

    Attributes:
        date (str): date of arrival or dishcarge
        time (str): time of arrival or discharge
        status (str): tells if this represents and arrival or discharge
        dispo (str): the patients final disposition can be ADMIT, DISCHARGE,
            Hospital Observation, or Screened and Left
    """

    def __init__(self, date, time, status, dispo):
        self._date = date
        self._time = time
        self._status = status
        self._dispo = dispo
        
    @property
    def date(self):
        """str: date of arrival or discharge"""
        return self._date

    @property
    def time(self):
        """str: time of arrival or discharge"""
        return self._time

    @property
    def status(self):
        """str: tells if this represents an arrival or discharge"""
        return self._status

    @property
    def dispo(self):
        """str: final dispotion of the patient"""
        return self._dispo


class Vitals:
    """Represents a Vital sign value
    Args:
        flowsheet_name (str): the name of the lab: Temp, BP, Pulse, etc
        value (str): the value of the vital sign: 35.5
        date_time (str): the lab collect date and time YYYY-MM-DD H:M:S

    Attributes:
        flowsheet_name(str): the name of the vital sign: Pulse, BP, etc
        value (str): the result of the vital sign: 7.35
        date_time (str): the time the vital sign was taken YYYY-MM-DD HH:MM:SS
        date (str): date the vital sign was collected
        time (str): time the vital sign was collected

        """

    def __init__(self, flowsheet_name, date_time, value):
        self._flowsheet_name = flowsheet_name
        self._date_time = date_time
        self._value = value
        self._date, self._time = date_time.split(" ")

    @property
    def value(self):
        """str: the vital sign result"""
        return self._value

    @property
    def date_time(self):
        """str: the date and time the vital sign was collected
        YYYY-MM-DD HH:MM:SS"""
        return self._date_time

    @property
    def date(self):
        """str: the date the vital sign was collected YYYY-MM-DD"""
        return self._date

    @property
    def time(self):
        """str: the time the vital sign was collected HH:MM:SS"""
        return self._time

    @property
    def flowsheet_name(self):
        """str: the component being resulted: Sodium"""
        return self._flowsheet_name

    def check_time(self, time_to_check):
        """Checks if vital sign value was taken before a given time

        Args:
            time_to_check (str): time the vital sign should be collected before
            generally the discharge time
        """
        
        time_to_check = datetime.strptime(time_to_check, '%Y-%m-%d %H:%M:%S')
        lab_time = datetime.strptime(self._date_time, '%Y-%m-%d %H:%M:%S')

        return time_to_check >= lab_time


class Lab:
    """Represents a Lab value
    Args:
        value (str): the result of the lab: 35.5
        date_time (str): the lab collect date and time YYYY-MM-DD H:M:S
        labname (str): the name of the lab: Complete Blood Count
        componentname (str): the lab component resulted: Hematocrit

    Attributes:
        value (str): the result of the lab: No DNA Detected
        date_time (str): the lab collect date and time YYYY-MM-DD HH:MM:SS
        date (str): date the lab was collected
        time (str): time the lab was collected
        labname (str): the name of the lab: Resp Virus Complex
        componentname (str): the lab component resulted: Influenza A
        """

    def __init__(self, value, collect_date_time, result_date_time, labname, componentname):
        self._value = value
        self._collect_date_time = collect_date_time
        self._result_date_time = result_date_time
        self._date, self._time = collect_date_time.split(" ")
        self._componentname = componentname
        self._labname = labname

    @property
    def value(self):
        """str: the lab result"""
        return self._value

    @property
    def collect_date_time(self):
        """str: the date and time the lab was collected YYYY-MM-DD HH:MM:SS"""
        return self._collect_date_time

    @property
    def result_date_time(self):
        """str: the date and time the lab was result YYYY-MM-DD HH:MM:SS"""
        return self._result_date_time

    @property
    def date(self):
        """str: the date the lab was collected YYYY-MM-DD"""
        return self._date

    @property
    def time(self):
        """str: the time the lab was collected HH:MM:SS"""
        return self._time

    @property
    def componentname(self):
        """str: the component being resulted: Sodium"""
        return self._componentname

    @property
    def labname(self):
        """str: the name of lab: Complete Metaboloic Panel"""
        return self._labname

    def check_time(self, time_to_check):
        """Checks if lab value was resulted before a given time

        Args:
            time_to_check (str): time the lab should be collected before
            generally the discharge time
        """

        time_to_check = datetime.strptime(time_to_check, '%Y-%m-%d %H:%M:%S')
        lab_time = datetime.strptime(self._collect_date_time, '%Y-%m-%d %H:%M:%S')
        return time_to_check >= lab_time
class Medication:
    """Represents a base medication class for other to inherit from

    Args:
        name (str): name of the medication
        date_time (str): the date and time the medication was ordered
            YYYY-MM-DD HH:MM:SS
        route (str): medication admin route: oral, IV, IM
        theraclass (str): the medications class: ANTIVIAL, ANTIBIOTIC etc
        outpt_inpt (str): tells if the medication was ordered in the hospittal
            or ordered for discharge
    Attributes:
        name (str): name of the medication
        date_time (str): the lab collect date and time YYYY-MM-DD HH:MM:SS
        date (str): date the lab was collected
        time (str): time the lab was collected
        route (str): medication admin route: oral, IV, IM
        theraclass (str): the medications class: ANTIVIRAL, ANTIBIOTIC, ect
        outpt_inpt (str): ordered in the hospital or for discharge
        """

    def __init__(self, name, date_time, route):
        self._name = name
        self._date_time = date_time
        self._date, self._time = date_time.split(" ")
        self._route = route

    @property
    def name(self):
        """str: name of the medication"""
        return self._name

    @property
    def date_time(self):
        """str: date and time medication was ordered YYYY-MM-DD HH:MM:SS"""
        return self._date_time

    @property
    def date(self):
        """str: date the medication was ordered"""
        return self._date

    @property
    def time(self):
        """str: time the lab was ordered"""
        return self._time

    @property
    def route(self):
        """str: med admin route"""
        return self._route

    def check_time(self, time_to_check):
        """Checks if medication was ordered before a given time

        Args:
            time_to_check (str): time the med should be ordered before
            generally the discharge time
        """

        time_to_check = datetime.strptime(time_to_check, '%Y-%m-%d %H:%M:%S')
        med_time = datetime.strptime(self._date_time, '%Y-%m-%d %H:%M:%S')
        return time_to_check >= med_time


class EdMedication(Medication):
    """Represents a medication that was given

    Args:
        name (str): name of the medication
        date_time (str): the date and time the medication was ordered
            YYYY-MM-DD HH:MM:SS
        route (str): medication admin route: oral, IV, IM
        theraclass (str): the medications class: ANTIVIAL, ANTIBIOTIC etc
        outpt_inpt (str): tells if the medication was ordered in the hospittal
            or ordered for discharge
    Attributes:
        name (str): name of the medication
        date_time (str): the lab collect date and time YYYY-MM-DD HH:MM:SS
        date (str): date the lab was collected
        time (str): time the lab was collected
        route (str): medication admin route: oral, IV, IM
        theraclass (str): the medications class: ANTIVIRAL, ANTIBIOTIC, ect
        outpt_inpt (str): ordered in the hospital or for discharge
        """

    def __init__(self, name, date_time, route, theraclass, outpt_inpt):
        super().__init__(name, date_time, route)
        self._theraclass = theraclass
        self._outpt_inpt = outpt_inpt

    @property
    def theraclass(self):
        """str: the medications class: ANTIVIRAL, ANTIBIOTIC, etc"""
        return self._theraclass

    @property
    def outpt_inpt(self):
        """str: tells if medication was ordered in hospital or for discharge"""
        return self._outpt_inpt

 
class Imaging:
    """Represents Imaging done

    Args:
        date_time (str): date and time imaging was done YYYY-MM-DD HH:MM:SS
        name (str): name of image: Chest XRAY , Chest CT
        status (str): completed or cancelled
        
    Attributes:
        date_time (str): date and time imaging was done YYYY-MM-DD HH:MM:SS
        date (str): date imaging was done YYYY-MM-DD
        time (str): time imaging was done HH:MM:SS
        name (str): name of image: Chest XRAY , Chest CT
        status (str): completed or cancelled
    """

    def __init__(self, name, date_time, status):
        self._name = name
        self._date_time = date_time
        self._date, self._time = date_time.split(" ")
        self._status = status

    @property
    def name(self):
        """str: name of the imaging test: Chest Xray, Chest CT"""
        return self._name

    @property
    def date(self):
        """str: date imaging was done"""
        return self._date

    @property
    def time(self):
        """str: time imaging was done"""
        return self._time

    @property
    def status(self):
        """str: tells if imaging was completed or cancelled"""
        return self._status

    @property
    def date_time(self):
        """str: date and time imaging was done YYYY-MM-DD HH:MM:SS"""
        return self._date_time

    def check_time(self, time_to_check):
        """Checks if image was resulted before a given time

        Args:
            time_to_check (str): time the image should be collected before
            generally the discharge time
        """
        
        time_to_check = datetime.strptime(time_to_check, '%Y-%m-%d %H:%M:%S')
        order_time = datetime.strptime(self._date_time, '%Y-%m-%d %H:%M:%S')
        return time_to_check >= order_time
