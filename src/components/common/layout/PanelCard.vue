<template>
  <div :class="containerClassName">
    <q-card flat :class="className">
      <flex-box align="center" justify="between">
        <flex-box align="center">
          <icon
            v-if="!!props.icon"
            :variant="props.icon"
            class="q-mr-sm"
            size="lg"
          />
          <typography
            v-if="!!props.title"
            variant="subtitle"
            el="h2"
            :value="props.title"
            :color="props.color"
          />
        </flex-box>
        <slot name="title-actions" />
      </flex-box>
      <separator v-if="!!props.title" b="2" />
      <typography
        v-if="!!props.subtitle"
        el="p"
        b="4"
        :value="props.subtitle"
      />
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
     * A subtitle title to render on the card.
     */
    subtitle?: string;
    /**
     * An icon to display before the title.
     */
    icon?: IconVariant;
    /**
     * The panel's classes.
     */
    class?: string;
    /**
     * The panel's container's classes.
     */
    containerClass?: string;
  }>(),
  {
    color: "primary",
    title: undefined,
    subtitle: undefined,
    icon: undefined,
    class: "",
    containerClass: "",
  }
);

const slots = useSlots();

const className = computed(
  () => `q-pa-md overflow-hidden bg-neutral bd-${props.color} ${props.class}`
);

const containerClassName = computed(() => `q-mb-md ${props.containerClass}`);
</script>
