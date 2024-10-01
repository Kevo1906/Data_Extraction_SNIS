import csv
import random
import os
from datetime import datetime
import calendar

def get_proxy():
    """
    Retrieves a random proxy from the 'Verified_proxys.csv' file along with predefined headers.

    Returns:
        dict: A dictionary containing the proxy and headers.
            {
                'proxy': str,  # Randomly selected proxy
                'header': {
                    'User-Agent': str,  # User-Agent header
                    'Accept': str,  # Accept header
                    'Accept-Encoding': str,  # Accept-Encoding header
                    'Accept-Language': str,  # Accept-Language header
                }
            }
    """
    with open('Verified_proxys.csv', 'r') as f:
        reader = csv.reader(f)
        lines = list(reader)
        random_proxy = random.choice(lines)[0]
        return {
            'proxy': random_proxy,
            'header': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9',
            }
        }


def createDirectoryStruct(file_date, base_path, publication_frequency, format='%Y-%m-%d'):
    """
    Creates directory structure where the file will be saved.

    Args:
        file_date (str): Date of the file data, expressed in YYYY-MM-DD format.
        base_path (str): Base path where the files will be stored.
        publication_frequency (str): Frequency of data of the file.
        format (str, optional): Format of the date string. Defaults to '%Y-%m-%d'.

    Returns:
        str: Absolute path of the created directory structure.
    """
    level_1_frecuency = ['mensual', 'trimestral', 'semestral', 'anual']
    level_2_frecuency = ['diario', 'semanal']

    try:

        fileDate = datetime.strptime(file_date, format) if isinstance(file_date,str) else file_date

    except ValueError as e:
        print(f"Date can not be procesed")
        return base_path

    if publication_frequency.lower() in level_2_frecuency:
        # For daily and weekly frequency, create directory structure up to month level
        filePath = os.path.join(base_path, str(fileDate.year))
        filePath = os.path.join(filePath, str(
            fileDate.year) + "-" + str("%02d" % (fileDate.month,)))
    elif publication_frequency.lower() in level_1_frecuency:
        # For monthly, quarterly, semi-annual, and annual frequency, create directory structure up to year level
        filePath = os.path.join(base_path, str(fileDate.year))
    else:
        # If the publication frequency is not recognized, return base path
        filePath = base_path
        print("Publication frecuency uwknomed")
    # Create the directory if it doesn't exist
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    return filePath


# * ESPECIFIC FUCNTIONS

def format_date(date, format='%Y-%m-%d'):
    """
    Formats the given date string into a datetime object.

    Args:
        date (str): The date string to be formatted.
        format (str): The format of the date string. Default is '%Y-%m-%d'.

    Returns:
        datetime.datetime: The formatted datetime object.
    """
    try:
        # Convert updated_to string to datetime object
        date_formated = datetime.strptime(date, format)
        return date_formated
    except ValueError as e:
        print(f"Date can not be procesed")
        return date


def month_to_number(month):
    """
    Converts a month name into its corresponding number.

    Args:
        month (str): The name of the month.

    Returns:
        int: The numerical representation of the month (1 for January, 2 for February, etc.).
            Returns None if the given month name is not found.
    """
    months = {
        "enero": 1,
        "febrero": 2,
        "marzo": 3,
        "abril": 4,
        "mayo": 5,
        "junio": 6,
        "julio": 7,
        "agosto": 8,
        "septiembre": 9,
        "octubre": 10,
        "noviembre": 11,
        "diciembre": 12
    }

    return months.get(month.lower())


def month_abr_to_number(month):
    """
    Converts an abbreviated month name into its corresponding number.

    Args:
        month (str): The abbreviated name of the month.

    Returns:
        int: The numerical representation of the month (1 for January, 2 for February, etc.).
            Returns None if the given month abbreviation is not found.
    """
    months = {
        "ENE": 1,
        "FEB": 2,
        "MAR": 3,
        "ABR": 4,
        "MAY": 5,
        "JUN": 6,
        "JUL": 7,
        "AGO": 8,
        "SEP": 9,
        "OCT": 10,
        "NOV": 11,
        "DIC": 12,
        "JAN": 1,
        "APR": 4,
        "AUG": 8,
        "DEC": 12,
        "SET":9
    }

    return months.get(month.upper())

def last_day_month(year, month):
    """
    Returns the last day of the given month and year.

    Args:
        year (int): The year.
        month (int): The month.

    Returns:
        int: The last day of the month.
    """
    return calendar.monthrange(year, month)[1]

def get_departamento_abr(dep):
    dep = dep.strip().lower()
    departamentos_dict = {
    "la paz": "lp",
    "santa cruz": "sc",
    "cochabamba": "cb",
    "oruro": "or",
    "potosi": "pt",
    "chuquisaca": "ch",
    "tarija": "tj",
    "beni": "bn",
    "pando": "pd"
}
    return departamentos_dict[dep]