<template>
  <panel-card v-if="permissionStore.isSuperuser" title="Admin Controls">
    <q-toggle v-model="adminApiStore.activeSuperuser" class="q-ma-md">
      <template #default>
        <typography value="Superuser mode" el="div" />
        <typography secondary value="Enables all permissions" />
      </template>
    </q-toggle>
    <expansion-item
      label="Create Account"
      :disable="!adminApiStore.activeSuperuser"
    >
      <email-input v-model="adminCreateEmail" />
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
    <expansion-item
      label="Enable Superuser"
      :disable="!adminApiStore.activeSuperuser"
    >
      <email-input v-model="adminSuperuserEmail" />
      <text-button
        block
        outlined
        color="primary"
        label="Enable Superuser"
        icon="invite"
        @click="handleAdminSuperuser"
      />
    </expansion-item>
    <expansion-item
      label="Enable Generation"
      :disable="!adminApiStore.activeSuperuser"
    >
      <select-input
        v-model="orgApiStore.currentOrg"
        :options="orgStore.allOrgs"
        label="Organization"
        option-value="id"
        option-label="name"
        class="q-mb-md"
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
    <expansion-item
      label="Reset Password"
      :disable="!adminApiStore.activeSuperuser"
    >
      <email-input v-model="adminResetEmail" />
      <text-button
        block
        outlined
        color="primary"
        label="Reset Password"
        icon="redo"
        @click="handleResetPassword"
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
  orgApiStore,
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
  SelectInput,
  EmailInput,
} from "@/components/common";

const adminCreateEmail = ref("");
const adminCreatePassword = ref("");
const adminSuperuserEmail = ref("");
const adminResetEmail = ref("");

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

/**
 * As an admin, resets the password of the given account.
 */
function handleResetPassword() {
  adminApiStore.handleAdminPasswordReset(adminResetEmail.value);
}
</script>
