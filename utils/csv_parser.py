"""File containing the SitesMobileCsvConverter class."""
from pathlib import Path
from typing import Dict
from logging import Logger
import pandas as pd
from utils.api_adresse import ApiAdresse
from utils.coordinates_converter import CoordinatesConverter


class SitesMobileCsvConverter():
    """Class used to convert the input csv with mobile sites data."""
    def __init__(self, mobile_csv_path: Path, logger: Logger, separator: str = ",") -> None:
        """
        Initialize the MobileSitesCsvConverter class.

        :param mobile_csv_path: Path to the csv file containing the mobile sites data.
        :param logger: Logger object.
        :param separator: Separator used on the csv file (',' by default).
        :return: None.
        """
        self._logger = logger
        self._operator_names: Dict[str, str] = self._get_operator_name_dict()
        self._transformer = CoordinatesConverter().lambert93_to_gps_transformer()
        self._df_to_convert = pd.read_csv(mobile_csv_path, sep=separator, dtype=str).dropna()

    def _get_operator_name_dict(self) -> Dict[str, str]:
        """
        Get mobile network code table from wiki page.

        :return: A dictionary used to get the operator name from its code.
        """
        self._logger.debug("Converting provider code into operator name.")
        ref_wiki_page: str = "https://fr.wikipedia.org/wiki/Mobile_Network_Code#Tableau_des_MNC_pour_la_France_m%C3%A9tropolitaine"
        mnc_table = pd.read_html(ref_wiki_page, header=0)[0]

        operator_name = {}
        for _, row in mnc_table.iterrows():
            provider_code = str(row["MCC"]) + str(row["MNC[3]"]).zfill(2)
            operator_name[provider_code] = row["Opérateur"] if row["Opérateur"] else row["Marque"]

        return operator_name

    def save_input_csv(self, file_path: Path = Path("input.csv")) -> Path:
        """
        Create a new dataframe from the original one with the fields:
        'operator_name', 'lon', 'lat', '2G', '3G' and '4G'.
        And then export it as a csv that will be used as input for the 'ApiAdresse'

        :param file_path: path to the csv file to be exported.
        :return: The file path.
        """
        self._logger.debug("Creating input csv to make the request to 'Adresse API'.")
        converted_data = []
        for _, row in self._df_to_convert.iterrows():
            operator_name: str = self._operator_names[row["Operateur"]]
            long, lat = list(self._transformer.transform(row["x"], row["y"]))
            converted_data.append([
                operator_name, long, lat, row["2G"], row["3G"], row["4G"]
                ])

        pd.DataFrame(converted_data,
                     columns=["operator_name", "lon", "lat", "2G", "3G", "4G"]
                     ).to_csv(file_path, index=False)

        return file_path

    def save_adresse_request_csv(self, input_file_path: Path, 
                                 file_path: Path = Path("output.csv")) -> Path:
        """
        Make a 'reverse csv' request to the 'API Adresse' and save the result to a csv file.
        
        :param input_file_path: Path for the input csv to make the request.
        :param output_file_path: Path for the file where the output csv that will be saved.
        :return: The file path.
        """
        self._logger.debug("Making the request with the input file and saving the output csv.")
        api_adresse = ApiAdresse(self._logger)

        requested_reverse_csv = api_adresse.reverse_csv(csv_file=input_file_path, timeout=10)

        with open(file_path, 'wb') as file:
            file.write(requested_reverse_csv)

        return file_path

    def convert_csv_to_dict(self, response_reverse_csv_path: Path) -> Dict:
        """
        Parse the response csv and make a dict with it to be used to create the database.

        :param response_reverse_csv_path: Path to the csv acquired with the 'API adresse'.
        :return: The converted dict
        """
        self._logger.debug("Converting the output file into dict.")
        df = pd.read_csv(response_reverse_csv_path, dtype=str)
        df = df[df["result_status"] != "not-found"]

        signal_dict = {}

        for _, row in df.iterrows():
            operator_name = row['operator_name']
            city_code = row['result_citycode']
            signal_2g = int(row['2G'])
            signal_3g = int(row['3G'])
            signal_4g = int(row['4G'])

            if city_code not in signal_dict:
                signal_dict[row["result_citycode"]] = {}

            if operator_name not in signal_dict[city_code]:
                signal_dict[city_code][operator_name] = {"2G": False, "3G": False, "4G": False}

            if signal_2g:
                signal_dict[city_code][operator_name]["2G"] = True
            if signal_3g:
                signal_dict[city_code][operator_name]["3G"] = True
            if signal_4g:
                signal_dict[city_code][operator_name]["4G"] = True

        signal_documents = []

        for city_code, signal_data in signal_dict.items():
            signal_documents.append({"city_code": city_code, "signal_data": signal_data})

        return signal_documents
