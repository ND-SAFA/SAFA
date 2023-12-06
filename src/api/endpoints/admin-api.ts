import { buildRequest } from "@/api";

/**
 * Creates a new superuser.
 * @param email - The email of the user to make a superuser.
 */
export async function createSuperuser(email: string): Promise<void> {
  await buildRequest<void, string, { email: string }>("setSuperuser").post({
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
