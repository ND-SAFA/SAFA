import { defineStore } from "pinia";

import { computed } from "vue";
import {
  GetProjectApiHook,
  IdentifierSchema,
  IOHandlerCallback,
} from "@/types";
import {
  getVersionApiStore,
  projectStore,
  sessionStore,
  useApi,
} from "@/hooks";
import { getParam, navigateTo, QueryParams, Routes } from "@/router";
import { getCurrentVersion, getProjects } from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing get project API requests.
 */
export const useGetProjectApi = defineStore(
  "getProjectApi",
  (): GetProjectApiHook => {
    const getProjectApi = useApi("getProjectApi");

    const loading = computed(() => getProjectApi.loading);

    const currentProject = computed({
      get: () => (projectStore.projectId ? projectStore.project : undefined),
      set(identifier: IdentifierSchema | undefined) {
        if (!identifier) return;

        getVersionApiStore.handleLoadCurrent(identifier);
      },
    });

    async function handleReload(
      callbacks: IOHandlerCallback = {}
    ): Promise<void> {
      console.trace("!");
      if (!sessionStore.doesSessionExist) {
        callbacks.onSuccess?.();
        return;
      }

      await getProjectApi.handleRequest(
        async () => {
          projectStore.allProjects = await getProjects();
        },
        {
          ...callbacks,
          error: "Unable to load your projects.",
        }
      );
    }

    async function handleLoadRecent(): Promise<void> {
      if (!sessionStore.doesSessionExist) return;

      let versionId = getParam(QueryParams.VERSION);

      if (!versionId) {
        if (projectStore.allProjects.length > 0) {
          versionId = (
            await getCurrentVersion(projectStore.allProjects[0].projectId)
          ).versionId;
        }
      }
      if (typeof versionId === "string") {
        await getVersionApiStore.handleLoad(versionId).catch(() => {
          navigateTo(Routes.HOME);
        });
      } else {
        await navigateTo(Routes.HOME);
      }
    }

    return {
      loading,
      currentProject,
      handleReload,
      handleLoadRecent,
    };
  }
);

export default useGetProjectApi(pinia);
