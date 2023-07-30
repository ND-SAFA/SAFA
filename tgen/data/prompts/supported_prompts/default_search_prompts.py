DEFAULT_SEARCH_GOAL = "# Goal\n---\n" \
                      "You are the expert on this project. " \
                      "You are perform the job of a search bar for a software system. " \
                      "Under the section `Software Specification` is a description of the software project. " \
                      "Under the section `Software Artifacts` is the list of potential software artifacts matching the search query. " \
                      "The artifacts are ranked from most to least related to the search query using a word matching algorithm. " \
                      "Your job is to improve this ranking, so that the artifacts ranked from most to least related to the functionality " \
                      "of the search query."
DEFAULT_SEARCH_INSTRUCTIONS = "# Instructions\n---\n" \
                              "1. Summarize the main feature or topic of the search query in 1-2 sentences. " \
                              "Use your knowledge of the system's capabilities to infer what the query is likely referring to. " \
                              "Enclose your answer in <query-summary></query-summary>" \
                              "\n\n2. Starting with the artifact with ID 0 and moving sequentially, " \
                              "provide the following information for each artifact:" \
                              "\nID | SUMMARY | EXPLANATION | SCORE" \
                              "\nFill `ID` with the ID of artifact being processed." \
                              "\nFill `SUMMARY` with a description of any parts of the artifacts related to the functionality of the search query." \
                              "\nFill `EXPLANATION` with a sentence describing how the artifact's functionality relates to " \
                              "the search query's functionality based on your summary." \
                              "\nFill `SCORE` with a number from 1-5 representing how directly the artifact contributes " \
                              "to the specific functionality described in your explanation for the artifact." \
                              "Specifically, it should be a number from 1-5 such that:" \
                              "\n- 5 = Related to core functionality of search query" \
                              "\n- 3 = Related to supporting functionality of search query." \
                              "\n- 1 = Related to distant or unrelated functionality of search query." \
                              "Focus your score on how directly each artifact contributes to or enables the functionality " \
                              "described in your answer to (1)." \
                              "\nWork through each artifact in sequential order and make sure to include every artifact." \
                              "Provide each artifact's entry on a single line in the format specified." \
                              "Enclose your answer in <explanation></explanation>."
DEFAULT_SEARCH_QUERY_TAG = "query"
DEFAULT_SEARCH_LINK_TAG = "search-results"
