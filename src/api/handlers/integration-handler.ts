import { IOHandlerCallback } from "@/types";
import { getJiraRefreshToken, getJiraToken } from "@/api";

/**
 * Handles Jira authentication when the app loads.
 *
 * @param accessCode -The Jira access code, if noe exists.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export function handleAuthorizeJira(
  accessCode: string | (string | null)[] | undefined,
  { onSuccess, onError }: IOHandlerCallback<string>
): void {
  if (accessCode) {
    getJiraToken(String(accessCode))
      .then((token) => onSuccess?.(token))
      .catch((e) => onError?.(e));
  } else {
    getJiraRefreshToken()
      .then((token) => onSuccess?.(token))
      .catch((e) => onError?.(e));
  }
}
