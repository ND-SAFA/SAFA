from enum import Enum


class InteractiveModeOptions(Enum):
    RE_RUN = "Re-run current step"
    NEXT_STEP = "Continue to next step"
    SKIP_STEP = "Skip next step"
    QUIT = "Quit"
    LOAD_NEW_STATE = "Load new state"
    TURN_OFF_INTERACTIVE = "Turn off interactive"
    LOAD_EXTERNAL_STATE = "Load external state"
    DO_NOT_RESUME = "Do not resume"
    DELETE_MODEL_OUTPUT = "Delete previous model output"

