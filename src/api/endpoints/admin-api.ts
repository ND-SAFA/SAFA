import {
  SingleUserProgressSummarySchema,
  UserProgressSummarySchema,
  UserSchema,
} from "@/types";
import { buildRequest } from "@/api";

/**
 * Creates a new superuser.
 * @param email - The email of the user to make a superuser.
 */
export async function createSuperuser(email: string): Promise<void> {
  await buildRequest<void, string, { email: string }>("superuser").put({
    email,
  });
}

/**
 * If the current user is a superuser, enables their superuser powers.
 */
export async function activateSuperuser(): Promise<void> {
  await buildRequest<void>("superuserActivate").put();
}

/**
 * If the current user is a superuser, disables their superuser powers.
 */
export async function deactivateSuperuser(): Promise<void> {
  await buildRequest<void>("superuserDeactivate").put();
}

/**
 * Retrieves all users in the system.
 */
export async function getUsers(): Promise<UserSchema[]> {
  return buildRequest<UserSchema[]>("accountCollection").get();
}

/**
 * Retrieves the statistics for the user progress in the app.
 * @returns The user progress statistics.
 */
export async function getOnboardingStatistics(): Promise<UserProgressSummarySchema> {
  return buildRequest<UserProgressSummarySchema>("statisticsOnboarding").get();
}

/**
 * Retrieves the statistics for the user progress in the app.
 * @param userId - The id of the user to retrieve statistics for.
 * @returns The user progress statistics.
 */
export async function getUserStatistics(
  userId: string
): Promise<SingleUserProgressSummarySchema> {
  return {
    importsPerformed: 0,
    summarizationsPerformed: 0,
    generationsPerformed: 0,
    linesGeneratedOn: 0,
    accountCreatedTime: new Date().toISOString(),
    githubLinkedTime: new Date().toISOString(),
    firstProjectImportedTime: new Date().toISOString(),
    firstGenerationPerformedTime: new Date().toISOString(),
  };
  return buildRequest<SingleUserProgressSummarySchema, "userId">(
    "statisticsUser",
    { userId }
  ).get();
}
