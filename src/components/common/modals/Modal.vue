<template>
  <q-dialog
    :model-value="props.open"
    :data-cy="props.dataCy"
    @close="emit('close')"
  >
    <q-card :class="className">
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
        <typography
          v-if="!!props.subtitle"
          t="2"
          b=""
          el="p"
          :value="props.subtitle"
        />
      </q-card-section>
      <q-card-section v-if="!!slots.default">
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
import { computed, useSlots } from "vue";
import { Typography, Separator, FlexBox } from "@/components/common/display";
import { IconButton } from "@/components/common/button";

const props = defineProps<{
  /**
   * The modal title.
   */
  title: string;
  /**
   * The modal subtitle.
   */
  subtitle?: string;
  /**
   * Whether the modal is open.
   */
  open: boolean;
  /**
   * Whether the component is loading.
   */
  loading?: boolean;
  /**
   * A fixed width size to set for the modal.
   */
  size?: "sm" | "md" | "lg";
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

const className = computed(() => `modal-${props.size}`);
</script>
