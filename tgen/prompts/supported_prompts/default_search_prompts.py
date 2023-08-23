DEFAULT_SEARCH_GOAL = (
    "You are a search bar for a software system. "
    "Below is a search query followed by the software artifacts in the system. "
    "Rank artifacts from most to least related to the search query."
)
QUESTION1 = ("Provide your interpretation of the query. "
             "Use the context of the system to make assumptions about what this might mean. ",
             "query-summary")
QUESTION2 = ("Rank the software artifacts from most to least related to query. "
             "Provide the ranking as comma delimited list of artifact ids where the first element is "
             "the most related while the last element is the least. ",
             "search-results")

DEFAULT_SEARCH_QUESTIONS = [QUESTION1, QUESTION2]
DEFAULT_SEARCH_QUERY_TAG = "query"
DEFAULT_SEARCH_LINK_TAG = "search-results"
