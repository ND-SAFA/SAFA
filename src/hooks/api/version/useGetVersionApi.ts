import { defineStore } from "pinia";

import { computed, onMounted, ref, watch } from "vue";
import { DocumentSchema, IdentifierSchema, VersionSchema } from "@/types";
import {
  documentStore,
  projectStore,
  sessionStore,
  setProjectApiStore,
} from "@/hooks";
import { navigateTo, QueryParams, Routes, router } from "@/router";
import { getProjectVersion, getProjectVersions } from "@/api";
import { useApi } from "@/hooks/api/useApi";
import { pinia } from "@/plugins";

export const useGetVersionApi = defineStore("getVersionApi", () => {
  const allVersions = ref<VersionSchema[]>([]);

  const getVersionApi = useApi("getVersionApi")();

  const currentProject = computed(() => projectStore.project);
  const currentVersion = computed({
    get: () => projectStore.version,
    set(version: VersionSchema | undefined) {
      if (!version) return;

      handleLoadVersion(version.versionId);
    },
  });

  /**
   * Loads the versions of the current project.
   */
  async function handleLoadCurrentProjectVersions(): Promise<void> {
    const { projectId } = currentProject.value;

    allVersions.value = projectId ? await getProjectVersions(projectId) : [];
  }

  /**
   * Load the given project version.
   * Navigates to the artifact view page to show the loaded project.
   *
   * @param versionId - The id of the version to retrieve and load.
   * @param document - The document to start with viewing.
   * @param doNavigate - Whether to navigate to the artifact tree if not already on an artifact page.
   */
  async function handleLoadVersion(
    versionId: string,
    document?: DocumentSchema,
    doNavigate = true
  ): Promise<void> {
    const routeRequiresProject = router.currentRoute.value.matched.some(
      ({ meta }) => meta.requiresProject
    );

    await getVersionApi.handleRequest(
      async () => {
        sessionStore.updateSession({ versionId });

        const project = await getProjectVersion(versionId);

        if (
          project.projectVersion &&
          !allVersions.value.find(
            ({ versionId }) => versionId === project.projectVersion?.versionId
          )
        ) {
          // Add the current version to the list of versions if it is not already there.
          allVersions.value = [project.projectVersion, ...allVersions.value];
        }

        await setProjectApiStore.handleSetProject(project);

        if (document) {
          // If a document is given, switch to it.
          await documentStore.switchDocuments(document);
        }

        if (!doNavigate || routeRequiresProject) return;

        await navigateTo(Routes.ARTIFACT, {
          [QueryParams.VERSION]: versionId,
        });
      },
      {},
      { useAppLoad: true }
    );
  }

  /**
   * Load the current version of the given project.
   *
   * @param identifier - The project to load the current version of.
   */
  async function handleLoadCurrentVersion(
    identifier: IdentifierSchema
  ): Promise<void> {
    const versions = await getProjectVersions(identifier.projectId);

    await handleLoadVersion(versions[0].versionId);
  }

  // Load the versions of the current project on mount.
  onMounted(() => handleLoadCurrentProjectVersions());

  // Load the versions of the current project whenever the current project changes.
  watch(
    () => currentProject.value,
    () => handleLoadCurrentProjectVersions()
  );

  return {
    allVersions,
    currentVersion,
    handleLoadVersion,
    handleLoadCurrentVersion,
  };
});

export default useGetVersionApi(pinia);
