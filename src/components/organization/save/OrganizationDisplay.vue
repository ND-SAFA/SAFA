<template>
  <panel-card title="My Organization">
    <template #title-actions>
      <text-button
        v-if="editMode"
        text
        label="Cancel"
        icon="cancel"
        @click="appStore.closePanel(PanelType.organizationEditor)"
      />
    </template>

    <div v-if="!editMode">
      <flex-box full-width>
        <attribute-chip value="3 Teams" />
        <attribute-chip value="15 Members" />
        <attribute-chip value="30 Projects" />
      </flex-box>

      <typography variant="caption" value="Description" />
      <br />
      <typography value="<Organization information will be displayed here>" />
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
import { PanelType } from "@/types";
import { appStore } from "@/hooks";
import {
  AttributeChip,
  FlexBox,
  PanelCard,
  TextButton,
  Typography,
} from "@/components/common";
import { SaveOrganizationInputs } from "@/components/organization/save";

const editMode = computed(() => appStore.isOrgEditorOpen);
</script>
