<template>
  <panel-card :minimal="props.minimal">
    <template #title-actions>
      <text-button
        v-if="addMode"
        text
        label="Cancel"
        icon="cancel"
        @click="handleClose"
      />
    </template>

    <selector-table
      v-if="!addMode"
      :columns="membersColumns"
      :rows="rows"
      row-key="email"
      :item-name="itemName"
      addable
      :deletable="displayMemberActions"
      :loading="memberApiStore.loading"
      :custom-cells="['role']"
      :icons="{ add: 'member-add', delete: 'member-delete', edit: 'edit' }"
      @row:add="handleAdd"
      @row:delete="handleDelete"
      @refresh="handleRefresh"
    >
      <template #search-append="{ search }">
        <icon-button
          v-if="!!search"
          small
          tooltip="Invite member"
          icon="invite"
          @click="handleAdd(search)"
        />
      </template>

      <template #body-cell-role="{ row }: { row: MembershipSchema }">
        <q-td align="end">
          <member-role-button v-if="displayMemberActions" :member="row" />
          <typography v-else :value="row.role" />
        </q-td>
      </template>

      <template #cell-actions="{ row }: { row: MembershipSchema }">
        <icon-button
          v-if="permissionStore.isSuperuser"
          icon="security"
          tooltip="Create superuser"
          data-cy="button-member-superuser"
          @click="handleSuperuser(row)"
        />
        <icon-button
          v-if="row.email === userEmail"
          icon="leave"
          tooltip="Leave project"
          data-cy="button-member-leave"
          @click="handleDelete(row)"
        />
      </template>
    </selector-table>

    <invite-member-inputs
      v-else
      :entity="props.entity"
      :email="addedMember"
      @save="handleClose"
    />
  </panel-card>
</template>

<script lang="ts">
/**
 * A table for managing members of a project, team, or organization.
 */
export default {
  name: "MemberTable",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import {
  MembershipSchema,
  MembershipType,
  MemberTableProps,
  PermissionType,
} from "@/types";
import { membersColumns } from "@/util";
import {
  adminApiStore,
  memberApiStore,
  membersStore,
  permissionStore,
  projectStore,
  sessionStore,
} from "@/hooks";
import {
  PanelCard,
  SelectorTable,
  IconButton,
  TextButton,
  Typography,
} from "@/components/common";
import {
  InviteMemberInputs,
  MemberRoleButton,
} from "@/components/members/save";

const props = defineProps<MemberTableProps>();

const addedMember = ref<string | null>(null);
const addMode = ref(false);

const name = computed(() => props.entity.entityType?.toLowerCase() || "");
const itemName = computed(() => `${name.value} member`);

const entityType = computed(() => props.entity.entityType || "PROJECT");

const memberPermission = computed(
  () =>
    (
      ({
        PROJECT: "project.edit_members",
        TEAM: "team.edit_members",
        ORGANIZATION: "org.edit_members",
      }) as Record<MembershipType, PermissionType>
    )[entityType.value]
);

const displayMemberActions = computed(() =>
  permissionStore.isAllowed(
    memberPermission.value,
    permissionStore.getCurrentContext(entityType.value)
  )
);

const rows = computed(() => membersStore.getMembers(entityType.value));

const userEmail = computed(() => sessionStore.user?.email);

/**
 * Loads the project's members.
 */
async function handleRefresh(): Promise<void> {
  if (projectStore.projectId === "") return;

  await memberApiStore.handleReload(props.entity);
}

/**
 * Clears all member modal state.
 */
function handleClose(): void {
  addedMember.value = "";
  addMode.value = false;
}

/**
 * Opens the invite member modal.
 * @param email - The member email to invite.
 */
function handleAdd(email: string | null): void {
  addedMember.value = email;
  addMode.value = true;
}

/**
 * Opens the delete member modal, if the member is not the only owner.
 * @param member - The member to delete.
 */
function handleDelete(member: MembershipSchema): void {
  memberApiStore.handleDelete(member);
}

/**
 * Enables superuser access for the member.
 * @param member - The member to turn into a superuser.
 */
function handleSuperuser(member: MembershipSchema): void {
  adminApiStore.enableSuperuser(member);
}
</script>
