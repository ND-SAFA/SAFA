<template>
  <div class="q-mb-md">
    <q-card flat :class="className">
      <flex-box align="center">
        <icon v-if="!!props.icon" :variant="icon" class="q-mr-sm" size="lg" />
        <typography
          v-if="!!props.title"
          variant="subtitle"
          el="h2"
          :value="props.title"
          :color="props.color"
        />
      </flex-box>
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
import { IconVariant, ThemeColor } from "@/types";
import { Typography, Icon, Separator } from "@/components/common/display";
import FlexBox from "@/components/common/layout/FlexBox.vue";

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
    /**
     * An icon to display before the title.
     */
    icon?: IconVariant;
  }>(),
  {
    color: "primary",
    title: undefined,
    icon: undefined,
  }
);

const slots = useSlots();

const className = computed(
  () => `q-pa-md overflow-hidden bg-neutral bd-${props.color}`
);
</script>
