<template>
  <q-select
    v-model="getProjectApiStore.currentProject"
    outlined
    dark
    :options-dark="darkMode"
    label="Project"
    :options="getProjectApiStore.allProjects"
    option-value="projectId"
    option-label="name"
    class="nav-input"
    color="primary"
    @popup-show="getProjectApiStore.handleReload()"
  >
    <template #option="{ opt, itemProps }">
      <list-item
        v-bind="itemProps"
        :title="opt.name"
        :action-cols="2"
        :data-cy-name="opt.name"
      >
        <template #actions>
          <flex-box justify="end">
            <icon-button
              v-if="sessionStore.isEditor(opt)"
              small
              :tooltip="`Edit ${opt.name}`"
              icon="edit"
              data-cy="button-project-edit"
              @click="identifierSaveStore.selectIdentifier(opt, 'save')"
            />
            <icon-button
              v-if="sessionStore.isOwner(opt)"
              small
              :tooltip="`Delete ${opt.name}`"
              icon="delete"
              data-cy="button-project-delete"
              @click="identifierSaveStore.selectIdentifier(opt, 'delete')"
            />
          </flex-box>
        </template>
      </list-item>
    </template>
    <template #after-options>
      <text-button
        text
        block
        label="Add Project"
        icon="add"
        @click="identifierSaveStore.selectIdentifier(undefined, 'save')"
      />
    </template>
  </q-select>
</template>

<script lang="ts">
/**
 Displays the current project, and allows it to be changed.
 */
export default {
  name: "ProjectSelector",
};
</script>

<script setup lang="ts">
import {
  getProjectApiStore,
  identifierSaveStore,
  sessionStore,
  useTheme,
} from "@/hooks";
import { FlexBox, IconButton, ListItem, TextButton } from "@/components/common";

const { darkMode } = useTheme();
</script>
