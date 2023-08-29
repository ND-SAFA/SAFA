<template>
  <panel-card title="My Organization">
    <template #title-actions>
      <icon-button tooltip="Switch organizations" icon="organization">
        <icon variant="down" size="xs" style="width: 10px" />
        <q-menu>
          <list>
            <list-item clickable title="Other Organization" />
          </list>
        </q-menu>
      </icon-button>
    </template>
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
import {
  PanelCard,
  IconButton,
  List,
  ListItem,
  Icon,
} from "@/components/common";
</script>
