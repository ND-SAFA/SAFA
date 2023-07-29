DEFAULT_SEARCH_GOAL = "Below is a set of software artifacts of a project. " \
                      "You are the expert on this project." \
                      "You are a search bar for a software system. " \
                      "The artifacts are ranked from most to least related to the search query using a heuristic algorithm. " \
                      "Your job is to make some minor modifications to the rankings, " \
                      "so the artifacts are perfectly ranked from most to least related to the search query."
DEFAULT_SEARCH_INSTRUCTIONS = "# Instructions" \
                              "\n1. First, provide a high-level description of the primary feature of the query. " \
                              "Use the context of the system to make assumptions about what this might mean. " \
                              "Enclose your answer in <query-summary></query-summary>" \
                              "\n2. For each artifact provide " \
                              "a score from 1 to 10 representing how much it enabled the query functionality followed " \
                              "by a sentence explaining how the artifact's functionality helps fulfill the query functionality. " \
                              "If the artifact is not related, then use `NA`. " \
                              "Each entry should be on a new line. " \
                              "Remember that the artifacts are already sorted so pay extra attention to the beginning of the list. " \
                              "The format should be ID - SCORE - SENTENCE. " \
                              "Start with the artifact with the smallest ID and work sequentially through all artifacts. " \
                              "Include an entry for each artifact. " \
                              "Enclose your answer in <explanation></explanation>." \
                              "\n3. Then, using your answer to (2) rank all the artifacts from most to least related to the query. " \
                              "Provide a ranking consistent with the scores given in your response to (2). " \
                              "Provide the ranking as comma delimited list of artifact ids where the first element is " \
                              "the most related while the last element is the least. " \
                              "All artifact ids should be included in this list. " \
                              "Enclose the list in <search-results></search-results>."
DEFAULT_SEARCH_QUERY_TAG = "query"
DEFAULT_SEARCH_LINK_TAG = "search-results"
