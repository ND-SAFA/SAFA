<template>
  <flex-box full-width class="show-on-hover-parent">
    <slot name="icon" />
    <div class="full-width">
      <div style="min-height: 30px">
        <slot />
        <div v-if="!props.disabled" class="float-right show-on-hover-child">
          <icon-button small icon="edit" tooltip="Edit" @click="emit('open')" />
          <slot name="actions" />
        </div>
      </div>
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
