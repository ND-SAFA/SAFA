export const ONBOARDING_SUPPORT_LINK =
  "https://calendly.com/agulaya/safa-support-call";

export const ONBOARDING_MEET_LINK = "https://www.safa.ai/contactus";

export const ONBOARDING_GITHUB_IMPORT = `
  To import code, you will need to connect to our GitHub integration,
  and be a contributor on the repository.
  Your organization will also need to approve our integration.
`;

export const ONBOARDING_GITHUB_SECURITY = `
  Our integration will only use read access from the repository you select,
  and does not train on any data you import.
  As we work toward SOC II compliance, you can track our current security practices below.    
`;

export const ONBOARDING_REPO_SELECT = `
  Select which repository you want to import below.
  After selecting, include the main branch and file path to your code
  to ensure that SAFA is applied to the correct data.
`;

export const ONBOARDING_REPO_FREE = `
  Do you work on an open source project? 
  We are offering free generation on projects that will benefit the open source community.
  Please reach out below to learn more.
`;

export const ONBOARDING_SUMMARIZE_MESSAGE = `
  During the import process,
  a summary of each individual code file will be generated
  along with an overall summary of the project.
  You will receive an email when the import completes.
`;

export const ONBOARDING_SUMMARIZE_ERROR = `
  Oh no! It looks like there was an issue with importing from GitHub.
  You can schedule a call with us below to ensure your data gets uploaded properly.
`;

export const ONBOARDING_SUMMARIZE_DURATION = `
  This process may take up to 30 minutes depending on the size of your project.
  Your generation may be put in a queue if there are many imports ahead of you.
`;

export const ONBOARDING_GENERATE_MESSAGE = `
  Now that your code has been imported and summarized,
  we can generate additional documentation to group related functionality.
  You will receive an email when the import completes.
`;

export const ONBOARDING_GENERATE_DURATION = `
  This process may take an additional 30 minutes depending on the size of your project.
  Your generation may be put in a queue if there are many imports ahead of you.
`;

export const ONBOARDING_GENERATE_SUCCESS = `
  Your documentation is ready!
  Below you can either export the documentation, or view the data in SAFA.
  If you are unhappy with the results, 
  please reach out and we can regenerate the data for you.
`;

export const ONBOARDING_GENERATE_LARGE = `
  SAFA is currently in early release.
  if you would like to generate documentation on a larger code base,
  please reach out to us!
  You can also add additional filters to the
  'Select Repository' step to reduce the size of your project.
`;

export const ONBOARDING_GENERATE_ERROR = `
  Oh no! It looks like there was an issue with generating documentation.
  Your invoice will not be finalized until the generation completes successfully.
  You can schedule a call with us below to ensure your data gets generated properly.
`;
