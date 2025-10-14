import { defineStore } from "pinia";

import { computed } from "vue";
import {
  IdentifierSchema,
  IOHandlerCallback,
  VersionSchema,
  GetVersionApiHook,
} from "@/types";
import { versionToString } from "@/util";
import {
  artifactStore,
  chatApiStore,
  documentStore,
  logStore,
  projectStore,
  sessionStore,
  setProjectApiStore,
  useApi,
  viewsStore,
} from "@/hooks";
import { navigateTo, QueryParams, Routes, router } from "@/router";
import {
  deleteProjectVersion,
  getProjectVersion,
  getProjectVersions,
} from "@/api";
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
    const deleteVersionApi = useApi("deleteVersionApi");

    const getLoading = computed(() => getVersionApi.loading);
    const loadLoading = computed(() => loadVersionApi.loading);
    const deleteLoading = computed(() => deleteVersionApi.loading);

    const currentProject = computed({
      get: () => (projectStore.projectId ? projectStore.project : undefined),
      set(identifier: IdentifierSchema | undefined) {
        if (!identifier) return;

        handleLoadCurrent(identifier);
      },
    });
    const currentVersion = computed({
      get: () => projectStore.version,
      set(version: VersionSchema | undefined) {
        if (!version) return;

        handleLoad(version.versionId);
      },
    });

    async function handleLoadVersions(
      projectId?: string,
      callbacks: IOHandlerCallback<VersionSchema[]> = {}
    ): Promise<void> {
      const id = projectId || currentProject.value?.projectId;

      await getVersionApi.handleRequest(async () => {
        const versions = id ? await getProjectVersions(id) : [];

        if (!projectId) {
          projectStore.allVersions = versions;
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

          await setProjectApiStore.handleSet(project);
          await handleLoadVersions();
          await chatApiStore.handleGetProjectChats();

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

    function handleDelete(
      version: VersionSchema,
      callbacks: IOHandlerCallback = {}
    ): void {
      const name = versionToString(version);

      logStore.confirm(
        `Delete Version`,
        `Are you sure you would like to delete "${name}"?`,
        async (isConfirmed: boolean) => {
          if (!isConfirmed) return;

          await deleteVersionApi.handleRequest(
            async () => {
              await deleteProjectVersion(version.versionId);

              projectStore.removeVersion(version, (newVersion) =>
                handleLoad(newVersion.versionId)
              );
            },
            {
              ...callbacks,
              success: `Version has been deleted: ${name}`,
              error: `Unable to delete version: ${name}`,
            }
          );
        }
      );
    }

    return {
      getLoading,
      loadLoading,
      deleteLoading,
      currentProject,
      currentVersion,
      handleLoadVersions,
      handleLoad,
      handleLoadCurrent,
      handleDelete,
    };
  }
);

export default useGetVersionApi(pinia);
