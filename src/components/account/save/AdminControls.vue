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
 * Displays controls for admins.
 */
export default {
  name: "AdminControls",
};
</script>

<script setup lang="ts">
import { ref } from "vue";
import { adminApiStore, permissionStore, sessionApiStore } from "@/hooks";
import {
  PanelCard,
  TextButton,
  Typography,
  ExpansionItem,
  TextInput,
} from "@/components/common";

const adminCreateEmail = ref("");
const adminCreatePassword = ref("");

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
