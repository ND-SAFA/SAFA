import { UserProgressSummarySchema } from "@/types";
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
  return buildRequest<UserProgressSummarySchema>("onboardingStatistics").get();
}
