import { UserApiKeysSchema } from "@/types";
import { buildRequest } from "@/api";

/**
 * Gets the user's API keys (masked).
 *
 * @return The user's API keys with values masked.
 * @throws If the request fails.
 */
export async function getUserApiKeys(): Promise<UserApiKeysSchema> {
  return buildRequest<UserApiKeysSchema>("accountApiKeys").get();
}

/**
 * Saves or updates the user's API keys.
 *
 * @param apiKeys - The API keys to save.
 * @throws If the request fails.
 */
export async function saveUserApiKeys(
  apiKeys: UserApiKeysSchema
): Promise<void> {
  await buildRequest<void, string, UserApiKeysSchema>("accountApiKeys").post(
    apiKeys
  );
}

/**
 * Deletes the user's API keys.
 *
 * @throws If the request fails.
 */
export async function deleteUserApiKeys(): Promise<void> {
  await buildRequest<void>("accountApiKeys").delete();
}
