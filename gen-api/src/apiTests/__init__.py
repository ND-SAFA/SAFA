from dotenv import load_dotenv

from tgen.common.constants import environment_constants

load_dotenv()
environment_constants.IS_TEST = True
