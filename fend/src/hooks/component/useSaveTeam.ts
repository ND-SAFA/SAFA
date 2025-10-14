import { defineStore } from "pinia";

import { TeamSchema } from "@/types";
import { buildTeam } from "@/util";
import { pinia } from "@/plugins";

/**
 * The save team store assists in creating and editing organization teams.
 */
export const useSaveTeam = defineStore("saveTeam", {
  state: () => ({
    /**
     * A base team being edited.
     */
    baseTeam: undefined as TeamSchema | undefined,
    /**
     * The team being created or edited.
     */
    editedTeam: buildTeam(),
  }),
  getters: {
    /**
     * @return Whether an existing team is being updated.
     */
    isUpdate(): boolean {
      return !!this.baseTeam;
    },
    /**
     * @return Whether the team can be saved.
     */
    canSave(): boolean {
      return this.editedTeam.name.length > 0;
    },
  },
  actions: {
    /**
     * Resets the team value to the given base value.
     */
    resetTeam(team?: TeamSchema): void {
      if (team) {
        this.baseTeam = team;
      }

      this.editedTeam = buildTeam(this.baseTeam);
    },
  },
});

export default useSaveTeam(pinia);
