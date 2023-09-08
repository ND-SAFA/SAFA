import { defineStore } from "pinia";

import { computed } from "vue";
import { IOHandlerCallback, TeamApiHook, TeamSchema } from "@/types";
import { removeMatches } from "@/util";
import { logStore, orgStore, teamStore, useApi } from "@/hooks";
import { createTeam, deleteTeam, editTeam } from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing requests to the teams API.
 */
export const useTeamApi = defineStore("teamApi", (): TeamApiHook => {
  const createTeamApi = useApi("createTeamApi");
  const editTeamApi = useApi("editTeamApi");
  const deleteTeamApi = useApi("deleteTeamApi");

  const createTeamApiLoading = computed(() => createTeamApi.loading);
  const editTeamApiLoading = computed(() => editTeamApi.loading);
  const deleteTeamApiLoading = computed(() => deleteTeamApi.loading);

  async function handleCreate(
    team: TeamSchema,
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    await createTeamApi.handleRequest(
      async () => {
        const createdTeam = await createTeam(orgStore.orgId, team);

        orgStore.org.teams.push(createdTeam);
        teamStore.team = createdTeam;
      },
      {
        ...callbacks,
        success: `Team has been created: ${team.name}`,
        error: `Unable to create team: ${team.name}`,
      }
    );
  }

  async function handleEdit(
    team: TeamSchema,
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    await editTeamApi.handleRequest(
      async () => {
        const editedTeam = await editTeam(orgStore.orgId, team);

        orgStore.org.teams = [
          ...removeMatches(orgStore.org.teams, "id", [team.id]),
          editedTeam,
        ];
        teamStore.team = editedTeam;
      },
      {
        ...callbacks,
        success: `Team has been updated: ${team.name}`,
        error: `Unable to update team: ${team.name}`,
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

            orgStore.org.teams = removeMatches(orgStore.org.teams, "id", [
              team.id,
            ]);

            if (teamStore.teamId !== team.id) return;

            // Clear the current team if it was deleted.
            teamStore.$reset();
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
    createTeamApiLoading,
    editTeamApiLoading,
    deleteTeamApiLoading,
    handleCreate,
    handleEdit,
    handleDelete,
  };
});

export default useTeamApi(pinia);
