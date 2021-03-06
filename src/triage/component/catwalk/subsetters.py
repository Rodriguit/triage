import logging

import pandas
from sqlalchemy.orm import sessionmaker

from triage.component.architect.entity_date_table_generators import EntityDateTableGenerator
from triage.component.catwalk.utils import (filename_friendly_hash, get_subset_table_name)
from triage.component.results_schema import Subset

class Subsetter(object):
    def __init__(
        self,
        db_engine,
        replace,
        as_of_times,
    ):
        self.db_engine = db_engine
        self.replace = replace
        self.as_of_times = as_of_times

    def generate_tasks(self, subset_configs):
        logging.info("Generating subset table creation tasks")
        subset_tasks = []
        for subset_config in subset_configs:
            if subset_config:
                subset_hash = filename_friendly_hash(subset_config)
                subset_table_generator = EntityDateTableGenerator(
                    entity_date_table_name=get_subset_table_name(subset_config),
                    db_engine=self.db_engine,
                    query=subset_config["query"],
                    replace=self.replace
                )
                subset_tasks.append(
                    {
                        "subset_config": subset_config,
                        "subset_hash": subset_hash,
                        "subset_table_generator": subset_table_generator,
                    }
                )
        return subset_tasks

    def process_all_tasks(self, tasks):
        for task in tasks:
            self.process_task(**task)

    def process_task(self, subset_config, subset_hash, subset_table_generator):
        logging.info(
            "Beginning subset creation for %s-%s",
            subset_config["name"],
            subset_hash
        )
        subset_table_generator.generate_entity_date_table(
            as_of_dates=self.as_of_times
        )
        self.save_subset_to_db(subset_hash, subset_config)

    def save_subset_to_db(self, subset_hash, subset_config):
        session = sessionmaker(bind=self.db_engine)()
        session.merge(Subset(subset_hash=subset_hash, config=subset_config))
        session.commit()
        session.close()
