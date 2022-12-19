import {
  IOHandlerCallback,
  ProjectSchema,
  IdentifierSchema,
  VersionSchema,
} from "@/types";
import { versionToString } from "@/util";
import { identifierSaveStore, logStore, projectStore } from "@/hooks";
import {
  deleteProject,
  deleteProjectVersion,
  handleClearProject,
  saveProject,
} from "@/api";

/**
 * Saves a project, updates app state, and logs the status.
 *
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 * @param onComplete - Called after the action.
 */
export function handleSaveProject({
  onSuccess,
  onError,
  onComplete,
}: IOHandlerCallback<ProjectSchema>): void {
  const identifier = identifierSaveStore.editedIdentifier;

  saveProject(identifier)
    .then((project) => {
      projectStore.addProject(project);
      logStore.onSuccess(`Project has been saved: ${project.name}`);
      onSuccess?.(project);
    })
    .catch((e) => {
      logStore.onError(`Unable to save project: ${identifier.name}`);
      logStore.onDevError(e.message);
      onError?.(e);
    })
    .finally(onComplete);
}

/**
 * Deletes a project, updates app state, and logs the status.
 *
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 * @param onComplete - Called after the action.
 */
export function handleDeleteProject({
  onSuccess,
  onError,
  onComplete,
}: IOHandlerCallback<IdentifierSchema>): void {
  const project = identifierSaveStore.baseIdentifier;

  if (!project) return;

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
 * @param version - The version to delete.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export function handleDeleteVersion(
  version: VersionSchema,
  { onSuccess, onError }: IOHandlerCallback
): void {
  const name = versionToString(version);

  logStore.confirm(
    `Delete Version`,
    `Are you sure you would like to delete "${name}"?`,
    async (isConfirmed: boolean) => {
      if (!isConfirmed) return;

      deleteProjectVersion(version.versionId)
        .then(async () => {
          logStore.onSuccess(`Successfully deleted version: ${name}`);
          onSuccess?.();
        })
        .catch((e) => {
          logStore.onError(`Unable to delete version: ${name}`);
          logStore.onDevError(e.message);
          onError?.(e);
        });
    }
  );
}
