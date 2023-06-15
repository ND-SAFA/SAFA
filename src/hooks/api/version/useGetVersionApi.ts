import { defineStore } from "pinia";

import { DocumentSchema } from "@/types";
import { documentStore, sessionStore, setProjectApiStore } from "@/hooks";
import { navigateTo, QueryParams, Routes, router } from "@/router";
import { getProjectVersion } from "@/api";
import { useApi } from "@/hooks/api/useApi";
import { pinia } from "@/plugins";

export const useGetVersionApi = defineStore("getVersionApi", () => {
  const getVersionApi = useApi("getVersionApi")();

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

        return getProjectVersion(versionId);
      },
      {
        onSuccess: async (version) => {
          await setProjectApiStore.handleSetProject(version);

          if (document) {
            await documentStore.switchDocuments(document);
          }

          if (!doNavigate || routeRequiresProject) return;

          await navigateTo(Routes.ARTIFACT, {
            [QueryParams.VERSION]: versionId,
          });
        },
      },
      { useAppLoad: true }
    );
  }

  return { handleLoadVersion };
});

export default useGetVersionApi(pinia);
