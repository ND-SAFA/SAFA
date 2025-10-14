<template>
  <text-button
    text
    icon="permission"
    :label="props.member.role"
    :loading="loading"
    data-cy="button-member-role"
  >
    <icon variant="down" size="xs" />
    <q-menu>
      <list>
        <list-item
          v-for="role in projectRoles"
          :key="role.id"
          clickable
          :title="role.id"
          :subtitle="role.name"
          @click="handleSave(role.id as MemberRole)"
        />
      </list>
    </q-menu>
  </text-button>
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
import { computed, ref } from "vue";
import { MemberRoleButtonProps, MemberRole } from "@/types";
import { memberRoleOptions } from "@/util";
import { memberApiStore } from "@/hooks";
import { TextButton, ListItem, Icon, List } from "@/components/common";

const props = defineProps<MemberRoleButtonProps>();

const projectRoles = computed(() => memberRoleOptions(props.member.entityType));

const loading = ref(false);

/**
 * Updates the project member's role.
 */
function handleSave(role: MemberRole) {
  loading.value = true;

  memberApiStore.handleSaveRole(
    { ...props.member, role },
    {
      onComplete: () => (loading.value = false),
    }
  );
}
</script>
