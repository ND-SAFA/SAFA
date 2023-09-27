from enum import Enum


class InteractiveModeOptions(Enum):
    RE_RUN = "Re-run current step"
    NEXT_STEP = "Continue to next step"
    SKIP_STEP = "Skip next step"
    QUIT = "Quit"
    LOAD_NEW_STATE = "Load new state"
