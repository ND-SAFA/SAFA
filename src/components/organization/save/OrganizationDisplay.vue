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

  <panel-card v-if="permissionStore.isSuperuser" title="Admin Controls">
    <expansion-item label="Toggle Superuser Mode">
      <q-toggle v-model="adminApiStore.activeSuperuser" class="q-mr-md">
        <template #default>
          <typography value="Superuser mode" el="div" />
          <typography secondary value="Enables all permissions" />
        </template>
      </q-toggle>
    </expansion-item>
    <expansion-item label="Create Account">
      <text-input v-model="adminCreateEmail" label="Email" />
      <text-input v-model="adminCreatePassword" label="Password" />
      <text-button
        text
        color="primary"
        label="Create Account"
        icon="invite"
        @click="handleAdminCreate"
      />
    </expansion-item>
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
import { computed, ref } from "vue";
import {
  adminApiStore,
  appStore,
  orgStore,
  permissionStore,
  sessionApiStore,
  sessionStore,
} from "@/hooks";
import {
  AttributeChip,
  FlexBox,
  PanelCard,
  TextButton,
  Typography,
  ExpansionItem,
  TextInput,
} from "@/components/common";
import SaveOrganizationInputs from "./SaveOrganizationInputs.vue";

const adminCreateEmail = ref("");
const adminCreatePassword = ref("");

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

/**
 * As an admin, creates a pre-verified account.
 */
function handleAdminCreate() {
  sessionApiStore.handleCreateAccount(
    {
      email: adminCreateEmail.value,
      password: adminCreatePassword.value,
    },
    true
  );
}
</script>
