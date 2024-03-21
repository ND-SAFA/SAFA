import { defineStore } from "pinia";

import { computed } from "vue";
import { GetProjectApiHook, IOHandlerCallback } from "@/types";
import { getVersionApiStore, projectStore, useApi } from "@/hooks";
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

    async function handleLoadProjects(
      callbacks: IOHandlerCallback = {}
    ): Promise<void> {
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
      let versionId = getParam(QueryParams.VERSION);

      if (!versionId && projectStore.allProjects.length > 0) {
        versionId = (
          await getCurrentVersion(projectStore.allProjects[0].projectId)
        ).versionId;
      }

      if (typeof versionId === "string") {
        await getVersionApiStore
          .handleLoad(versionId)
          .catch(() => navigateTo(Routes.HOME));
      } else {
        await navigateTo(Routes.HOME);
      }
    }

    return {
      loading,
      handleLoadProjects,
      handleLoadRecent,
    };
  }
);

export default useGetProjectApi(pinia);
