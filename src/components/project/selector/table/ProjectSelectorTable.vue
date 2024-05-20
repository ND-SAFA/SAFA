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
    item-name="project"
    :icons="{
      add: 'project-add',
      edit: 'project-edit',
      delete: 'project-delete',
    }"
    data-cy="table-project"
    :custom-cells="['name']"
    @refresh="handleReload"
    @row:add="identifierSaveStore.selectIdentifier(undefined, 'save')"
    @row:edit="identifierSaveStore.selectIdentifier($event, 'save')"
    @row:delete="identifierSaveStore.selectIdentifier($event, 'delete')"
  >
    <template #body-cell-name="{ row }: { row: ProjectSchema }">
      <q-td style="max-width: 400px">
        <typography :value="row.name" />
        <typography
          :value="row.description"
          secondary
          el="div"
          class="text-ellipsis"
        />
      </q-td>
    </template>
    <template #cell-actions="{ row }: { row: ProjectSchema }">
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

  <invite-member-modal
    :open="!!projectInviteId"
    :entity="entity"
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
import {
  IdentifierSchema,
  MemberEntitySchema,
  ProjectSchema,
  ProjectSelectorTableProps,
} from "@/types";
import { projectColumns, projectNameColumn } from "@/util";
import {
  getProjectApiStore,
  identifierSaveStore,
  memberApiStore,
  permissionStore,
  projectStore,
  sessionStore,
  teamApiStore,
  teamStore,
} from "@/hooks";
import { Routes } from "@/router";
import { SelectorTable, IconButton, Typography } from "@/components/common";
import { InviteMemberModal } from "@/components/members";

const props = defineProps<ProjectSelectorTableProps>();

const emit = defineEmits<{
  /**
   * Emitted when the selected project changes.
   */
  (e: "selected", project: IdentifierSchema | undefined): void;
}>();

const currentRoute = useRoute();

const selected = ref<IdentifierSchema | undefined>();
const projectInviteId = ref<string>();

const columns = computed(() =>
  props.minimal ? [projectNameColumn] : projectColumns
);
const rows = computed(() =>
  props.teamOnly ? teamStore.allProjects : projectStore.allProjects
);

const entity = computed(
  () =>
    ({
      entityId: projectInviteId.value,
      entityType: "PROJECT",
    }) as MemberEntitySchema
);

const selectedItems = computed({
  get() {
    return selected.value ? [selected.value] : [];
  },
  set(items: IdentifierSchema[]) {
    selected.value = items[0];
    emit("selected", items[0]);
  },
});

/**
 * Loads all projects.
 */
function handleReload() {
  selected.value = undefined;
  projectInviteId.value = undefined;

  if (props.teamOnly) {
    teamApiStore.handleLoadProjects();
  } else {
    getProjectApiStore.handleLoadProjects();
  }
}

/**
 * Removes the current user from the project.
 * @param project - The project to leave.
 */
function handleLeave(project: IdentifierSchema) {
  const member = sessionStore.getCurrentMember(project);

  if (!member) return;

  memberApiStore.handleDelete(member, project);
}

/**
 * Whether the current user can edit the project.
 * @param project - The project to check.
 * @returns Whether the current user can edit the project.
 */
function isEditable(project: IdentifierSchema): boolean {
  return permissionStore.isAllowed("project.edit", project);
}

/**
 * Whether the current user can delete the project.
 * @param project - The project to check.
 * @returns Whether the current user can delete the project.
 */
function isDeletable(project: IdentifierSchema): boolean {
  return permissionStore.isAllowed("project.delete", project);
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

watch(
  () => currentRoute.path,
  (path) => {
    if (path !== Routes.PROJECT_CREATOR) return;

    handleReload();
  }
);

onMounted(() => {
  handleReload();
});
</script>
