<template>
  <flex-box
    :align="smallWindow ? 'start' : 'center'"
    justify="between"
    class="overflow-hidden"
    :column="smallWindow"
    :style="smallWindow ? 'flex-direction: column-reverse' : undefined"
  >
    <flex-box column full-width>
      <typography
        v-if="splitLines"
        variant="caption"
        :value="codePath"
        ellipsis
        :align="props.align"
        :class="codePathClass"
      />
      <typography
        v-if="symbolName"
        variant="caption"
        :value="fileName + symbolFileLines"
        ellipsis
        :align="props.align"
        :class="codePathClass"
      />
      <typography
        :align="props.align"
        :class="splitLines ? 'full-width text-word-break-all' : 'full-width'"
        :el="props.isHeader ? 'h1' : undefined"
        :variant="props.isHeader ? 'subtitle' : undefined"
        :value="symbolName || fileName"
        ellipsis
        color="text"
        :data-cy="props.dataCyName"
      />
      <q-tooltip v-if="props.displayTooltip">
        {{ props.artifact.name }}
      </q-tooltip>
    </flex-box>
    <attribute-chip
      v-if="props.displayType"
      artifact-type
      :value="artifactType"
      :data-cy="props.dataCyType"
    />
  </flex-box>
</template>

<script lang="ts">
/**
 * Displays the name, code path, and type of an artifact.
 */
export default {
  name: "ArtifactNameDisplay",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { ArtifactNameDisplayProps } from "@/types";
import { timStore, useScreen } from "@/hooks";
import { FlexBox, Typography, AttributeChip } from "@/components/common";

const props = defineProps<ArtifactNameDisplayProps>();

const { smallWindow } = useScreen();

const artifactType = computed(() => timStore.getTypeName(props.artifact.type));

const hasCodePath = computed(
  () => props.artifact.name.includes("/") && !props.artifact.name.includes(" ")
);
const hasSymbolName = computed(
  () => props.artifact.name.includes("#") && props.artifact.name.includes("<")
);
const splitLines = computed(() => props.artifact.isCode || hasCodePath.value);

const codePath = computed(() =>
  splitLines.value
    ? props.artifact.name.split("/").slice(0, -1).join("/") + "/"
    : undefined
);

const codePathClass = computed(
  () => "full-width " + (props.dense ? "text-no-wrap" : "text-word-break-all")
);

const fileName = computed(() =>
  splitLines.value
    ? props.artifact.name.split("/").pop()?.split("#")[0]
    : props.artifact.name
);

const symbolName = computed(() =>
  hasSymbolName.value ? props.artifact.name.split("#").pop()?.split("<")[0] : ""
);

const symbolFileLines = computed(() =>
  hasSymbolName.value
    ? `<${props.artifact.name.split("<").pop()?.split(">")[0]}>`
    : ""
);
</script>
