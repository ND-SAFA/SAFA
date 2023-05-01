<template>
  <private-page full-window>
    <flex-box full-width justify="center" t="10">
      <panel-card>
        <flex-box>
          <q-select
            v-model="mode"
            outlined
            label="Search Mode"
            :options="modes"
            class="nav-search-mode"
            style="min-width: 150px"
          />
          <q-select
            v-model="prompt"
            outlined
            use-input
            clearable
            :label="placeholder"
            class="nav-search-prompt"
            style="min-width: 600px"
          >
            <template #append>
              <icon variant="search" />
            </template>
            <template #before-options> </template>
            <template #no-option>
              <flex-box column y="2" x="2">
                <flex-box full-width>
                  <q-select
                    v-model="searchTypes"
                    outlined
                    label="Search Artifact Types"
                    hint="What types am I generating relationships to."
                    class="full-width"
                    style="min-width: 250px"
                  />
                  <q-input
                    v-model="maxResults"
                    outlined
                    type="number"
                    label="Max Results"
                    class="q-ml-sm"
                    style="min-width: 100px; width: 100px"
                  />
                </flex-box>
                <q-select
                  v-model="relateTypes"
                  outlined
                  label="Include Artifact Types"
                  hint="What types do I want to see related to my search."
                  class="full-width q-my-md"
                  style="min-width: 250px"
                />
                <flex-box full-width justify="end">
                  <q-btn color="primary"> Search </q-btn>
                </flex-box>
              </flex-box>
            </template>
          </q-select>
        </flex-box>
      </panel-card>
    </flex-box>
  </private-page>
</template>

<script lang="ts">
/**
 * Displays the project search page.
 */
export default {
  name: "SearchView",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { PrivatePage, FlexBox, PanelCard, Icon } from "@/components";

type Mode = "Prompt" | "Artifact" | "Artifact Type";

const modes: Mode[] = ["Prompt", "Artifact", "Artifact Type"];

const mode = ref<Mode>("Prompt");
const prompt = ref<string>("");
const searchTypes = ref<string[]>([]);
const maxResults = ref<number>(5);
const relateTypes = ref<string[]>([]);

const placeholder = computed(
  () =>
    ({
      Prompt: "Enter a prompt...",
      Artifact: "Search artifacts...",
      "Artifact Type": "Search artifact types...",
    }[mode.value])
);
</script>

<style lang="scss">
.nav-search-mode {
  & > .q-field__inner > .q-field__control {
    border-bottom-right-radius: 0;
    border-top-right-radius: 0;

    &:before {
      border-right: none;
    }
  }
}

.nav-search-prompt {
  & > .q-field__inner > .q-field__control {
    border-bottom-left-radius: 0;
    border-top-left-radius: 0;
  }
}
</style>
