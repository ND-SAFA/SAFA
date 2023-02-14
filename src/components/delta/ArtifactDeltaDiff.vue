<template>
  <modal
    :title="`Artifact Changes: ${name}`"
    :is-open="isOpen"
    :actions-height="0"
    size="l"
    @close="$emit('close')"
  >
    <template #body>
      <div class="mt-5">
        <code-diff
          v-if="deltaType === 'added'"
          :old-string="''"
          :new-string="splitIntoLines(artifact.body)"
          :context="context"
          :output-format="outputFormat"
          :diff-style="diffStyle"
        />
        <code-diff
          v-else-if="deltaType === 'removed'"
          :old-string="splitIntoLines(artifact.body)"
          :new-string="''"
          :context="context"
          :output-format="outputFormat"
          :diff-style="diffStyle"
        />
        <code-diff
          v-else-if="deltaType === 'modified' && modification !== undefined"
          :old-string="splitIntoLines(modification.before.body)"
          :new-string="splitIntoLines(modification.after.body)"
          :context="context"
          :output-format="outputFormat"
          :diff-style="diffStyle"
        />
      </div>
    </template>
  </modal>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import CodeDiff from "vue-code-diff";
import {
  ArtifactSchema,
  DeltaArtifact,
  DeltaType,
  EntityModification,
} from "@/types";
import { isArtifact, isModifiedArtifact, splitIntoLines } from "@/util";
import { Modal } from "@/components/common";

/**
 * Displays artifact delta code diffs.
 *
 * @emits `close` - On close.
 */
export default defineComponent({
  name: "ArtifactDeltaDiff",
  components: { Modal, CodeDiff },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    inputArtifact: {
      type: Object as PropType<DeltaArtifact>,
      required: true,
    },
    name: {
      type: String,
      required: true,
    },
    deltaType: {
      type: String as PropType<DeltaType>,
      required: true,
    },
  },
  data() {
    return {
      context: 100,
      outputFormat: "line-by-line",
      diffStyle: "word",
      maxWordCount: 15,
    };
  },
  computed: {
    /**
     * Returns the current artifact.
     */
    artifact(): DeltaArtifact | undefined {
      return isArtifact(this.inputArtifact) ? this.inputArtifact : undefined;
    },
    /**
     * Returns the current modified artifact.
     */
    modification(): EntityModification<ArtifactSchema> | undefined {
      return isModifiedArtifact(this.inputArtifact)
        ? this.inputArtifact
        : undefined;
    },
  },
  methods: {
    /**
     * Splits a string into separate links.
     * @param str - The strong to split.
     * @return The split string.
     */
    splitIntoLines(str: string): string {
      return splitIntoLines(str, this.maxWordCount);
    },
  },
});
</script>
