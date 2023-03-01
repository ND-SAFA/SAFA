<template>
  <tab-list v-model="tab" :tabs="tabs">
    <template #before>
      <typography r="4" el="h2" variant="subtitle" value="Layouts" />
    </template>
    <template #after>
      <text-button v-if="!createOpen" text icon="add" @click="handleAddLayout">
        Add Layout
      </text-button>
    </template>
    <template v-for="({ id }, idx) in tabs" #[id] :key="id">
      <save-attribute-layout
        v-if="idx === tab"
        :layout="layouts[idx]"
        @save="handleSaveLayout(id)"
      />
    </template>
  </tab-list>
</template>

<script lang="ts">
/**
 * Allows for editing attribute layouts.
 */
export default {
  name: "AttributeLayoutEditor",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { SelectOption } from "@/types";
import { attributesStore } from "@/hooks";
import { TabList, TextButton, Typography } from "@/components/common";
import SaveAttributeLayout from "./SaveAttributeLayout.vue";

const createOpen = ref(false);

const tab = computed({
  get() {
    return attributesStore.selectedLayoutId;
  },
  set(tab) {
    attributesStore.selectedLayoutId = tab;
  },
});

const layouts = computed(() => attributesStore.attributeLayouts);

const tabs = computed<SelectOption[]>(() => {
  const tabs = attributesStore.attributeLayouts.map(({ id, name }) => ({
    id,
    name,
  }));

  if (createOpen.value) {
    tabs.push({ id: "", name: "New Layout" });
  }

  return tabs;
});

/**
 * Adds a new attribute layout.
 */
function handleAddLayout(): void {
  createOpen.value = true;
  tab.value = "";
}

/**
 * Closes the layout creator on save.
 * @param id - The id of the saved layout.
 */
function handleSaveLayout(id: string): void {
  createOpen.value = false;
  tab.value = id;
}
</script>
