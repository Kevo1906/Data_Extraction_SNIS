import os
from robots.SNIS import SNIS

# URL of the website from which the data will be downloaded
URL = "https://estadisticas.minsalud.gob.bo/Reportes_Dinamicos/Menu_rep_dinamicos.aspx"
# Path to save the downloaded files
PATH = os.path.join(os.getcwd(),"downloads")
# Filters to be applied when downloading the data
FILTERS_ORDER = ['subsector', 'ambito', 'establecimiento', 'nivel',
                 'tipo', 'institucion', 'municipio', 'provincia', 'semana', 'mes']
# Variables to search for, along with their respective codes
VARIABLES_SEARCHED = [
    {
        "code": "01",
        "key_words": "sospecha diagnostica"
    },
    {
        "code": "04",
        "key_words": "inmunoprevenibles"
    },
    {
        "code":"05",
            "key_words":"infecc sexual"
    },
    {
        "code":"06",
            "key_words":"otras infecciones"
    },
    {
        "code":"07",
            "key_words":"tuberculosis lepra"
    }
]
# Form code to be used
FORM_CODE='302'
# Year for which the data is being searched
YEAR=2024


if __name__ == '__main__':
    # Create the downloads folder if it does not exist
    os.makedirs(PATH,exist_ok=True)

    # Instantiate the SNIS robot
    robot = SNIS()

    # Iterate through the variables to search for
    for element in VARIABLES_SEARCHED:
        print(f"Processing variable: {element['key_words']} (Code: {element['code']})")
        # Verify if the URL is accessible
        if robot.verify_url(url=URL):
            # Download the data and get the temporary path
            tmp_path = robot.verify_download(main_url=URL, path=PATH, filters_order=FILTERS_ORDER, variable=element, form_code=FORM_CODE,year=YEAR)
            print(f"Downloaded data for {element['key_words']} to temporary path: {tmp_path}")

            # Store the new data
            robot.store_new_data(path=PATH, tmp_path=tmp_path, last_file_path="-",ALL=True)
            print(f"Stored new data for {element['key_words']} in: {PATH}")
            
        else:
            print(f"Invalid URL: {URL}")
