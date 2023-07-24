<template>
  <chip
    v-if="!props.confidenceScore"
    :class="chipClassName"
    :outlined="enumerated"
    :color="displayColor"
    :removable="props.removable"
    :data-cy="props.dataCy"
    :dense="props.dense"
    @remove="emit('remove')"
  >
    <q-tooltip :hidden="text.length < 15">
      {{ text }}
    </q-tooltip>
    <icon
      v-if="iconVisible"
      :id="iconId"
      :variant="props.icon"
      :color="iconColor"
      :size="props.dense ? 'xs' : 'sm'"
    />
    <typography
      ellipsis
      :color="enumerated ? displayColor : 'text'"
      :small="text.length >= 15"
      :l="iconVisible ? '1' : ''"
      :value="text"
    />
  </chip>
  <flex-box v-else align="center" class="attribute-bar">
    <q-linear-progress
      rounded
      :value="progress / 100"
      :color="displayColor"
      :track-color="trackColor"
      size="20px"
    />
    <typography l="2" :value="progress + '%'" class="attribute-bar-text" />
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
import { AttributeChipProps } from "@/types";
import {
  camelcaseToDisplay,
  getEnumColor,
  getScoreColor,
  uppercaseToDisplay,
} from "@/util";
import { typeOptionsStore } from "@/hooks";
import { FlexBox, Typography } from "../content";
import { Icon } from "../icon";
import Chip from "./Chip.vue";

const props = defineProps<AttributeChipProps>();

const emit = defineEmits<{
  /**
   * When the remove button is clicked.
   */
  (e: "remove"): void;
}>();

const enumerated = computed(() => props.approvalType || props.deltaType);

const text = computed(() => {
  if (props.confidenceScore) {
    return String(props.value).slice(0, 4);
  } else if (enumerated.value) {
    return uppercaseToDisplay(String(props.value) || "");
  } else if (props.format) {
    return camelcaseToDisplay(String(props.value) || "");
  } else if (props.artifactType) {
    return typeOptionsStore.getArtifactTypeDisplay(String(props.value));
  } else {
    return String(props.value);
  }
});

const progress = computed(() =>
  Math.min(Math.ceil(parseFloat(String(text.value)) * 100), 100)
);

const iconId = computed(() =>
  props.artifactType
    ? typeOptionsStore.getArtifactTypeIcon(String(props.value))
    : ""
);

const typeColor = computed(() =>
  props.artifactType
    ? typeOptionsStore.tim.artifacts[props.value]?.color || "primary"
    : "primary"
);

const iconVisible = computed(() => iconId.value || props.icon);

const displayColor = computed(() => {
  if (props.color) {
    return props.color;
  } else if (props.confidenceScore) {
    return getScoreColor(props.value);
  } else if (props.artifactType) {
    return typeColor.value;
  } else if (enumerated.value) {
    return getEnumColor(String(props.value));
  } else {
    return "";
  }
});

const iconColor = computed(() => {
  if (props.artifactType) {
    return typeColor.value;
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
  enumerated.value
    ? "q-mr-sm bg-neutral attribute-chip"
    : "qmr-sm bd-primary bg-neutral attribute-chip"
);
</script>
