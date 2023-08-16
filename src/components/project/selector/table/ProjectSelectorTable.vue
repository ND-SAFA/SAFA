<template>
  <selector-table
    v-model:selected="selectedItems"
    :minimal="props.minimal"
    addable
    :editable="isEditable"
    :deletable="isDeletable"
    :loading="getProjectApiStore.loading"
    :columns="columns"
    :rows="rows"
    row-key="projectId"
    item-name="Project"
    data-cy="table-project"
    @refresh="handleReload"
    @row:add="identifierSaveStore.selectIdentifier(undefined, 'save')"
    @row:edit="identifierSaveStore.selectIdentifier($event, 'save')"
    @row:delete="identifierSaveStore.selectIdentifier($event, 'delete')"
  >
    <template #cell-actions="{ row }">
      <icon-button
        v-if="isEditable(row)"
        :small="props.minimal"
        :tooltip="`Invite to ${row.name}`"
        icon="invite"
        data-cy="button-project-invite"
        @click="projectInviteId = row.projectId"
      />
      <icon-button
        v-if="row.members.length > 1"
        :small="props.minimal"
        icon="leave"
        tooltip="Leave project"
        data-cy="button-selector-leave"
        @click="handleLeave(row)"
      />
    </template>
  </selector-table>

  <project-member-modal
    :open="!!projectInviteId"
    :project-id="projectInviteId"
    @close="projectInviteId = undefined"
    @submit="projectInviteId = undefined"
  />
</template>

<script lang="ts">
/**
 * A table for selecting projects.
 */
export default {
  name: "ProjectSelectorTable",
};
</script>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { IdentifierSchema, ProjectRole } from "@/types";
import {
  actionsColumn,
  projectExpandedColumns,
  projectNameColumn,
} from "@/util";
import {
  getProjectApiStore,
  identifierSaveStore,
  logStore,
  memberApiStore,
  permissionStore,
  sessionStore,
} from "@/hooks";
import { SelectorTable, IconButton } from "@/components/common";
import { ProjectMemberModal } from "@/components/settings";

const props = defineProps<{
  /**
   * Whether this component is currently in view.
   * The content will be reloaded when opened.
   */
  open: boolean;
  /**
   * Whether to display minimal information.
   */
  minimal?: boolean;
}>();

const emit = defineEmits<{
  /**
   * Emitted when the selected project changes.
   */
  (e: "selected", project: IdentifierSchema | undefined): void;
}>();

const currentRoute = useRoute();

const selected = ref<IdentifierSchema | undefined>();
const projectInviteId = ref<string>();

const selectedItems = computed({
  get() {
    return selected.value ? [selected.value] : [];
  },
  set(items: IdentifierSchema[]) {
    selected.value = items[0];
    emit("selected", items[0]);
  },
});

const columns = computed(() =>
  props.minimal
    ? [projectNameColumn, actionsColumn]
    : [projectNameColumn, ...projectExpandedColumns]
);

const rows = computed(() => getProjectApiStore.allProjects);

/**
 * Loads all projects.
 */
function handleReload() {
  selected.value = undefined;
  projectInviteId.value = undefined;

  getProjectApiStore.handleReload();
}

/**
 * Removes the current user from the project.
 * @param project - The project to leave.
 */
function handleLeave(project: IdentifierSchema) {
  const member = sessionStore.getProjectMember(project);
  const ownerCount = project.members.filter(
    (member) => member.role === ProjectRole.OWNER
  ).length;

  if (!member || (member.role === ProjectRole.OWNER && ownerCount === 1)) {
    logStore.onInfo("You cannot remove the only owner of this project.");
  } else {
    memberApiStore.handleDelete(member);
  }
}

/**
 * Whether the current user can edit the project.
 * @param project - The project to check.
 * @returns Whether the current user can edit the project.
 */
function isEditable(project: IdentifierSchema): boolean {
  return permissionStore.projectAllows("editor", project);
}

/**
 * Whether the current user can delete the project.
 * @param project - The project to check.
 * @returns Whether the current user can delete the project.
 */
function isDeletable(project: IdentifierSchema): boolean {
  return permissionStore.projectAllows("owner", project);
}

/**
 * Loads all projects when opened.
 */
watch(
  () => props.open,
  (open) => {
    if (!open) return;

    handleReload();
  }
);

/**
 * Loads all projects when the page changes.
 */
watch(
  () => currentRoute.path,
  () => handleReload()
);

/**
 * Loads all projects when mounted.
 */
onMounted(() => handleReload());
</script>
