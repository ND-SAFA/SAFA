<template>
  <div>
    <text-input
      label="Organization Name"
      hint="Required"
      data-cy="input-org-name"
    />
    <text-input
      label="Organization Description"
      type="textarea"
      data-cy="input-org-description"
    />
    <flex-box full-width justify="end">
      <text-button color="primary" label="Save" data-cy="button-org-save" />
    </flex-box>
  </div>
</template>

<script lang="ts">
/**
 * Inputs for editing an organization.
 */
export default {
  name: "SaveOrganizationInputs",
};
</script>

<script setup lang="ts">
import { FlexBox, TextButton, TextInput } from "@/components/common";
</script>
