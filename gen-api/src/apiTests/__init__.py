from dotenv import load_dotenv

from gen_common.constants import environment_constants

load_dotenv()
environment_constants.IS_TEST = True
