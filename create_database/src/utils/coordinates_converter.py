"""File containing the CoordinatesConverter class."""
from pyproj import Proj, Transformer


class CoordinatesConverter:
    """Class used to get the Transformer objects from specific types of projection."""
    def __init__(self) -> None:
        """
        Initialize the CoordinatesConverter class.

        :return: None.
        """
        self._lambert_proj = Proj('+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs')
        self._wgs84_proj = Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

    def lambert93_to_gps_transformer(self) -> Transformer:
        """
        Get the lambert93 to gps Transformer object.

        :return: The Transformer object.
        """
        return Transformer.from_proj(self._lambert_proj, self._wgs84_proj)

    def gps_to_lambert93_converter(self) -> Transformer:
        """
        Get the gps to lambert93 Transformer object.

        :return: The Transformer object.
        """
        return Transformer.from_proj(self._wgs84_proj, self._lambert_proj)
