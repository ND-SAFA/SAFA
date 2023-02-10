<template>
  <div>
    <v-row v-if="store.isCustom" dense>
      <v-col cols="6">
        <v-text-field v-model="store.editedLayout.name" filled label="Name"
      /></v-col>
      <v-col cols="6">
        <artifact-type-input
          v-model="store.editedLayout.artifactTypes"
          multiple
          persistent-hint
          hint="The layout will only appear on these artifact types."
          :error-messages="store.typeErrors"
      /></v-col>
    </v-row>

    <panel-card>
      <attribute-grid editable :layout="store.editedLayout">
        <template #item="{ attribute }">
          <v-card v-if="!!attribute" outlined class="pa-3 mx-2">
            <flex-box align="center" justify="space-between">
              <div>
                <typography :value="attribute.label" />
                <br />
                <typography variant="caption" :value="attribute.key" />
              </div>
              <icon-button
                icon-id="mdi-delete"
                tooltip="Remove from layout"
                color="error"
                @click="handleDeleteAttribute(attribute)"
              />
            </flex-box>
          </v-card>
        </template>
      </attribute-grid>
    </panel-card>

    <flex-box justify="space-between" b="4">
      <text-button
        v-if="store.isCustom && store.isUpdate"
        text
        variant="delete"
        @click="handleDeleteLayout"
      >
        Delete
      </text-button>
      <v-spacer />
      <text-button
        :disabled="!store.canSave"
        variant="save"
        @click="handleSave"
      >
        Save
      </text-button>
    </flex-box>
  </div>
</template>

<script lang="ts">
/**
 * Allows for editing attribute layouts.
 */
export default {
  name: "SaveAttributeLayout",
};
</script>

<script setup lang="ts">
import { onMounted, ref, watch, defineProps, defineEmits } from "vue";
import { AttributeSchema, AttributeLayoutSchema } from "@/types";
import { attributeLayoutSaveStore } from "@/hooks";
import { handleDeleteAttributeLayout, handleSaveAttributeLayout } from "@/api";
import {
  AttributeGrid,
  ArtifactTypeInput,
  FlexBox,
  PanelCard,
  Typography,
  IconButton,
  TextButton,
} from "@/components/common";

const props = defineProps<{
  layout?: AttributeLayoutSchema;
}>();

const emit = defineEmits<{
  (e: "save"): void;
}>();

const store = ref(attributeLayoutSaveStore(props.layout?.id || ""));

/**
 * Saves an attribute layout.
 */
function handleSave() {
  handleSaveAttributeLayout(store.value.editedLayout, store.value.isUpdate, {
    onSuccess: () => emit("save"),
  });
}

/**
 * Deletes an attribute layout.
 */
function handleDeleteLayout() {
  handleDeleteAttributeLayout(store.value.editedLayout, {});
}

/**
 * Deletes an attribute from the layout.
 */
function handleDeleteAttribute(attribute: AttributeSchema) {
  store.value.deleteAttribute(attribute);
}

onMounted(() => store.value.resetLayout(props.layout));

watch(
  () => props.layout,
  () => store.value.resetLayout(props.layout)
);
</script>
