import { TrainingStepSchema } from "@/types";

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
 * A mapping of whether certain test features are enabled.
 */
export const ENABLED_FEATURES = {
  EXAMPLE_TRAINING_STEPS: false,
};
