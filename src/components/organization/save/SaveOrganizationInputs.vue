<template>
  <div>
    <text-input
      v-model="name"
      label="Organization Name"
      hint="Required"
      data-cy="input-org-name"
    />
    <text-input
      v-model="description"
      label="Organization Description"
      type="textarea"
      data-cy="input-org-description"
    />
    <flex-box full-width justify="end">
      <text-button
        color="primary"
        label="Save"
        data-cy="button-org-save"
        @click="handleSave"
      />
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
import { computed, ref } from "vue";
import { orgApiStore, orgStore } from "@/hooks";
import { FlexBox, TextButton, TextInput } from "@/components/common";

const org = computed(() => orgStore.org);

const name = ref(org.value.name);
const description = ref(org.value.description);

/**
 * Saves the edited organization.
 */
function handleSave() {
  orgApiStore.handleEdit({
    ...org.value,
    name: name.value,
    description: description.value,
  });
}
</script>
