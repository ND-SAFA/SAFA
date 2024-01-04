<template>
  <div>
    <project-overview-display hide-overflow />
    <q-carousel
      v-model="artifactId"
      transition-prev="slide-right"
      transition-next="slide-left"
      swipeable
      animated
      navigation
      padding
      arrows
      height="600px"
      navigation-position="top"
      control-color="primary"
    >
      <q-carousel-slide
        v-for="artifact in artifacts"
        :key="artifact.id"
        :name="artifact.id"
      >
        <div class="width-fit q-mx-auto q-mt-sm">
          <panel-card>
            <artifact-body-display
              display-title
              default-expanded
              display-divider
              :artifact="artifact"
            />
          </panel-card>
        </div>
      </q-carousel-slide>
    </q-carousel>
  </div>
</template>

<script lang="ts">
/**
 * Previews a project after it has been uploaded.
 */
export default {
  name: "ProjectPreview",
};
</script>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { artifactStore } from "@/hooks";
import { ProjectOverviewDisplay } from "@/components/project";
import { PanelCard } from "@/components/common";
import { ArtifactBodyDisplay } from "@/components/artifact";

const artifacts = computed(() => artifactStore.allArtifacts);

const artifactId = ref(artifacts.value[0]?.id);

watch(
  artifacts,
  (newArtifacts) => {
    artifactId.value = newArtifacts[0]?.id;
  },
  { immediate: true }
);
</script>
