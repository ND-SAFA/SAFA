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
      v-if="iconId || props.iconVariant"
      :id="iconId"
      :variant="props.iconVariant"
      size="sm"
      :color="props.artifactType ? 'primary' : ''"
    />
    <typography ellipsis inherit-color :l="iconId ? '1' : '0'" :value="text" />
  </q-chip>
  <flex-box v-else align="center">
    <q-linear-progress
      rounded
      :value="progress"
      :color="displayColor"
      size="md"
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
import { computed, defineProps } from "vue";
import { ApprovalType, IconVariant } from "@/types";
import {
  camelcaseToDisplay,
  getBackgroundColor,
  getScoreColor,
  uppercaseToDisplay,
} from "@/util";
import { typeOptionsStore, useTheme } from "@/hooks";
import { FlexBox } from "@/components/common/layout";
import Icon from "@/components/common/display/icon/Icon.vue";
import Typography from "../Typography.vue";

const props = defineProps<{
  value: string;
  format?: boolean;
  icon?: string;
  iconVariant?: IconVariant;
  artifactType?: boolean;
  confidenceScore?: boolean;
  dataCy?: string;
  color?: string;
}>();

const { darkMode } = useTheme();

const enumerated = computed(() => props.value in ApprovalType);

const text = computed(() => {
  if (props.confidenceScore) {
    return props.value.slice(0, 4);
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
  props.artifactType
    ? typeOptionsStore.getArtifactTypeIcon(props.value)
    : props.icon || ""
);

const displayColor = computed(() => {
  if (props.color) {
    return props.color;
  } else if (props.confidenceScore) {
    return getScoreColor(props.value);
  } else if (enumerated.value) {
    return getBackgroundColor(props.value, darkMode.value);
  } else {
    return "";
  }
});

const chipClassName = computed(() =>
  enumerated.value ? "q-mr-sm" : "qmr-sm bd-primary bg-neutral"
);
</script>
