import { ViewSchema } from "@/types";
import { buildRequest } from "@/api";

/**
 * Creates or updates given view under project specified.
 *
 * @param versionId - The version to mark the view as created.
 * @param view - The view to be created.
 * @return The saved view.
 */
export async function saveView(
  versionId: string,
  view: ViewSchema
): Promise<ViewSchema> {
  return buildRequest<ViewSchema, "versionId", ViewSchema>("viewCollection", {
    versionId,
  }).post(view);
}

/**
 * Returns list of view associated with given project.
 *
 * @param versionId - The project version to get views for.
 * @return The project's views.
 */
export async function getViews(versionId: string): Promise<ViewSchema[]> {
  return buildRequest<ViewSchema[], "versionId">("viewCollection", {
    versionId,
  }).get();
}

/**
 * Deletes the given view from the database.
 * User must have edit permissions on the project.
 *
 * @param viewId - The view to be deleted.
 */
export async function deleteView(viewId: string): Promise<void> {
  await buildRequest<void, "viewId">("view", {
    viewId,
  }).delete();
}

/**
 * Sets the view to be the user's current view.
 * @param viewId - The view to save.
 */
export async function setCurrentView(viewId: string): Promise<void> {
  return buildRequest<void, "viewId">("viewCurrent", {
    viewId,
  }).post();
}

/**
 * Removes the current view affiliated with current user.
 */
export async function clearCurrentView(): Promise<void> {
  return buildRequest("viewCurrentClear").delete();
}
