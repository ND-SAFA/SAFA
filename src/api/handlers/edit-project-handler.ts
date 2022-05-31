import {
  IOHandlerCallback,
  Project,
  ProjectEntities,
  ProjectIdentifier,
} from "@/types";
import { logModule, projectModule } from "@/store";
import {
  deleteProject,
  deleteProjectVersion,
  handleClearProject,
  saveProject,
} from "@/api";

/**
 * Saves a project, updates app state, and logs the status.
 *
 * @param project - The project to delete.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export function handleSaveProject(
  project: Pick<ProjectIdentifier, "projectId" | "name" | "description">,
  { onSuccess, onError }: IOHandlerCallback<Project>
): void {
  saveProject(project)
    .then((project: Project) => {
      logModule.onSuccess(`Project has been saved: ${project.name}`);
      onSuccess?.(project);
    })
    .catch((e) => {
      logModule.onSuccess(`Unable to save project ${project.name}.`);
      logModule.onDevError(e.message);
      onError?.(e);
    });
}

/**
 * Deletes a project, updates app state, and logs the status.
 *
 * @param project - The project to delete.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export function handleDeleteProject(
  project: ProjectIdentifier,
  { onSuccess, onError }: IOHandlerCallback<ProjectIdentifier>
): void {
  deleteProject(project.projectId)
    .then(async () => {
      logModule.onSuccess(`Project has been deleted: ${project.name}`);
      onSuccess?.(project);

      if (project.name !== projectModule.getProject.name) return;

      // Clear the current project if it has been deleted.
      await handleClearProject();
    })
    .catch((e) => {
      logModule.onSuccess(`Unable to delete project: ${project.name}.`);
      logModule.onDevError(e.message);
      onError?.(e);
    });
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
      logModule.onSuccess(`Version has successfully been deleted.`);
      onSuccess?.();
    })
    .catch((e) => {
      logModule.onSuccess(`Unable to delete version.`);
      logModule.onDevError(e.message);
      onError?.(e);
    });
}
