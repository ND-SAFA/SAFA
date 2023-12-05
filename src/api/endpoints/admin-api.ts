import { buildRequest } from "@/api";

/**
 * Creates a new superuser.
 * @param userId - The user id of the user to make a superuser.
 */
export async function createSuperuser(userId: string): Promise<void> {
  await buildRequest<void, "userId">("setSuperuser", { userId }).put();
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
