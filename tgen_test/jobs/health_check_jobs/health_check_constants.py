from tgen.common.objects.artifact import Artifact

ARTIFACT_CONTENT = ["All dogs are really cute.", "Cars make vroom vroom sound.", "Fire trucks are loud.", "Dogs pee on fire hydrants.",
                    "Cats are better than Dogs"]
ARTIFACT_IDS = [f"a_{i}" for i in range(len(ARTIFACT_CONTENT))]
QUERY = Artifact(id="query1", content="What pet should I get?", layer_id="queries")
EXPECTED_CONTEXT_IDS = [ARTIFACT_IDS[0], ARTIFACT_IDS[-1]]
EXPECTED_CONFLICTING_IDS = [ARTIFACT_IDS[0]]
EXPECTED_CONTRADICTION_EXPLANATION = "this is an explanation"
EXISTING_CONCEPTS = ["dog", "cat", "fire truck", "car", "vroom"]
CONCEPT_LAYER_ID = "concept"
UNDEFINED_CONCEPT = "undefined_concept"
QUERY_CONCEPTS = ["pug", "dog", UNDEFINED_CONCEPT]
QUERY_CONTENT = "Pugs aren't cute dogs."
QUERY_ID = "target"
EXPECTED_RELATED_ARTIFACTS = EXPECTED_CONTEXT_IDS + EXISTING_CONCEPTS[:2]
