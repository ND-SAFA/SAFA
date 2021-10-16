<template>
  <GenericModal
    :title="`Artifact Changes: ${name}`"
    :isOpen="isOpen"
    @onClose="$emit('onClose')"
    :actionsHeight="0"
  >
    <template v-slot:body>
      <v-container class="mt-5">
        <code-diff
          v-if="deltaType === 'added'"
          :old-string="''"
          :new-string="splitIntoLines(artifact.after)"
          :context="context"
          :output-format="outputFormat"
          :diff-style="diffStyle"
        />
        <code-diff
          v-else-if="deltaType === 'removed'"
          :old-string="splitIntoLines(artifact.before)"
          :new-string="''"
          :context="context"
          :output-format="outputFormat"
          :diff-style="diffStyle"
        />
        <code-diff
          v-else-if="deltaType === 'modified'"
          :old-string="splitIntoLines(artifact.before)"
          :new-string="splitIntoLines(artifact.after)"
          :context="context"
          :output-format="outputFormat"
          :diff-style="diffStyle"
        />
      </v-container>
    </template>
  </GenericModal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import GenericModal from "@/components/common/modals/GenericModal.vue";
import CodeDiff from "vue-code-diff";
import { DeltaArtifact, DeltaType, getDeltaType } from "@/types/domain/delta";
import { splitIntoLines } from "@/util/string-helper";

export default Vue.extend({
  components: { GenericModal, CodeDiff },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    artifact: {
      type: Object as PropType<DeltaArtifact>,
      required: true,
    },
    name: {
      type: String,
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
    deltaType(): DeltaType {
      return getDeltaType(this.artifact);
    },
  },
  methods: {
    splitIntoLines(str: string): string {
      return splitIntoLines(str, this.maxWordCount);
    },
  },
});
</script>
