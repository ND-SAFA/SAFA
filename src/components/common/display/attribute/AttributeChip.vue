<template>
  <q-chip
    v-if="!props.confidenceScore"
    :class="chipClassName"
    :outline="enumerated"
    :color="displayColor"
    :data-cy="props.dataCy"
    style="max-width: 200px"
    class="bg-white"
  >
    <q-tooltip :hidden="text.length < 10">
      {{ text }}
    </q-tooltip>
    <icon
      v-if="iconVisible"
      :id="iconId"
      :variant="props.icon"
      :color="iconColor"
      size="sm"
    />
    <typography
      ellipsis
      inherit-color
      :l="iconVisible ? '1' : ''"
      :value="text"
    />
  </q-chip>
  <flex-box v-else align="center">
    <q-linear-progress
      rounded
      :value="props.value"
      :color="displayColor"
      :track-color="trackColor"
      size="20px"
    />
    <typography l="2" :value="progress + '%'" style="width: 50px" />
  </flex-box>
</template>

<script lang="ts">
/**
 * Displays a generic chip that can render specific attributes.
 */
export default {
  name: "AttributeChip",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { ApprovalType, IconVariant, ThemeColor } from "@/types";
import {
  camelcaseToDisplay,
  getApprovalColor,
  getScoreColor,
  uppercaseToDisplay,
} from "@/util";
import { typeOptionsStore } from "@/hooks";
import { FlexBox } from "@/components/common/layout";
import Icon from "@/components/common/display/icon/Icon.vue";
import Typography from "../Typography.vue";

const props = defineProps<{
  /**
   * The chip text.
   */
  value: string;
  /**
   * If true, the chip text will be converted from "camelCase" to "Display Case".
   */
  format?: boolean;
  /**
   * Whether this chip is for an artifact type, customizing the display and icon.
   */
  artifactType?: boolean;
  /**
   * Whether to render a confidence score instead of a chip.
   */
  confidenceScore?: boolean;
  /**
   * The type of icon to render.
   */
  icon?: IconVariant;
  /**
   * The color to render the component with.
   */
  color?: ThemeColor;
  /**
   * The testing selector to set.
   */
  dataCy?: string;
}>();

const enumerated = computed(() => props.value in ApprovalType);

const text = computed(() => {
  if (props.confidenceScore) {
    return String(props.value).slice(0, 4);
  } else if (enumerated.value || props.value === props.value?.toUpperCase()) {
    return uppercaseToDisplay(props.value || "");
  } else if (props.format) {
    return camelcaseToDisplay(props.value || "");
  } else if (props.artifactType) {
    return typeOptionsStore.getArtifactTypeDisplay(props.value);
  } else {
    return props.value;
  }
});

const progress = computed(() =>
  Math.min(Math.ceil(parseFloat(text.value) * 100), 100)
);

const iconId = computed(() =>
  props.artifactType ? typeOptionsStore.getArtifactTypeIcon(props.value) : ""
);

const iconVisible = computed(() => iconId.value || props.icon);

const displayColor = computed(() => {
  if (props.color) {
    return props.color;
  } else if (props.confidenceScore) {
    return getScoreColor(props.value);
  } else if (enumerated.value) {
    return getApprovalColor(props.value);
  } else {
    return "";
  }
});

const iconColor = computed(() => {
  if (props.artifactType) {
    return "primary";
  } else {
    return displayColor.value;
  }
});

const trackColor = computed(() => {
  switch (displayColor.value) {
    case "positive":
      return "green-3";
    case "secondary":
      return "amber-4";
    case "negative":
      return "red-3";
    default:
      return "";
  }
});

const chipClassName = computed(() =>
  enumerated.value ? "q-mr-sm" : "qmr-sm bd-primary bg-neutral"
);
</script>
