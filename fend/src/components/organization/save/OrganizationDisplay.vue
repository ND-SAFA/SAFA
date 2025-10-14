<template>
  <panel-card :title="org.name">
    <template #title-actions>
      <text-button
        v-if="editMode"
        text
        label="Cancel"
        icon="cancel"
        @click="appStore.close('saveOrg')"
      />
    </template>

    <div v-if="!editMode">
      <flex-box full-width>
        <attribute-chip :value="teamCount" />
        <attribute-chip :value="memberCount" />
        <attribute-chip :value="projectCount" />
      </flex-box>

      <typography variant="caption" value="Description" />
      <br />
      <typography :value="org.description" />
    </div>

    <save-organization-inputs v-else />
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays an organization.
 */
export default {
  name: "OrganizationDisplay",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { appStore, orgStore } from "@/hooks";
import {
  AttributeChip,
  FlexBox,
  PanelCard,
  TextButton,
  Typography,
} from "@/components/common";
import SaveOrganizationInputs from "./SaveOrganizationInputs.vue";

const editMode = computed(() => appStore.popups.saveOrg);

const org = computed(() => orgStore.org);

const teamCount = computed(() => orgStore.org.teams.length + " Teams");
const memberCount = computed(() => orgStore.org.members.length + " Members");
const projectCount = computed(
  () =>
    orgStore.org.teams
      .map(({ projects }) => projects.length)
      .reduce((a, b) => a + b, 0) + " Projects"
);
</script>
