<template>
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
        block
        outlined
        color="primary"
        label="Create Account"
        icon="invite"
        @click="handleAdminCreate"
      />
    </expansion-item>
    <expansion-item label="Enable Superuser">
      <text-input v-model="adminSuperuserEmail" label="Email" />
      <text-button
        block
        outlined
        color="primary"
        label="Enable Superuser"
        icon="invite"
        @click="handleAdminSuperuser"
      />
    </expansion-item>
    <expansion-item label="Enable Generation">
      <select-input
        v-model="orgStore.org"
        :options="orgStore.allOrgs"
        label="Organization"
        option-value="id"
        option-label="name"
      />
      <text-button
        block
        outlined
        color="primary"
        label="Enable Generation"
        icon="invite"
        @click="handleEnableGeneration"
      />
    </expansion-item>
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays controls for admins.
 */
export default {
  name: "AdminControls",
};
</script>

<script setup lang="ts">
import { ref } from "vue";
import {
  adminApiStore,
  orgStore,
  permissionStore,
  sessionApiStore,
} from "@/hooks";
import {
  PanelCard,
  TextButton,
  Typography,
  ExpansionItem,
  TextInput,
} from "@/components/common";
import SelectInput from "@/components/common/input/SelectInput.vue";

const adminCreateEmail = ref("");
const adminCreatePassword = ref("");
const adminSuperuserEmail = ref("");

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

/**
 * As an admin, sets an account as a superuser.
 */
function handleAdminSuperuser() {
  adminApiStore.enableSuperuser({
    email: adminSuperuserEmail.value,
  });
}

/**
 * As an admin, sets an account to recurring billing to allow generation.
 */
function handleEnableGeneration() {
  adminApiStore.updatePaymentTier(orgStore.org, "RECURRING");
}
</script>
