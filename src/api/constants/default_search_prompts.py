DEFAULT_SEARCH_GOAL = "You are a search bar for a software system. " \
                      "Below is a search query followed by the software artifacts in the system. " \
                      "Rank artifacts from most to least related to the search query."
DEFAULT_SEARCH_INSTRUCTIONS = "# Instructions" \
                              "\n1. First, output your interpretation of the query. " \
                              "Use the context of the system to make assumptions about what this might mean. " \
                              "Enclose your answer in <query-summary></query-summary>" \
                              "2. Then, rank the software artifacts from most to least related to query. " \
                              "Provide the ranking as comma delimited list of artifact ids where the first element is " \
                              "the most related while the last element is the least. " \
                              "Enclose the list in <search-results></search-results>."
DEFAULT_SEARCH_QUERY_TAG = "query"
DEFAULT_SEARCH_LINK_TAG = "search-results"
