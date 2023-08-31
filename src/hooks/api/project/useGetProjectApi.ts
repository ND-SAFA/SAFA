import { defineStore } from "pinia";

import { computed, ref } from "vue";
import {
  GetProjectApiHook,
  IdentifierSchema,
  IOHandlerCallback,
} from "@/types";
import { removeMatches } from "@/util";
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

    const allProjects = ref<IdentifierSchema[]>([]);

    const unloadedProjects = computed(() =>
      allProjects.value.filter(
        ({ projectId }) => projectId !== projectStore.projectId
      )
    );

    const loading = computed(() => getProjectApi.loading);

    const currentProject = computed({
      get: () => (projectStore.projectId ? projectStore.project : undefined),
      set(identifier: IdentifierSchema | undefined) {
        if (!identifier) return;

        getVersionApiStore.handleLoadCurrent(identifier);
      },
    });

    function addProject(project: IdentifierSchema): void {
      allProjects.value = [
        project,
        ...removeMatches(allProjects.value, "projectId", [project.projectId]),
      ];
    }

    async function handleReload(
      callbacks: IOHandlerCallback = {}
    ): Promise<void> {
      if (!sessionStore.doesSessionExist) {
        callbacks.onSuccess?.();
        return;
      }

      await getProjectApi.handleRequest(
        async () => {
          allProjects.value = await getProjects();
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
        if (allProjects.value.length > 0) {
          versionId = (await getCurrentVersion(allProjects.value[0].projectId))
            .versionId;
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
      allProjects,
      unloadedProjects,
      currentProject,
      addProject,
      handleReload,
      handleLoadRecent,
    };
  }
);

export default useGetProjectApi(pinia);
