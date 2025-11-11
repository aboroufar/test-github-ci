import logging.config
import os

import hydra
from omegaconf import DictConfig

from capgemmini.use_cases.multi_wrapper_retrieve_handler import (
    DataRetrieveHandler,
    MultiWrapperManager,
)


@hydra.main(
    version_base=None,
    config_path=os.environ.get("CONFPATH"),
    config_name="multi_wrapper_config.yaml",
)  # type: ignore
def main(cfg: DictConfig) -> None:
    """Main function to run the data retrieve a pipeline."""
    logger = logging.getLogger(__name__)
    data_retrieve_manager = MultiWrapperManager()
    handler = DataRetrieveHandler(client_settings=cfg, logger=logger)
    data_retrieve_manager.handler = handler
    data_retrieve_manager.run_data_retrieve_pipeline()


if __name__ == "__main__":
    main()
