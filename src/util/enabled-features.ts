import {
  AttributeLayoutSchema,
  AttributeSchema,
  TrainingStepSchema,
} from "@/types";

/**
 * Example steps for model training.
 */
export const EXAMPLE_TRAINING_STEPS = [
  {
    type: "document",
    updatedAt: new Date(Date.now()).toISOString(),
    status: "Completed",
    keywords: [],
    documents: [
      {
        name: "BOSCH Automotive Handbook.pdf",
        url: "https://path-to-gcp-bucket-file",
      },
    ],
    repositories: [],
    projects: [],
  },
  {
    type: "repository",
    updatedAt: new Date(Date.now()).toISOString(),
    status: "Completed",
    keywords: [],
    documents: [],
    repositories: [
      {
        name: "organization/my-project",
        url: "https://path-to-git-hub-repo",
      },
    ],
    projects: [],
  },
  {
    type: "project",
    updatedAt: new Date(Date.now()).toISOString(),
    status: "In Progress",
    keywords: [],
    documents: [],
    repositories: [],
    projects: [
      {
        id: "123",
        name: "My Project",
        levels: [
          {
            source: "Designs",
            target: "Designs",
          },
          {
            source: "Designs",
            target: "Requirements",
          },
        ],
      },
    ],
  },
] as TrainingStepSchema[];

/**
 * Example attributes for artifacts.
 */
export const EXAMPLE_ATTRIBUTES = [
  {
    key: "str",
    label: "Custom String",
    type: "text",
    min: 4,
    max: 4,
  },
  {
    key: "int",
    label: "Custom Int",
    type: "int",
    min: 0,
    max: 5,
  },
  {
    key: "sel",
    label: "Custom Select",
    type: "select",
    options: ["A", "B", "C"],
  },
  {
    key: "multi",
    label: "Custom Multiselect",
    type: "multiselect",
    options: ["A", "B", "C"],
    min: 1,
    max: 2,
  },
  {
    key: "date",
    label: "Custom Date",
    type: "date",
  },
  {
    key: "float",
    label: "Custom Float",
    type: "float",
  },
  {
    key: "bool",
    label: "Custom Boolean",
    type: "boolean",
  },
  {
    key: "rel",
    label: "Custom Relation",
    type: "relation",
  },
  {
    key: "par",
    label: "Custom Paragraph",
    type: "paragraph",
  },
] as AttributeSchema[];

/**
 * Example attribute layouts for artifacts.
 */
export const EXAMPLE_ATTRIBUTE_LAYOUTS = [
  {
    id: "default",
    artifactTypes: [],
    positions: [
      { x: 0, y: 0, width: 1, height: 1, key: "str" },
      { x: 1, y: 0, width: 1, height: 1, key: "bool" },

      { x: 0, y: 1, width: 1, height: 1, key: "date" },

      { x: 0, y: 2, width: 1, height: 1, key: "int" },
      { x: 1, y: 2, width: 1, height: 1, key: "float" },

      { x: 0, y: 3, width: 1, height: 1, key: "sel" },
      { x: 1, y: 3, width: 1, height: 1, key: "rel" },

      { x: 0, y: 4, width: 2, height: 1, key: "multi" },

      { x: 0, y: 5, width: 2, height: 1, key: "par" },
    ],
  },
] as AttributeLayoutSchema[];

/**
 * A mapping of whether certain test features are enabled.
 */
export const ENABLED_FEATURES = {
  EXAMPLE_TRAINING_STEPS: false,
  EXAMPLE_ATTRIBUTES: false,
};
