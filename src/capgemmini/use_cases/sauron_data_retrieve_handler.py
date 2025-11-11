from logging import Logger
from typing import Union

import sauron_client
from chandra.rest_adapters.swagger_rest_adapter.api_client import ApiClient
from chandra.rest_adapters.swagger_rest_adapter.configuration import (
    ExtendedClientConfiguration,
)
from chandra.rest_adapters.swagger_rest_adapter.rest import ApiException
from omegaconf import DictConfig


class DataRetrieveHandler:
    """DataRetrieveHandler for the vpws tracker."""

    def __init__(
        self,
        logger: Logger,
        client_settings: DictConfig,
    ):
        """Handler for the vpws tracker."""
        self.client_settings = client_settings
        self.logger = logger

    def data_retrieve_pipeline(self) -> None:
        """Run the data retrieve pipeline."""
        configuration = ExtendedClientConfiguration(
            sauron_client.Configuration(),
            client_settings=self.client_settings.sauron_client_settings,
        )
        api_client = ApiClient(
            configuration=configuration,
            logger=self.logger,
        )
        api_isp_asn = sauron_client.DeIspAsnApi(api_client)

        try:
            api_response = api_isp_asn.de_isp_asn_list()
            self.logger.info(api_response)
        except ApiException as e:
            self.logger.debug(
                "Exception when calling DeIspAsnApi->de_isp_asn_list: %s\n" % e
            )


class SauronManager:
    """Manager for the vpws tracker."""

    def __init__(self) -> None:
        """Manager for the vpws tracker."""
        self._handler: Union[DataRetrieveHandler, None] = None

    @property
    def handler(self) -> Union[DataRetrieveHandler, None]:
        """Handler for the vpws tracker."""
        return self._handler

    @handler.setter
    def handler(self, handler: Union[DataRetrieveHandler, None]) -> None:
        """Handler for the vpws tracker."""
        self._handler = handler

    def run_data_retrieve_pipeline(self) -> None:
        """Run the data retrieve pipeline."""
        if self.handler:
            self.handler.data_retrieve_pipeline()
