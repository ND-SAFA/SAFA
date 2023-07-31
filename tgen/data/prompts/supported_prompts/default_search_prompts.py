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
                              "\n\n2. Provide the following information for each artifact as formatted below:" \
                              "\n    Format: ID | SUMMARY | EXPLANATION | SCORE" \
                              "\n    - For `ID` provide the ID of artifact currently being processed." \
                              "\n    - For `SUMMARY` summarize the relevant parts of the artifact's functionality in the context of your response to (1)." \
                              "\n    - For `EXPLANATION` detail what part of the artifact's functionality contributes to the " \
                              "fulfillment of the query's functionality and what how it does it." \
                              "\n    - For `SCORE` provide a number from 1-10 representing how relevant the artifact functionality's " \
                              "is to the functionality described in your response to (1). " \
                              "Specifically, the score should be a number from 1-10. " \
                              "Use the following guidelines to extrapolate the correct score:" \
                              "\n        * 10 = Artifact performs the query's core functionality" \
                              "\n        * 8 = Artifact performs an essential function to the query's functionality" \
                              "\n        * 4 = Artifact performs functionality indirectly related to query's functionality" \
                              "\n        * 1 = Related to distant or unrelated functionality of search query." \
                              "\n    Base your score on how directly each artifact contributes to or enables the functionality " \
                              "described in your answer to (1)." \
                              "\nIMPORTANT: For question (2), work through each artifact sequentially starting with ID 0. " \
                              "Include an entry for each artifact. " \
                              "Provide each artifact's entry on a single line in the format specified. " \
                              "Enclose your answer in <explanation></explanation>."
DEFAULT_SEARCH_QUERY_TAG = "query"
DEFAULT_SEARCH_LINK_TAG = "search-results"
