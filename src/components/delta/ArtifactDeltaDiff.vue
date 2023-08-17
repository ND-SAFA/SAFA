<template>
  <modal
    :title="`Artifact Changes: ${props.delta.name}`"
    :open="props.open"
    size="lg"
    @close="emit('close')"
  >
    <code-diff
      v-if="deltaType === 'added' && !!artifact"
      :old-string="''"
      :new-string="splitLines(artifact.body)"
      :context="context"
      :output-format="outputFormat"
      :diff-style="diffStyle"
      class="q-my-none"
    />
    <code-diff
      v-else-if="deltaType === 'removed' && !!artifact"
      :old-string="splitLines(artifact.body)"
      :new-string="''"
      :context="context"
      :output-format="outputFormat"
      :diff-style="diffStyle"
      class="q-my-none"
    />
    <code-diff
      v-else-if="deltaType === 'modified' && !!modification"
      :old-string="splitLines(modification.before.body)"
      :new-string="splitLines(modification.after.body)"
      :context="context"
      :output-format="outputFormat"
      :diff-style="diffStyle"
      class="q-my-none"
    />
  </modal>
</template>

<script lang="ts">
/**
 * Displays artifact delta code diffs.
 */
export default {
  name: "ArtifactDeltaDiff",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { CodeDiff } from "v-code-diff";
import { ArtifactDeltaDiffProps } from "@/types";
import { isArtifact, isModifiedArtifact, splitIntoLines } from "@/util";
import { Modal } from "@/components/common";

const props = defineProps<ArtifactDeltaDiffProps>();

const emit = defineEmits<{
  (e: "close"): void;
}>();

const context = 100;
const outputFormat = "line-by-line";
const diffStyle = "word";
const maxWordCount = 15;

const deltaType = computed(() => props.delta.deltaType);

const artifact = computed(() =>
  isArtifact(props.delta.artifact) ? props.delta.artifact : undefined
);
const modification = computed(() =>
  isModifiedArtifact(props.delta.artifact) ? props.delta.artifact : undefined
);

/**
 * Splits a string into separate links.
 * @param str - The strong to split.
 * @return The split string.
 */
function splitLines(str: string): string {
  return splitIntoLines(str, maxWordCount);
}
</script>
