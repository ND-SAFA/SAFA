import { defineStore } from "pinia";

import { computed, ref, watch } from "vue";
import {
  IdentifierSchema,
  IOHandlerCallback,
  VersionSchema,
  GetVersionApiHook,
} from "@/types";
import {
  artifactStore,
  documentStore,
  projectStore,
  sessionStore,
  setProjectApiStore,
  useApi,
  viewsStore,
} from "@/hooks";
import { navigateTo, QueryParams, Routes, router } from "@/router";
import { getProjectVersion, getProjectVersions } from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing get version API requests.
 * - Watches for changes to the current project to load its versions.
 */
export const useGetVersionApi = defineStore(
  "getVersionApi",
  (): GetVersionApiHook => {
    const getVersionApi = useApi("getVersionApi");
    const loadVersionApi = useApi("loadVersionApi");

    const allVersions = ref<VersionSchema[]>([]);

    const getLoading = computed(() => getVersionApi.loading);
    const loadLoading = computed(() => loadVersionApi.loading);

    const currentProject = computed(() => projectStore.project);
    const currentVersion = computed({
      get: () => projectStore.version,
      set(version: VersionSchema | undefined) {
        if (!version) return;

        handleLoad(version.versionId);
      },
    });

    async function handleReload(
      projectId?: string,
      callbacks: IOHandlerCallback<VersionSchema[]> = {}
    ): Promise<void> {
      const id = projectId || currentProject.value?.projectId;

      await getVersionApi.handleRequest(async () => {
        const versions = id ? await getProjectVersions(id) : [];

        if (!projectId) {
          allVersions.value = versions;
        }

        return versions;
      }, callbacks);
    }

    async function handleLoad(
      versionId: string,
      viewId?: string,
      doNavigate = true,
      callbacks: IOHandlerCallback = {}
    ): Promise<void> {
      const routeRequiresProject = router.currentRoute.value.matched.some(
        ({ meta }) => meta.requiresProject
      );

      await loadVersionApi.handleRequest(
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

          await setProjectApiStore.handleSet(project);

          if (viewId) {
            // If a view is given, switch to the associated artifact or document.
            const artifact = artifactStore.getArtifactById(viewId);
            const document = documentStore.getDocument(viewId);

            if (artifact) {
              await viewsStore.addDocumentOfNeighborhood(artifact);
            } else if (document) {
              await documentStore.switchDocuments(document);
            }
          }

          if (!doNavigate || routeRequiresProject) return;

          await navigateTo(Routes.ARTIFACT, {
            [QueryParams.VERSION]: versionId,
          });
        },
        { useAppLoad: true, ...callbacks }
      );
    }

    async function handleLoadCurrent(
      identifier: Pick<IdentifierSchema, "projectId">,
      callbacks?: IOHandlerCallback
    ): Promise<void> {
      const versions = await getProjectVersions(identifier.projectId);

      await handleLoad(versions[0].versionId, undefined, false, callbacks);
    }

    // Load the versions of the current project whenever the current project changes.
    watch(
      () => currentProject.value,
      () => handleReload()
    );

    return {
      getLoading,
      loadLoading,
      allVersions,
      currentVersion,
      handleReload,
      handleLoad,
      handleLoadCurrent,
    };
  }
);

export default useGetVersionApi(pinia);
