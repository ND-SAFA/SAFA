import { defineStore } from "pinia";

import { IdentifierSchema, OrganizationSchema, TeamSchema } from "@/types";
import { buildTeam, removeMatches } from "@/util";
import { membersStore, permissionStore, sessionStore } from "@/hooks";
import { pinia } from "@/plugins";

/**
 * A store for managing the state of the user's current team.
 */
export const useTeam = defineStore("team", {
  state: () => ({
    /**
     * All teams for the current org.
     */
    allTeams: [] as TeamSchema[],
    /**
     * The currently loaded team.
     */
    team: buildTeam(),
    /**
     * The projects associated with the current team.
     */
    allProjects: [] as IdentifierSchema[],
  }),
  getters: {
    /**
     * @return The current team id.
     */
    teamId(): string {
      return this.team.id;
    },
    /**
     * @return The current organization's teams that allow the current user
     * to create a project.
     */
    teamsWithCreateProject(): TeamSchema[] {
      return this.allTeams.filter((team) =>
        permissionStore.isAllowed("team.create_projects", team)
      );
    },
  },
  actions: {
    /**
     * Initializes the current team.
     * @param team - The team to initialize.
     */
    initialize(team: TeamSchema): void {
      this.team = team;

      this.addTeam(team);
      membersStore.initialize(team.members, "TEAM");
    },
    /**
     * Initializes the team with the given organization.
     * @param org - The organization to initialize the team from.
     */
    initializeOrg(org: OrganizationSchema): void {
      this.allTeams = org.teams;
      this.initialize(
        org.teams.find(({ members = [] }) =>
          members.find(({ email }) => email === sessionStore.userEmail)
        ) ||
          org.teams[0] ||
          buildTeam()
      );
    },
    /**
     * Synchronizes loaded data for the current team.
     */
    sync(allProjects: IdentifierSchema[]): void {
      this.allProjects = allProjects;
    },
    /**
     * Adds a team to the list of all teams.
     * @param team - The team to add.
     */
    addTeam(team: TeamSchema): void {
      this.allTeams = [team, ...removeMatches(this.allTeams, "id", [team.id])];
    },
    /**
     * Removes a team to the list of all teams.
     * - If the team is the current team,
     *   the first team in the list will be set as the current.
     * @param team - The team to remove.
     * @param onCurrentRemoved - The callback to call if the current team is removed.
     *
     */
    removeTeam(
      team: TeamSchema,
      onCurrentRemoved?: (team: TeamSchema) => void
    ): void {
      this.allTeams = removeMatches(this.allTeams, "id", [team.id]);

      if (team.id === this.teamId) {
        this.team = this.allTeams[0] || buildTeam();
        onCurrentRemoved?.(this.team);
      }
    },
  },
});

export default useTeam(pinia);
