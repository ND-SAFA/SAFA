/**
 * Defines the schema for the user progress summary.
 */
export interface UserProgressSummarySchema {
  /**
   * Statistics for the accounts created.
   */
  accounts: AccountCreationStatisticsSchema;
  /**
   * Statistics for the github integrations.
   */
  github: GithubIntegrationStatisticsSchema;
  /**
   * Statistics for the project imports.
   */
  imports: ProjectImportStatisticsSchema;
  /**
   * Statistics for the project summarizations.
   */
  summarizations: ProjectSummarizationStatisticsSchema;
  /**
   * Statistics for the project generations.
   */
  generations: GenerationStatisticsSchema;
}

/**
 * Defines the schema for statistics of account creation.
 */
interface AccountCreationStatisticsSchema {
  /**
   * Number of accounts that exist within the app.
   */
  created: number;
  /**
   * Number of accounts that have been verified.
   */
  verified: number;
  /**
   * Number of accounts that have actual progress tracking.
   */
  haveProperProgressTracking: number;
}

/**
 * Defines the schema for statistics of github integrations that have been performed.
 */
interface GithubIntegrationStatisticsSchema {
  /**
   * Statistics for all accounts.
   */
  total: GithubIntegrationStatisticsSingleSchema;
  /**
   * Statistics for all accounts with proper tracking.
   */
  withProperTracking: GithubIntegrationStatisticsSingleSchema;
}

/**
 * Defines the schema for statistics of accounts that have integrated with github.
 */
interface GithubIntegrationStatisticsSingleSchema {
  /**
   * Number of accounts with github integrated.
   */
  accounts: number;
  /**
   * Percentage of created accounts with github integrated.
   */
  percent: number;
  /**
   * Average amount of time in seconds between account creation and github integration.
   */
  averageTime: number;
}

/**
 * Defines the schema for statistics of project imports that have been performed.
 */
interface ProjectImportStatisticsSchema {
  /**
   * Statistics for all accounts.
   */
  total: ImportStatisticsSchema;
  /**
   * Statistics for all accounts with github integration completed.
   */
  fromGithub: ImportStatisticsSchema;
  /**
   * Statistics for all accounts with github integration completed and with proper tracking.
   */
  fromGithubProper: ImportStatisticsSchema;
  /**
   * Total number of imports performed.
   */
  totalPerformed: number;
}

/**
 * Defines the schema for statistics of accounts that have imported projects.
 */
interface ImportStatisticsSchema {
  /**
   * Number of accounts that have performed a project import.
   */
  accounts: number;
  /**
   * Percentage of accounts that have performed a project import.
   */
  percent: number;
  /**
   * Average amount of time between github being connected and an import being performed.
   */
  averageTime: number;
}

/**
 * Defines the schema for statistics of summarizations that have been performed.
 */
interface ProjectSummarizationStatisticsSchema {
  /**
   * Total number of summarizations performed.
   */
  totalPerformed: number;
}

/**
 * Defines the schema for statistics of generations that have been performed.
 */
interface GenerationStatisticsSchema {
  /**
   * Statistics for all accounts.
   */
  total: GenerationStatisticsSingleSchema;
  /**
   * Statistics for all accounts with a project imported.
   */
  fromImport: GenerationStatisticsSingleSchema;
  /**
   * Statistics for all accounts with a project imported and with proper tracking.
   */
  fromImportProper: GenerationStatisticsSingleSchema;
  /**
   * Total number of generations that have been performed.
   */
  totalGenerations: number;
  /**
   * Total number of lines that have been generated on.
   */
  linesGeneratedOn: number;
}

/**
 * Defines the schema for statistics of accounts that have generated.
 */
interface GenerationStatisticsSingleSchema {
  /**
   * Number of accounts that have performed a hierarchy generation.
   */
  accounts: number;
  /**
   * Percentage of accounts that have performed a hierarchy generation.
   */
  percent: number;
  /**
   * Average amount of time between a project being imported and a generation being performed.
   */
  averageTime: number;
}

/**
 * Defines the schema for a single user's progress summary.
 */
export interface SingleUserProgressSummarySchema {
  /**
   * Number of imports performed.
   */
  importsPerformed: number;
  /**
   * Number of summarizations performed.
   */
  summarizationsPerformed: number;
  /**
   * Number of generations performed.
   */
  generationsPerformed: number;
  /**
   * Number of lines generated on.
   */
  linesGeneratedOn: number;
  /**
   * ISO Time the account was created.
   */
  accountCreatedTime: string;
  /**
   * ISO Time the github was linked.
   */
  githubLinkedTime: string;
  /**
   * ISO Time the first project was imported.
   */
  firstProjectImportedTime: string;
  /**
   * ISO Time the first generation was performed.
   */
  firstGenerationPerformedTime: string;
}
