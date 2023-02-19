<template>
  <q-dialog :model-value="props.isOpen" @close="emit('close')">
    <q-card>
      <q-card-section>
        <flex-box
          full-width
          justify="between"
          align="center"
          data-cy="modal-title"
        >
          <typography :value="props.title" />
          <icon-button
            tooltip="Close"
            icon-variant="cancel"
            data-cy="button-close"
            @click="$emit('close')"
          />
        </flex-box>
        <q-separator />
        <q-linear-progress v-if="props.isLoading" indeterminate />
      </q-card-section>
      <q-card-section>
        <slot />
      </q-card-section>
      <q-card-actions v-if="props.actions" align="right">
        <q-separator />
        <slot name="actions" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script lang="ts">
/**
 * Displays a generic modal.
 */
export default {
  name: "Modal",
};
</script>

<script setup lang="ts">
import { Typography } from "@/components/common/display";
import { IconButton } from "@/components/common/button";
import { FlexBox } from "@/components/common/layout";

const props = defineProps<{
  title: string;
  isOpen: boolean;
  isLoading?: boolean;
  dataCy?: string;
  actions?: boolean;
}>();

const emit = defineEmits<{
  (e: "close"): void;
}>();
</script>
