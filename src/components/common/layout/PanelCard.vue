<template>
  <div class="q-mb-md">
    <q-card flat :class="className">
      <typography
        v-if="!!props.title"
        variant="subtitle"
        el="h2"
        :value="props.title"
        :color="props.color"
      />
      <separator v-if="!!props.title" b="2" />
      <slot />
      <q-card-actions v-if="!!slots.actions">
        <slot name="actions" />
      </q-card-actions>
    </q-card>
  </div>
</template>

<script lang="ts">
/**
 * Displays a card that contains panel content.
 */
export default {
  name: "PanelCard",
};
</script>

<script setup lang="ts">
import { computed, useSlots, withDefaults } from "vue";
import { ThemeColor } from "@/types";
import Separator from "@/components/common/display/Separator.vue";
import Typography from "@/components/common/display/Typography.vue";

const props = withDefaults(
  defineProps<{
    /**
     * The color for the card border.
     */
    color?: ThemeColor;
    /**
     * A title to render on the card.
     */
    title?: string;
  }>(),
  {
    color: "primary",
    title: undefined,
  }
);

const slots = useSlots();

const className = computed(
  () => `q-pa-md overflow-hidden bg-neutral bd-${props.color}`
);
</script>
