<template>
  <v-tooltip
    v-if="!confidenceScore"
    bottom
    z-index="12"
    :disabled="text.length < 10"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-chip
        v-on="on"
        v-bind="attrs"
        small
        style="max-width: 200px"
        class="mr-1"
        :outlined="outlined"
        :color="color"
        :data-cy="dataCy"
      >
        <v-icon v-if="iconId" small>{{ iconId }}</v-icon>
        <typography
          ellipsis
          inherit-color
          :l="iconId ? '1' : '0'"
          :value="text"
        />
      </v-chip>
    </template>
    <span>{{ text }}</span>
  </v-tooltip>
  <flex-box v-else align="center">
    <v-progress-linear :value="progress" :color="color" height="20" rounded />
    <typography l="2" :value="progress + '%'" style="width: 50px" />
  </flex-box>
</template>

<script lang="ts">
import Vue from "vue";
import { ApprovalType } from "@/types";
import {
  camelcaseToDisplay,
  getBackgroundColor,
  getScoreColor,
  uppercaseToDisplay,
} from "@/util";
import { typeOptionsStore } from "@/hooks";
import FlexBox from "@/components/common/display/FlexBox.vue";
import Typography from "./Typography.vue";

/**
 * Displays a generic chip that can render specific attributes.
 */
export default Vue.extend({
  name: "AttributeChip",
  components: { FlexBox, Typography },
  props: {
    value: String,
    format: Boolean,
    icon: String,
    artifactType: Boolean,
    confidenceScore: Boolean,
    dataCy: String,
  },
  computed: {
    /**
     * @return Whether the value of this chip is enumerated.
     */
    enumerated(): boolean {
      return this.value in ApprovalType;
    },
    /**
     * @return The text of the chip.
     */
    text(): string {
      if (this.confidenceScore) {
        return this.value.slice(0, 4);
      } else if (this.enumerated || this.value === this.value?.toUpperCase()) {
        return uppercaseToDisplay(this.value || "");
      } else if (this.format) {
        return camelcaseToDisplay(this.value || "");
      } else if (this.artifactType) {
        return typeOptionsStore.getArtifactTypeDisplay(this.value || "");
      } else {
        return this.value || "";
      }
    },
    /**
     * @return The icon to display on this chip.
     */
    iconId(): string {
      return this.artifactType
        ? typeOptionsStore.getArtifactTypeIcon(this.value || "")
        : this.icon;
    },
    /**
     * @return The color to display for this chip.
     */
    color(): string {
      if (this.confidenceScore) {
        return getScoreColor(this.value || "");
      } else {
        return getBackgroundColor(this.value || "");
      }
    },
    /**
     * @return Whether the chip is outlined.
     */
    outlined(): boolean {
      return this.enumerated || this.confidenceScore;
    },
    /**
     * @return Thee current progress %.
     */
    progress(): number {
      return Math.min(Math.ceil(parseFloat(this.text) * 100), 100);
    },
  },
});
</script>

<style scoped></style>
