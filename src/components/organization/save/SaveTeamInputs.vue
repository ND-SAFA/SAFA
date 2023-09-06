<template>
  <div class="long-input q-mx-auto">
    <text-input label="Team Name" hint="Required" data-cy="input-org-name" />
    <flex-box full-width justify="end">
      <text-button color="primary" label="Save" data-cy="button-org-save" />
    </flex-box>
  </div>
</template>

<script lang="ts">
/**
 * Inputs for creating a team.
 */
export default {
  name: "SaveTeamInputs",
};
</script>

<script setup lang="ts">
import { FlexBox, TextButton, TextInput } from "@/components/common";
</script>
