<template>
  <tab-list v-model="tab" :tabs="tabs">
    <template #before>
      <typography r="4" el="h2" variant="subtitle" value="Layouts" />
    </template>
    <template #after>
      <text-button
        v-if="!createOpen"
        text
        label="Add Layout"
        icon="add"
        data-cy="button-attribute-layout-add"
        @click="handleAddLayout"
      />
    </template>
    <template v-for="({ id }, idx) in tabs" #[id] :key="idx">
      <save-attribute-layout
        v-if="id === tab"
        :layout="layouts[idx]"
        @save="handleSaveLayout"
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

const getTabId = (id = "") => `tab-${id}`;
const stripTabId = (tabId: string) => tabId.replace("tab-", "");

const createOpen = ref(false);

const tab = computed({
  get() {
    return getTabId(attributesStore.selectedLayoutId);
  },
  set(tab) {
    attributesStore.selectedLayoutId = stripTabId(tab);
  },
});

const layouts = computed(() => attributesStore.attributeLayouts);

const tabs = computed<SelectOption[]>(() => {
  const tabs = attributesStore.attributeLayouts.map<SelectOption>(
    ({ id, name }) => ({
      id: getTabId(id),
      name,
    })
  );

  if (createOpen.value) {
    tabs.push({ id: getTabId(), name: "New Layout" });
  }

  return tabs;
});

/**
 * Adds a new attribute layout.
 */
function handleAddLayout(): void {
  createOpen.value = true;
  tab.value = getTabId();
}

/**
 * Closes the layout creator on save.
 * @param tabId - The tab id of the saved layout.
 */
function handleSaveLayout(tabId: string): void {
  createOpen.value = false;
  tab.value = tabId;
}
</script>
