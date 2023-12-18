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
    title: ENABLED_FEATURES.GENERATE_ONBOARDING
      ? "Generate Documentation"
      : "Import Code",
    caption: ENABLED_FEATURES.BILLING_ONBOARDING
      ? "Review costs and generate documentation for your code."
      : ENABLED_FEATURES.GENERATE_ONBOARDING
        ? "Generate documentation for your code."
        : "Import your code from GitHub.",
    index: 2,
    number: 3,
  },
  job: {
    title: ENABLED_FEATURES.GENERATE_ONBOARDING
      ? "Await Generation"
      : "Await Upload",
    caption: ENABLED_FEATURES.GENERATE_ONBOARDING
      ? "Wait for data generation to complete."
      : "Wait for your upload to complete.",
    index: 3,
    number: 4,
  },
  view: {
    title: ENABLED_FEATURES.GENERATE_ONBOARDING
      ? "View Documentation"
      : "Generate Documentation",
    caption: ENABLED_FEATURES.GENERATE_ONBOARDING
      ? "Export generated data or view within SAFA."
      : "Generate documentation for your code.",
    index: 4,
    number: 5,
  },
};
