import { ENABLED_FEATURES } from "@/util/enabled-features";

/**
 * The steps involved in the initial onboarding process.
 */
export const ONBOARDING_STEPS = {
  connect: {
    title: "Connect GitHub",
    caption: "Connect your GitHub account to get started.",
    index: 0,
    number: 1,
  },
  code: {
    title: "Select Repository",
    caption: "Select code from GitHub to import.",
    index: 1,
    number: 2,
  },
  generate: {
    title: "Generate Documentation",
    caption: ENABLED_FEATURES.BILLING_ONBOARDING
      ? "Review costs and generate documentation for your code."
      : "Generate documentation for your code.",
    index: 2,
    number: 3,
  },
  job: {
    title: "Await Generation",
    caption: "Wait for data generation to complete.",
    index: 3,
    number: 4,
  },
  view: {
    title: "View Documentation",
    caption: "Export generated data, or view the data within SAFA.",
    index: 4,
    number: 5,
  },
};
