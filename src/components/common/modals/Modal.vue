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
            icon="cancel"
            data-cy="button-close"
            @click="emit('close')"
          />
        </flex-box>
        <separator />
        <q-linear-progress v-if="!!props.loading" indeterminate />
      </q-card-section>
      <q-card-section>
        <slot />
      </q-card-section>
      <q-card-actions v-if="!!slots.actions" align="right">
        <separator />
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
import { useSlots } from "vue";
import { Typography, Separator } from "@/components/common/display";
import { IconButton } from "@/components/common/button";
import { FlexBox } from "@/components/common/layout";

const props = defineProps<{
  /**
   * The modal title.
   */
  title: string;
  /**
   * Whether the modal is open.
   */
  isOpen: boolean;
  /**
   * Whether the component is loading.
   */
  loading?: string;
  /**
   * The testing selector to set.
   */
  dataCy?: string;
}>();

const emit = defineEmits<{
  /**
   * Called when closed.
   */
  (e: "close"): void;
}>();

const slots = useSlots();
</script>
