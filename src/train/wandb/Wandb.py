import json
import os
from typing import Dict, Union

from constants import BASE_EXPERIMENT_NAME, EXPERIMENTAL_VARS_IGNORE


class Wandb:
    """
    Provides utility methods for setting up run for weights and biases.
    """

    @staticmethod
    def get_run_name(experimental_vars: Dict) -> str:
        """
        Returns the name of the run by parsing experimental variables.
        :param experimental_vars: The variables used to identify this run.
        :return: String representing run name.
        """
        clean_vars = Wandb.get_clean_vars(experimental_vars)
        return json.dumps(clean_vars)

    @staticmethod
    def get_clean_vars(experimental_vars: Dict) -> Union[Dict, str]:
        """
        Cleans experimental variables to be presented on wandb.
        :param experimental_vars: The experimental variables to clean.
        :return: Cleaned experimental variables.
        """
        if experimental_vars is None or len(experimental_vars) == 0:
            return BASE_EXPERIMENT_NAME
        if isinstance(experimental_vars, str):
            return experimental_vars

        return {k: Wandb.clean_var(v) for k, v in experimental_vars.items() if k not in EXPERIMENTAL_VARS_IGNORE}

    @staticmethod
    def clean_var(v: str):
        """
        Cleans the given variable to fix nicely with WandB.
        :param v: The variable to clean.
        :return: The cleaned variable.
        """
        if isinstance(v, str) and "/" in v:
            v = os.path.split(v)[1]
        if isinstance(v, float):
            v = round(v, 2)
        return v
