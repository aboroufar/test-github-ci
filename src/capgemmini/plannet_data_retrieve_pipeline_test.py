import logging.config
import os

import hydra
from omegaconf import DictConfig

from capgemmini.use_cases.plannet_data_retrieve_handler import (
    DataRetrieveHandler,
    PlannetManager,
)


@hydra.main(
    version_base=None,
    config_path=os.environ.get("CONFPATH"),
    config_name="plannet_wrapper_config_test",
)  # type: ignore
def main(cfg: DictConfig) -> None:
    """Main function to run the data retrieve a pipeline."""
    logger = logging.getLogger(__name__)
    data_retrieve_manager = PlannetManager()
    handler = DataRetrieveHandler(client_settings=cfg, logger=logger)
    data_retrieve_manager.handler = handler
    data_retrieve_manager.run_data_retrieve_pipeline()


if __name__ == "__main__":
    main()
