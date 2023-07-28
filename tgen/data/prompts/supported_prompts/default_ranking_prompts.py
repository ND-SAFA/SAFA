DEFAULT_RANKING_EXPLANATION_TAG = "explanation"
DEFAULT_RANKING_GOAL = "# Task\n\n" \
                       "Below is a set of software artifacts of a project. You are the expert on this project. " \
                       "You are performing traceability by finding the children associated with a given parent artifact. " \
                       "You are focusing on a single parent artifact. " \
                       "Enclosed in <parent-artifact><parent-artifact> the parent artifact followed by " \
                       "description of the project and then by the list of potential children (formatted in XML)." \
                       "\n\n"
DEFAULT_RANKING_INSTRUCTIONS = "# Instructions\n" \
                               "1. Provide 2-3 sentences describing the job of the parent artifact. " \
                               "Include its responsibilities, its dependencies, and its purpose in the system. " \
                               "Enclose your answer in <function></function>" \
                               "\n2. Read each potential child artifact in order. " \
                               "Decide whether the artifact impacts, implements, or refines the parent artifact functionality. " \
                               "Format your answer as: ID - Yes/No. Enclose your answer in <classification></classification>." \
                               "\n3. For each selected artifact, " \
                               "provide a sentence describing how its role in the system helps the parent artifact achieve its job. " \
                               "Put each entry on different lines and follow the format: ID - DESCRIPTION. " \
                               "Work through one artifact at a time so that the IDs are in ascending order. " \
                               f"Enclose your answer in <{DEFAULT_RANKING_EXPLANATION_TAG}></{DEFAULT_RANKING_EXPLANATION_TAG}>." \
                               "\n3. Rank the children by proximity to the parent artifact functionality." \
                               "Provide a comma delimited list of artifact ids where the " \
                               "first element is the most similar to the parent artifact while the last element is the least. " \
                               "Enclose the list in <links></links>."
