<template>
  <flex-box :full-width="props.fullWidth" class="show-on-hover-parent">
    <slot name="icon" />
    <div :class="props.fullWidth ? 'full-width' : undefined">
      <flex-box :full-width="props.fullWidth" align="center" justify="between">
        <div>
          <slot />
        </div>
        <div v-if="!props.disabled" class="q-ml-sm show-on-hover-child">
          <icon-button small icon="edit" tooltip="Edit" @click="emit('open')" />
          <slot name="actions" />
        </div>
      </flex-box>
      <slot name="body" />
      <q-popup-edit
        v-if="props.editing"
        v-slot="scope"
        :model-value="value"
        @hide="emit('close')"
        @save="(newValue) => emit('save', newValue)"
      >
        <q-input
          v-model="scope.value"
          :autogrow="props.multiline"
          :type="props.multiline ? 'textarea' : undefined"
          dense
          class="full-width"
        >
          <template #append>
            <icon-button small icon="save" tooltip="Save" @click="scope.set" />
          </template>
        </q-input>
      </q-popup-edit>
    </div>
  </flex-box>
</template>

<script lang="ts">
/**
 * A input that pops up over the edited content.
 */
export default {
  name: "PopupEditInput",
};
</script>

<script setup lang="ts">
import { FlexBox, IconButton } from "@/components";

const props = defineProps<{
  value: string;
  disabled?: boolean;
  editing?: boolean | null;
  multiline?: boolean;
  fullWidth?: boolean;
}>();

const emit = defineEmits<{
  /**
   * Called when edit mode is opened.
   */
  (e: "open"): void;
  /**
   * Called when edit mode is closed.
   */
  (e: "close"): void;
  /**
   * Called when the value is saved.
   */
  (e: "save", newValue: string): void;
}>();
</script>
