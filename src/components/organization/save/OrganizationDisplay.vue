<template>
  <panel-card title="My Organization">
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
        <attribute-chip value="<#> Teams" />
        <attribute-chip value="<#> Members" />
        <attribute-chip value="<#> Projects" />
      </flex-box>

      <typography variant="caption" value="Description" />
      <br />
      <typography value="<Organization information>" />
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
import { appStore } from "@/hooks";
import {
  AttributeChip,
  FlexBox,
  PanelCard,
  TextButton,
  Typography,
} from "@/components/common";
import SaveOrganizationInputs from "./SaveOrganizationInputs.vue";

const editMode = computed(() => appStore.popups.saveOrg);
</script>
