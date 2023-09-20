<template>
  <safa-icon v-if="props.variant === 'safa'" icon-only />
  <q-icon
    v-else
    :color="iconColor"
    :size="props.size"
    :style="iconStyle"
    :name="iconId"
    :data-cy="`icon-${props.variant}`"
  />
</template>

<script lang="ts">
/**
 * Icon
 */
export default {
  name: "Icon",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { IconDisplayProps } from "@/types";
import { getIcon } from "@/util";
import SafaIcon from "@/components/common/display/icon/SafaIcon.vue";

const props = defineProps<IconDisplayProps>();

const iconId = computed(() => {
  if (props.id) {
    return props.id;
  }

  return getIcon(props.variant);
});

const iconColor = computed(() => {
  if (props.color?.includes("#")) {
    return "";
  } else if (props.color) {
    return props.color;
  }

  switch (props.variant) {
    case "home-list":
    case "home-add":
    case "trace-approve":
      return "primary";
    case "warning":
      return "secondary";
    case "error":
    case "trace-decline":
    case "trace-decline-all":
      return "negative";
    default:
      return "";
  }
});

const iconStyle = computed(() => {
  if (props.style) {
    return props.style;
  } else if (props.rotate) {
    return `transform: rotate(${props.rotate}deg)`;
  } else if (props.color?.includes("#")) {
    return `color: ${props.color}`;
  } else {
    return "";
  }
});
</script>
