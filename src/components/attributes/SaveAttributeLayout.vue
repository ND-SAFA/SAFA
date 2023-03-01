<template>
  <div>
    <flex-box v-if="store.isCustom" column b="3">
      <text-input v-model="store.editedLayout.name" label="Name" />
      <artifact-type-input
        v-model="store.editedLayout.artifactTypes"
        multiple
        hint="The layout only appears on these types."
        :error-message="store.typeErrors"
        class="full-width"
      />
    </flex-box>

    <panel-card>
      <attribute-grid editable :layout="store.editedLayout">
        <template #item="{ attribute }">
          <q-card v-if="!!attribute" bordered class="q-pa-md q-ma-sm">
            <flex-box align="center" justify="between">
              <div>
                <typography :value="attribute.label" />
                <br />
                <typography variant="caption" :value="attribute.key" />
              </div>
              <icon-button
                icon="delete"
                tooltip="Remove from layout"
                color="negative"
                @click="handleDeleteAttribute(attribute)"
              />
            </flex-box>
          </q-card>
        </template>
      </attribute-grid>
    </panel-card>

    <flex-box justify="between" b="4">
      <text-button
        v-if="store.isCustom && store.isUpdate"
        text
        label="Delete"
        icon="delete"
        @click="handleDeleteLayout"
      />
      <q-space />
      <text-button
        label="Save"
        :disabled="!store.canSave"
        icon="save"
        @click="handleSave"
      />
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
import { onMounted, ref, watch } from "vue";
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
  TextInput,
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
