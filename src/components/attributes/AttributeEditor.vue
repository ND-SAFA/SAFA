<template>
  <div class="q-pr-md">
    <flex-box full-width wrap justify="between" align="center" t="1">
      <typography
        variant="subtitle"
        :value="createOpen ? 'Attribute' : 'Attributes'"
      />
      <q-space />
      <text-button
        v-if="!createOpen"
        text
        label="Create"
        icon="add"
        data-cy="button-add-attribute"
        @click="createOpen = true"
      />
      <text-button
        v-else
        text
        label="Cancel"
        icon="cancel"
        @click="createOpen = false"
      />
    </flex-box>
    <save-attribute v-if="createOpen" @save="createOpen = false" />
    <separator v-if="createOpen" />
    <expansion-item
      v-for="attribute in attributes"
      :key="attribute.key"
      :label="attribute.label"
    >
      <template #icon>
        <span @click.stop>
          <icon-button
            class="ml-auto"
            icon="add"
            tooltip="Add to layout"
            :disabled="isAttributeInLayout(attribute)"
            data-cy="button-add-attribute-to-layout"
            @click="handleAddToLayout(attribute)"
          />
        </span>
      </template>
      <save-attribute :attribute="attribute" />
      <separator class="faded" />
    </expansion-item>
    <flex-box v-if="attributes.length === 0" justify="center">
      <typography
        variant="caption"
        value="You have not yet created any custom attributes."
      />
    </flex-box>
  </div>
</template>

<script lang="ts">
/**
 * Renders the list of project attributes and allows for editing them.
 */
export default {
  name: "AttributeEditor",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { AttributePositionSchema, AttributeSchema } from "@/types";
import { attributeLayoutSaveStore, attributesStore } from "@/hooks";
import {
  FlexBox,
  TextButton,
  Typography,
  IconButton,
  Separator,
  ExpansionItem,
} from "@/components/common";
import SaveAttribute from "./SaveAttribute.vue";

const createOpen = ref(false);

const attributes = computed(() => attributesStore.attributes);

const layoutStore = computed(() =>
  attributeLayoutSaveStore(attributesStore.selectedLayoutId)
);

/**
 * @return Whether this attribute is in the current layout.
 */
function isAttributeInLayout(attribute: AttributeSchema): boolean {
  return !!layoutStore.value.editedLayout.positions.find(
    ({ key }: AttributePositionSchema) => key === attribute.key
  );
}

/**
 * Adds an attribute to the current layout.
 * @param attribute - The attribute to add.
 */
function handleAddToLayout(attribute: AttributeSchema): void {
  layoutStore.value.addAttribute(attribute.key);
}
</script>
