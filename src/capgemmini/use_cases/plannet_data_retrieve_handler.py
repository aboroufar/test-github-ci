import time
from logging import Logger
from typing import Union

import plannet_client
from chandra.rest_adapters.swagger_rest_adapter.api_client import ApiClient
from chandra.rest_adapters.swagger_rest_adapter.configuration import (
    ExtendedClientConfiguration,
)
from chandra.utils.api_client_utils import ApiClientUtils
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
            plannet_client.Configuration(),
            client_settings=self.client_settings.plannet_client_settings,
        )
        api_client = ApiClient(
            configuration=configuration,
            logger=self.logger,
        )
        api_dcim_instance = plannet_client.DcimApi(api_client)
        # api_circuits_instance = plannet_client.CircuitsApi(api_client)
        # api_logical_instance = plannet_client.LogicalApi(api_client)

        api_dcim_instance.dcim_nes_read(id=2)
        results = api_dcim_instance.dcim_interfaces_read(id=2)

        self.logger.info(results)

        jobs = [
            ApiClientUtils.perform_async_call(api_dcim_instance.dcim_nes_read)(id=2),
            ApiClientUtils.perform_async_call(api_dcim_instance.dcim_interfaces_read)(
                id=2
            ),
            ApiClientUtils.perform_async_call(api_dcim_instance.dcim_interfaces_read)(
                id=909837754875
            ),
        ]

        while not all(job.is_finished or job.is_failed for job in jobs):
            time.sleep(0.5)

        for job in jobs:
            if job.is_finished:
                self.logger.info(f"Job {job.id} successful")
            elif job.is_failed:
                self.logger.error(f"Job {job.id} failed")
        """
        try:
            for obj_id in range(1, 10):
                self.logger.info("GET bandwidth data")
                api_response = api_circuits_instance.circuits_bandwidth_read(id=obj_id)
                self.logger.info(api_response)
                self.logger.info("GET card types data read")
                api_response = api_dcim_instance.dcim_card_types_read(id=obj_id)
                self.logger.info(api_response)
                self.logger.info("GET card roles data")
                api_responses = api_dcim_instance.dcim_card_roles_list()
                self.logger.info(api_responses)
                self.logger.info("GET TG data")
                api_response = api_dcim_instance.dcim_tgs_read(id=obj_id)
                self.logger.info(api_response)
                self.logger.info("GET card types data")
                api_response = api_dcim_instance.dcim_card_types_list()
                self.logger.info(api_response)
                self.logger.info("GET card data")
                api_response = api_dcim_instance.dcim_cards_read(id=obj_id)
                self.logger.info(api_response)
                self.logger.info("GET interface link data")
                api_response = api_dcim_instance.dcim_interface_links_read(id=obj_id)
                self.logger.info(api_response)
                self.logger.info("GET interface type data")
                api_response = api_dcim_instance.dcim_interface_type_list()
                self.logger.info(api_response)
                self.logger.info("GET interfaces data")
                api_response = api_dcim_instance.dcim_interfaces_read(id=obj_id)
                self.logger.info(api_response)
                self.logger.info("GET ne-roles data")
                api_response = api_dcim_instance.dcim_ne_roles_list()
                self.logger.info(api_response)
                self.logger.info("GET ne-types data")
                api_response = api_dcim_instance.dcim_ne_types_list()
                self.logger.info(api_response)
                self.logger.info("GET ne data")
                api_response = api_dcim_instance.dcim_nes_read(id=obj_id)
                self.logger.info(api_response)
                self.logger.info("GET region data")
                api_response = api_dcim_instance.dcim_regions_list()
                self.logger.info(api_response)
                self.logger.info("GET syte type data")
                api_response = api_dcim_instance.dcim_site_types_list()
                self.logger.info(api_response)
                self.logger.info("GET site data")
                api_response = api_dcim_instance.dcim_sites_read(id=obj_id)
                self.logger.info(api_response)
                self.logger.info("GET slot data")
                api_response = api_dcim_instance.dcim_slots_read(id=obj_id)
                self.logger.info(api_response)
                self.logger.info("GET TG resource data")
                api_response = api_dcim_instance.dcim_tg_resource_info_read(id=obj_id)
                self.logger.info(api_response)
                self.logger.info("GET topology data")
                api_response = api_logical_instance.logical_topologies_read(id=obj_id)
                self.logger.info(api_response)
        except ApiException as e:
            self.logger.error("Exception when calling Api: %s\n" % e)
        """


class PlannetManager:
    """PlannetManager for the vpws tracker."""

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
