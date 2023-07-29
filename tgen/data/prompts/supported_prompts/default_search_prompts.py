DEFAULT_SEARCH_GOAL = "Below is a set of software artifacts of a project. " \
                      "You are the expert on this project." \
                      "You are perform the job of a search bar for a software system. " \
                      "The artifacts are ranked from most to least related to the search query using a heuristic algorithm. " \
                      "Your job is to make some minor modifications to the rankings, " \
                      "so the artifacts are perfectly ranked from most to least related to the search query."
DEFAULT_SEARCH_INSTRUCTIONS = "# Instructions" \
                              "\n1. Summarize the main feature or topic of the search query in 1-2 sentences. " \
                              "Use your knowledge of the system's purpose and capabilities to infer what the " \
                              "query is likely referring to." \
                              "Enclose your answer in <query-summary></query-summary>" \
                              "\n2. For each artifact, assign a score from 1-10 indicating its relevance to the query's main feature. " \
                              "\nFormat: ID | SCORE | EXPLANATION" \
                              "\nExplanation should be a sentence describing" \
                              " how the artifact contributes to delivering the query functionality." \
                              "\n10 = Directly provides functionality\n1 = Unrelated" \
                              "\nMake sure to include every artifact. Work through each artifact in sequential order " \
                              "starting with smallest ID and ending with the largest. " \
                              "Focus more detail on top artifacts. " \
                              "Enclose your answer in <explanation></explanation>."
DEFAULT_SEARCH_QUERY_TAG = "query"
DEFAULT_SEARCH_LINK_TAG = "search-results"
