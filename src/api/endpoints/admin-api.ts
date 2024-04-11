import { UserProgressSummarySchema } from "@/types";
import { ENABLED_FEATURES } from "@/util";
import { buildRequest } from "@/api";

/**
 * Creates a new superuser.
 * @param email - The email of the user to make a superuser.
 */
export async function createSuperuser(email: string): Promise<void> {
  await buildRequest<void, string, { email: string }>("setSuperuser").put({
    email,
  });
}

/**
 * If the current user is a superuser, enables their superuser powers.
 */
export async function activateSuperuser(): Promise<void> {
  await buildRequest<void>("activateSuperuser").put();
}

/**
 * If the current user is a superuser, disables their superuser powers.
 */
export async function deactivateSuperuser(): Promise<void> {
  await buildRequest<void>("deactivateSuperuser").put();
}

/**
 * Retrieves the statistics for the user progress in the app.
 */
export async function getOnboardingStatistics(): Promise<UserProgressSummarySchema> {
  if (ENABLED_FEATURES.ONBOARDING_STATS_TEST) {
    return {
      accounts: {
        created: 0,
        verified: 0,
        haveProperProgressTracking: 0,
      },
      github: {
        total: {
          accounts: 0,
          percent: 0,
          averageTime: 0,
        },
        withProperTracking: {
          accounts: 0,
          percent: 0,
          averageTime: 0,
        },
      },
      imports: {
        total: {
          accounts: 0,
          percent: 0,
          averageTime: 0,
        },
        fromGithub: {
          accounts: 0,
          percent: 0,
          averageTime: 0,
        },
        fromGithubProper: {
          accounts: 0,
          percent: 0,
          averageTime: 0,
        },
        totalPerformed: 0,
      },
      summarizations: {
        totalPerformed: 0,
      },
      generations: {
        total: {
          accounts: 0,
          percent: 0,
          averageTime: 0,
        },
        fromImport: {
          accounts: 0,
          percent: 0,
          averageTime: 0,
        },
        fromImportProper: {
          accounts: 0,
          percent: 0,
          averageTime: 0,
        },
        totalGenerations: 0,
        linesGeneratedOn: 0,
      },
    };
  }

  return buildRequest<UserProgressSummarySchema>("onboardingStatistics").get();
}
