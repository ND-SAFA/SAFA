<template>
  <icon-button
    icon="permission"
    tooltip="Edit roles"
    :loading="loading"
    data-cy="button-member-roles"
  >
    <icon variant="down" size="xs" style="width: 10px" />
    <q-menu>
      <list>
        <list-item
          v-for="role in projectRoles"
          :key="role.id"
          clickable
          :title="role.id"
          :subtitle="role.name"
          @click="handleSave(role.id as ProjectRole)"
        />
      </list>
    </q-menu>
  </icon-button>
</template>

<script lang="ts">
/**
 * A dropdown button for editing member roles.
 */
export default {
  name: "MemberRoleButton",
};
</script>

<script setup lang="ts">
import { ref } from "vue";
import { MemberRoleButtonProps, ProjectRole } from "@/types";
import { projectRoleOptions } from "@/util";
import { memberApiStore } from "@/hooks";
import { IconButton, ListItem, Icon, List } from "@/components/common";

const props = defineProps<MemberRoleButtonProps>();

const projectRoles = projectRoleOptions();

const loading = ref(false);

/**
 * Updates the project member's role.
 */
function handleSave(role: ProjectRole) {
  loading.value = true;

  memberApiStore.handleSaveRole(props.projectId, props.member.email, role, {
    onComplete: () => (loading.value = false),
  });
}
</script>
