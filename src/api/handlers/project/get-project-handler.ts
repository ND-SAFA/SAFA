import { IOHandlerCallback } from "@/types";
import { logStore, projectStore, sessionStore } from "@/hooks";
import { getProjects } from "@/api";

/**
 * Stores all projects for the current user.
 *
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 * @param onComplete - Called after the action.
 */
export async function handleGetProjects({
  onSuccess,
  onError,
  onComplete,
}: IOHandlerCallback): Promise<void> {
  if (!sessionStore.doesSessionExist) {
    onSuccess?.();
    return;
  }

  try {
    projectStore.allProjects = await getProjects();

    onSuccess?.();
  } catch (e) {
    logStore.onError("Unable to load your projects.");
    logStore.onDevError(String(e));
    onError?.(e as Error);
  } finally {
    onComplete?.();
  }
}
