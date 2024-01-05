/**
 * All types of artifacts that can be generated.
 */
export const ARTIFACT_GENERATION_TYPES = {
  USER_STORY: "User Story",
  FUNCTIONAL_REQ: "Functional Requirement",
  FEATURE: "Feature",
  EPIC: "Epic",
  SUB_SYSTEM: "Sub-System",
  GRAPH_QL: "GraphQL API Documentation",
  BUS_LOGIC: "Business Logic",
};

/**
 * The types of artifacts allowed to be generated.
 */
export const ARTIFACT_GENERATION_OPTIONS =
  process.env.NODE_ENV === "production"
    ? [
        ARTIFACT_GENERATION_TYPES.USER_STORY,
        ARTIFACT_GENERATION_TYPES.FUNCTIONAL_REQ,
        ARTIFACT_GENERATION_TYPES.FEATURE,
        ARTIFACT_GENERATION_TYPES.EPIC,
        ARTIFACT_GENERATION_TYPES.SUB_SYSTEM,
      ]
    : [
        ARTIFACT_GENERATION_TYPES.USER_STORY,
        ARTIFACT_GENERATION_TYPES.FUNCTIONAL_REQ,
        ARTIFACT_GENERATION_TYPES.FEATURE,
        ARTIFACT_GENERATION_TYPES.EPIC,
        ARTIFACT_GENERATION_TYPES.SUB_SYSTEM,
        ARTIFACT_GENERATION_TYPES.GRAPH_QL,
        ARTIFACT_GENERATION_TYPES.BUS_LOGIC,
      ];

/**
 * The maximum number of artifacts that can be generated on.
 */
export const MAX_GENERATED_BASE_ARTIFACTS = 1000;
