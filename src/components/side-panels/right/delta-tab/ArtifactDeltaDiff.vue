<template>
  <generic-modal
    :title="`Artifact Changes: ${name}`"
    :is-open="isOpen"
    :actions-height="0"
    @close="$emit('close')"
  >
    <template v-slot:body>
      <v-container class="mt-5">
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
      </v-container>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import CodeDiff from "vue-code-diff";
import { Artifact, DeltaType, EntityModification } from "@/types";
import { isArtifact, isModifiedArtifact, splitIntoLines } from "@/util";
import { GenericModal } from "@/components/common";

type InputArtifact = Artifact | EntityModification<Artifact>;

/**
 * Displays artifact delta code diffs.
 *
 * @emits `close` - On close.
 */
export default Vue.extend({
  components: { GenericModal, CodeDiff },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    inputArtifact: {
      type: Object as PropType<InputArtifact>,
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
    artifact(): Artifact | undefined {
      if (isArtifact(this.inputArtifact)) {
        return this.inputArtifact;
      }
      return undefined;
    },
    modification(): EntityModification<Artifact> | undefined {
      if (isModifiedArtifact(this.inputArtifact)) {
        return this.inputArtifact;
      }
      return undefined;
    },
  },
  methods: {
    splitIntoLines(str: string): string {
      return splitIntoLines(str, this.maxWordCount);
    },
  },
});
</script>
