from logging import Logger
from typing import Union

import horizon_client
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
            horizon_client.Configuration(),
            client_settings=self.client_settings.horizon_client_settings,
        )
        api_client = ApiClient(configuration)

        api_instance = horizon_client.ApiApi(api_client)

        try:
            api_response = api_instance.api_base_deliverable_list()
            self.logger.info(api_response)
        except ApiException as e:
            self.logger.error(
                "Exception when calling ApiApi->api_base_payload_template_read: %s\n"
                % e
            )


class HorizonManager:
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
