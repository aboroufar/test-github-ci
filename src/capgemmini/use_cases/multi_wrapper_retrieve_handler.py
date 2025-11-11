import logging.config
from typing import Union

import horizon_client
import plannet_client
import sauron_client
from chandra.rest_adapters.swagger_rest_adapter.api_client import ApiClient
from chandra.rest_adapters.swagger_rest_adapter.configuration import (
    ExtendedClientConfiguration,
)
from chandra.rest_adapters.swagger_rest_adapter.rest import ApiException
from chandra.utils.api_client_utils import ApiClientUtils
from omegaconf import DictConfig


class DataRetrieveHandler:
    """Handler for test retrieve test."""

    def __init__(
        self,
        logger: logging.Logger,
        client_settings: DictConfig,
    ):
        """Data retrieve handler for the multiwrapper test pipeline."""
        self.client_settings = client_settings
        self.logger = logger

    def data_retrieve_pipeline(self) -> None:
        """Run the data retrieve pipeline."""
        sauron_conf = ExtendedClientConfiguration(
            sauron_client.Configuration(),
            client_settings=self.client_settings.sauron_client_settings,
        )
        sauron_chandra = ApiClient(
            configuration=sauron_conf,
            logger=self.logger,
        )
        group_pnt = sauron_client.GroupPntPlanRecordApi(sauron_chandra)

        us_weekly = sauron_client.UsCdnApiSummaryWeeklyApi(sauron_chandra)

        plannet_conf = ExtendedClientConfiguration(
            plannet_client.Configuration(),
            client_settings=self.client_settings.plannet_client_settings,
        )
        plannet_chandra = ApiClient(
            configuration=plannet_conf,
            logger=self.logger,
        )
        api_dcim_instance = plannet_client.DcimApi(plannet_chandra)

        horizon_conf = ExtendedClientConfiguration(
            horizon_client.Configuration(),
            client_settings=self.client_settings.horizon_client_settings,
        )
        horizon_chandra = ApiClient(
            configuration=horizon_conf,
            logger=self.logger,
        )
        api_api_instance = horizon_client.ApiApi(horizon_chandra)

        try:
            sauron_chandra.stale_redis_cache_on()
            horizon_chandra.stale_redis_cache_on()
            plannet_chandra.stale_redis_cache_on()

            for _ in range(1, 30):
                self.logger.info("START SAURON RETRIEVE ----  \n\n")
                group_pnt.group_pnt_plan_record_list()
                us_weekly.us_cdn_api_summary_weekly_list()
                self.logger.info("START HORIZON RETRIEVE ----  \n\n")
                api_api_instance.api_base_deliverable_list()
                self.logger.info("START PLANNET RETRIEVE ----  \n\n")
                api_dcim_instance.dcim_asns_list()
                # sync call
                api_dcim_instance.dcim_card_types_read(id=151)
                # 404 Not found error sync call
                api_dcim_instance.dcim_card_types_read(id=999999)
                # async call
                ApiClientUtils.perform_async_call(
                    api_dcim_instance.dcim_card_types_read
                )(id=151)
                # 404 Didn't find error async call
                ApiClientUtils.perform_async_call(
                    api_dcim_instance.dcim_card_types_read
                )(id=999999)

        except ApiException as e:
            self.logger.error("Exception when calling Api: %s\n" % e)


class MultiWrapperManager:
    """Manager for a multi wrapper test pipeline."""

    def __init__(self) -> None:
        """Init method for handler."""
        self._handler: Union[DataRetrieveHandler, None] = None

    @property
    def handler(self) -> Union[DataRetrieveHandler, None]:
        """Service handler for the vpws tracker."""
        return self._handler

    @handler.setter
    def handler(self, handler: Union[DataRetrieveHandler, None]) -> None:
        """Service handler for the multi wrapper test pipeline."""
        self._handler = handler

    def run_data_retrieve_pipeline(self) -> None:
        """Run the data retrieve pipeline."""
        if self.handler:
            self.handler.data_retrieve_pipeline()
