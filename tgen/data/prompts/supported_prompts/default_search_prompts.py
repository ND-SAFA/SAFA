DEFAULT_SEARCH_GOAL = "# Goal\n---\n" \
                      "You are the expert on this project. " \
                      "You are perform the job of a search bar for a software system. " \
                      "Under the section `Software Specification` is a description of the software project. " \
                      "Under the section `Software Artifacts` is the list of potential software artifacts matching the search query. " \
                      "The artifacts are ranked from most to least related to the search query using a word matching algorithm. " \
                      "Your job is to improve this ranking, so that the artifacts ranked from most to least related to the functionality " \
                      "of the search query."
DEFAULT_SEARCH_INSTRUCTIONS = "# Instructions\n---\n" \
                              "*Answer the questions below as a system expert. " \
                              "Each questions has multiple parts, please read the instructions carefully.*" \
                              "\n\n1. Write a paragraph about the search query describing:" \
                              "\n- High-level summary of search query functionality" \
                              "\n- Acceptance criteria for fulfillment of the search query functionality" \
                              "\n- Description of existing system functionality relevant to the search query functionality. " \
                              "\nUse your knowledge of the system's capabilities to infer what the search query is likely referring to. " \
                              "Enclose your answer in <query-summary></query-summary>" \
                              "\n\n2. Starting with the artifact with ID 0, " \
                              "sequentially analyze each artifact and provide the following information as formatted below:" \
                              "\nFormat: ID | SUMMARY | EXPLANATION | SCORE" \
                              "\n- For `ID` provide the ID of artifact currently being processed." \
                              "\n- For `SUMMARY` extract the parts of the artifact's functionality relevant to your response to (1)." \
                              "\n- For `EXPLANATION` describe how the artifact's functionality contributes to the fulfillment of the search query" \
                              " as described in your response to (1)." \
                              "\n- For `SCORE` provide a number from 1-10 representing how relevant the artifact functionality's " \
                              "is to the functionality described in your response to (1). " \
                              "Specifically, the score should be a number from 1-10. " \
                              "Use the following guidelines to extrapolate the correct score:" \
                              "\n    * 10 = Artifact performs core search query functionality" \
                              "\n    * 8 = Artifact performs an essential function to the search query functionality" \
                              "\n    * 4 = Related to supporting (auxiliary) functionality of search query." \
                              "\n    * 1 = Related to distant or unrelated functionality of search query." \
                              "\n    Base your score on how directly each artifact contributes to or enables the functionality " \
                              "described in your answer to (1)." \
                              "\nWork through each artifact in sequential order and make sure to include every artifact." \
                              "Provide each artifact's entry on a single line in the format specified." \
                              "Enclose your answer in <explanation></explanation>."
DEFAULT_SEARCH_QUERY_TAG = "query"
DEFAULT_SEARCH_LINK_TAG = "search-results"
