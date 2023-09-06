<template>
  <panel-card title="My Team">
    <template #title-actions>
      <text-button
        v-if="editMode"
        text
        label="Cancel"
        icon="cancel"
        @click="appStore.closePanel(PanelType.teamEditor)"
      />
    </template>

    <div v-if="!editMode">
      <flex-box full-width>
        <attribute-chip value="<#> Members" />
        <attribute-chip value="<#> Projects" />
      </flex-box>

      <typography variant="caption" value="Description" />
      <br />
      <typography value="<Organization information>" />
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
import { PanelType } from "@/types";
import { appStore } from "@/hooks";
import {
  AttributeChip,
  FlexBox,
  PanelCard,
  TextButton,
  Typography,
} from "@/components/common";
import SaveTeamInputs from "./SaveTeamInputs.vue";

const editMode = computed(() => appStore.isTeamEditorOpen);
</script>
