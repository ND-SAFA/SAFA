<template>
  <panel-card :title="team.name">
    <template #title-actions>
      <text-button
        v-if="editMode"
        text
        label="Cancel"
        icon="cancel"
        @click="appStore.close('saveTeam')"
      />
    </template>

    <div v-if="!editMode">
      <flex-box full-width>
        <attribute-chip :value="memberCount" />
        <attribute-chip :value="projectCount" />
      </flex-box>
    </div>

    <save-team-inputs v-else />
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays a team.
 */
export default {
  name: "OrganizationDisplay",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { appStore, teamStore } from "@/hooks";
import {
  AttributeChip,
  FlexBox,
  PanelCard,
  TextButton,
} from "@/components/common";
import SaveTeamInputs from "./SaveTeamInputs.vue";

const editMode = computed(() => appStore.popups.saveTeam);

const team = computed(() => teamStore.team);

const memberCount = computed(() => team.value.members.length + " Members");
const projectCount = computed(() => team.value.projects.length + " Members");
</script>
