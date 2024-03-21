import { defineStore } from "pinia";

import { computed } from "vue";
import { IOHandlerCallback, TeamApiHook, TeamSchema } from "@/types";
import { logStore, orgStore, teamStore, useApi } from "@/hooks";
import { createTeam, deleteTeam, editTeam, getTeamProjects } from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing requests to the teams API.
 */
export const useTeamApi = defineStore("teamApi", (): TeamApiHook => {
  const getTeamApi = useApi("getTeamApi");
  const saveTeamApi = useApi("saveTeamApi");
  const deleteTeamApi = useApi("deleteTeamApi");

  const saveTeamApiLoading = computed(() => saveTeamApi.loading);
  const deleteTeamApiLoading = computed(() => deleteTeamApi.loading);

  const currentTeam = computed({
    get: () => teamStore.team,
    set: (team: TeamSchema) => handleUpdate(team),
  });

  async function handleUpdate(team: TeamSchema): Promise<void> {
    teamStore.initialize(team);

    await handleLoadProjects();
  }

  async function handleLoadProjects(): Promise<void> {
    if (!teamStore.team.id) return;

    await getTeamApi.handleRequest(async () => {
      teamStore.sync(await getTeamProjects(teamStore.team.id));
    });
  }

  async function handleSave(
    team: TeamSchema,
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    await saveTeamApi.handleRequest(
      async () => {
        if (!team.id) {
          currentTeam.value = await createTeam(orgStore.orgId, team);
        } else {
          teamStore.initialize(await editTeam(orgStore.orgId, team));
        }
      },
      {
        ...callbacks,
        success: `Team has been saved: ${team.name}`,
        error: `Unable to save team: ${team.name}`,
      }
    );
  }

  async function handleDelete(
    team: TeamSchema,
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    logStore.confirm(
      "Delete Team",
      `Are you sure you want to delete ${team.name}?`,
      async (isConfirmed) => {
        if (!isConfirmed) return;

        await deleteTeamApi.handleRequest(
          async () => {
            await deleteTeam(orgStore.orgId, team);

            teamStore.removeTeam(team, (newTeam) => handleUpdate(newTeam));
          },
          {
            ...callbacks,
            success: `Team has been deleted: ${team.name}`,
            error: `Unable to delete team: ${team.name}`,
          }
        );
      }
    );
  }

  return {
    currentTeam,
    saveTeamApiLoading,
    deleteTeamApiLoading,
    handleLoadProjects,
    handleSave,
    handleDelete,
  };
});

export default useTeamApi(pinia);
