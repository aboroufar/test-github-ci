import logging.config
import os

import hydra
from omegaconf import DictConfig

from capgemmini.use_cases.sauron_data_retrieve_handler import (
    DataRetrieveHandler,
    SauronManager,
)


@hydra.main(
    version_base=None,
    config_path=os.environ.get("CONFPATH"),
    config_name="sauron_wrapper_config_test",
)  # type: ignore
def main(cfg: DictConfig) -> None:
    """Main function to run the data retrieve a pipeline."""
    logger = logging.getLogger(__name__)
    data_retrieve_manager = SauronManager()
    handler = DataRetrieveHandler(
        client_settings=cfg,
        logger=logger,
    )
    data_retrieve_manager.handler = handler
    data_retrieve_manager.run_data_retrieve_pipeline()


if __name__ == "__main__":
    main()
