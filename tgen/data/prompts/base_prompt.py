from enum import Enum


class BasePrompt(Enum):
    CLASSIFICATION = "Are these two artifacts related?"
    CODE_SUMMARY = "Summarize this code '{}'"
    NL_SUMMARY = "Summarize the following '{}'"
    SHALL_REQUIREMENT_SUMMARY = "Remove the terms `The system shall' from the following text and then " \
                                "summarize in 20 words or less '{}'"
    HEADING_SUMMARY = "I am trying to provide a very short and representative summary of the long text to use as a heading " \
                      "in a diagram. Please reduce the following text to less than 8 words '{}'"
    USER_STORY_CREATION = "I want to write user requirements from the perspective of key stakeholders starting with 'As a'. " \
                          "Please write two to three user stories for the following functions '{}'"
    SYSTEM_REQUIREMENT_CREATION = "I am trying to write short requirements specification given a python code file.\n" \
                                  "I would like the requirements to reference physical world entities related to the UAV systems.\n" \
                                  "Write numbered system level requirements for the following code using `shall' format:\n" \
                                  "```python\n{}\n```\n\n" \
                                  "Summarize these requirements in less than 20 words\n"
