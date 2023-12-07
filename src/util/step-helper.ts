/**
 * The steps involved in the initial onboarding process.
 */
export const ONBOARDING_STEPS = {
  // Connect to GitHub
  connect: {
    title: "Connect GitHub",
    caption: "Connect your GitHub account to get started.",
    index: 0,
    number: 1,
  },
  // Select GitHUb org, repo, branch, file path.
  code: {
    title: "Select Repository",
    caption: "Select code to import from GitHub.",
    index: 1,
    number: 2,
  },
  // Import, await job, show summary to the right when complete.
  summarize: {
    title: "Import & Summarize",
    caption: "Generate system and code level summaries while importing.",
    index: 2,
    number: 3,
  },
  // Generate, await job, show buttons for export and view when complete.
  generate: {
    title: "Generate Documentation",
    caption: "Generate documentation on the functionality of your system.",
    index: 3,
    number: 4,
  },
};
