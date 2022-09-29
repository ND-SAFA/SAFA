import { IOHandlerCallback, ProjectModel, IdentifierModel } from "@/types";
import { logStore, projectStore } from "@/hooks";
import {
  deleteProject,
  deleteProjectVersion,
  handleClearProject,
  saveProject,
} from "@/api";

/**
 * Saves a project, updates app state, and logs the status.
 *
 * @param project - The project to save.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 * @param onComplete - Called after the action.
 */
export function handleSaveProject(
  project: Pick<IdentifierModel, "projectId" | "name" | "description">,
  { onSuccess, onError, onComplete }: IOHandlerCallback<ProjectModel>
): void {
  saveProject(project)
    .then((project) => {
      projectStore.allProjects = [
        project,
        ...projectStore.allProjects.filter(
          ({ projectId }) => projectId !== project.projectId
        ),
      ];

      logStore.onSuccess(`Project has been saved: ${project.name}`);
      onSuccess?.(project);
    })
    .catch((e) => {
      logStore.onError(`Unable to save project: ${project.name}`);
      logStore.onDevError(e.message);
      onError?.(e);
    })
    .finally(onComplete);
}

/**
 * Deletes a project, updates app state, and logs the status.
 *
 * @param project - The project to delete.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 * @param onComplete - Called after the action.
 */
export function handleDeleteProject(
  project: IdentifierModel,
  { onSuccess, onError, onComplete }: IOHandlerCallback<IdentifierModel>
): void {
  deleteProject(project.projectId)
    .then(async () => {
      projectStore.allProjects = projectStore.allProjects.filter(
        ({ projectId }) => projectId !== project.projectId
      );

      logStore.onSuccess(`Project has been deleted: ${project.name}`);
      onSuccess?.(project);

      if (project.name !== projectStore.project.name) return;

      // Clear the current project if it has been deleted.
      await handleClearProject();
    })
    .catch((e) => {
      logStore.onError(`Unable to delete project: ${project.name}.`);
      logStore.onDevError(e.message);
      onError?.(e);
    })
    .finally(onComplete);
}

/**
 * Deletes a version, updates app state, and logs the status.
 *
 * @param versionId - The version to delete.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export function handleDeleteVersion(
  versionId: string,
  { onSuccess, onError }: IOHandlerCallback
): void {
  deleteProjectVersion(versionId)
    .then(async () => {
      logStore.onSuccess(`Version has successfully been deleted.`);
      onSuccess?.();
    })
    .catch((e) => {
      logStore.onError(`Unable to delete version.`);
      logStore.onDevError(e.message);
      onError?.(e);
    });
}
