<template>
  <v-expansion-panel>
    <v-expansion-panel-header>
      <v-container>
        <v-row>
          <v-col cols="1" align-self="center">
            <v-icon :color="iconColor">{{ iconName }}</v-icon>
          </v-col>
          <v-col cols="11" align-self="center">
            <h3>{{ artifactFile.type }}</h3>
          </v-col>
        </v-row>
      </v-container>
    </v-expansion-panel-header>
    <v-expansion-panel-content>
      <v-container>
        <v-row><h4>File(s):</h4> </v-row>
        <v-row>
          <FileSelector
            :multiple="false"
            @onChangeFiles="onChangeFiles"
            @onClear="$emit('onClearFile')"
          />
        </v-row>
        <v-row v-if="!hasArtifactFile" justify="center" style="color: red">
          <label class="text-caption">Missing artifact file</label>
        </v-row>

        <v-row class="mt-5 mb-5">
          <v-divider />
        </v-row>

        <v-row> <h4>Traces:</h4> </v-row>

        <v-row>
          <v-expansion-panels>
            <v-expansion-panel
              v-for="traceFile in traceFiles"
              :key="`${traceFile.source}-${traceFile.target}`"
            >
              <v-expansion-panel-header>
                <v-row>
                  <v-col cols="1" align-self="center">
                    <v-icon :color="getTraceIconColor(traceFile)">
                      {{ getTraceIconName(traceFile) }}</v-icon
                    >
                  </v-col>
                  <v-col cols="10">
                    <label :class="getSourceClass(artifactFile, traceFile)">
                      {{ traceFile.source }}
                    </label>
                    <v-icon>mdi-arrow-right</v-icon>
                    <label :class="getTargetClass(artifactFile, traceFile)">
                      {{ traceFile.target }}
                    </label>
                  </v-col>
                </v-row>
              </v-expansion-panel-header>
              <v-expansion-panel-content>
                <v-row>
                  <v-col cols="9" align-self="center"> Generate Links: </v-col>
                  <v-col cols="3" align-self="center">
                    <v-switch v-model="traceFile.isGenerated" />
                  </v-col>
                </v-row>
                <v-row v-if="!traceFile.isGenerated">
                  <v-col>
                    <v-row>
                      <FileSelector
                        :multiple="false"
                        @onChangeFiles="onChangeTraceFiles(traceFile, $event)"
                      />
                    </v-row>
                    <v-row
                      v-if="!isValidTraceFile(traceFile)"
                      justify="center"
                      style="color: red"
                    >
                      Missing trace file
                    </v-row>
                  </v-col>
                </v-row>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-row>
        <v-row justify="center" class="mt-5">
          <ButtonRow
            :definitions="[createAddTracePathButtonDefinition(artifactFile)]"
          />
        </v-row>

        <v-row class="mt-5 mb-5">
          <v-divider />
        </v-row>

        <v-row class="mt-5 mb-5" justify="center">
          <v-btn
            @click="$emit('onDelete')"
            text
            small
            color="error"
            class="pa-2 ma-2"
          >
            Delete
          </v-btn>
        </v-row>
      </v-container>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import {
  ArtifactFile,
  TraceFile,
  ButtonDefinition,
  ButtonType,
} from "@/types/common-components";
import ButtonRow from "@/components/common/ButtonRow.vue";
import FileSelector from "@/components/common/FileSelector.vue";

const DEFAULT_IS_GENERATED = true;

export default Vue.extend({
  components: {
    ButtonRow,
    FileSelector,
  },
  props: {
    artifactFile: {
      type: Object as PropType<ArtifactFile>,
      required: true,
    },
    traceFiles: {
      type: Array as PropType<TraceFile[]>,
      required: true,
    },
    menuLabels: {
      type: Array as PropType<string[]>,
      required: true,
    },
  },
  computed: {
    isValid(): boolean {
      return this.hasArtifactFile && this.hasTraceFiles;
    },
    hasArtifactFile(): boolean {
      return this.artifactFile.file !== undefined;
    },
    hasTraceFiles(): boolean {
      return (
        this.traceFiles.filter((f) => !this.isValidTraceFile(f)).length === 0
      );
    },
    iconName(): string {
      return this.isValid ? "mdi-check" : "mdi-close";
    },
    iconColor(): string {
      return this.isValid ? "success" : "error";
    },
  },
  methods: {
    isValidTraceFile(traceFile: TraceFile): boolean {
      return traceFile.file !== undefined || traceFile.isGenerated;
    },
    getTraceIconName(traceFile: TraceFile): string {
      return this.isValidTraceFile(traceFile) ? "mdi-check" : "mdi-close";
    },
    getTraceIconColor(traceFile: TraceFile): string {
      return this.isValidTraceFile(traceFile) ? "success" : "error";
    },
    onChangeFiles(file: File): void {
      if (file === null) {
        this.$emit("onClearFile");
      } else {
        this.$emit("onAddFile", file);
      }
    },
    onChangeTraceFiles(traceFile: TraceFile, file: File): void {
      if (file === null) {
        this.$emit("onClearTraceFile", { ...traceFile, file: undefined });
        console.log("CLEARING TRACE FILE");
      } else {
        this.$emit("onAddTraceFile", { ...traceFile, file });
      }
    },
    getSourceClass(artifactFile: ArtifactFile, traceFile: TraceFile): string {
      return artifactFile.type !== traceFile.source ? "font-weight-bold" : "";
    },
    getTargetClass(artifactFile: ArtifactFile, traceFile: TraceFile): string {
      return artifactFile.type !== traceFile.target ? "font-weight-bold" : "";
    },
    createTraceFileLabel(source: string, traceFile: TraceFile): string {
      const isSource = traceFile.source === source;
      return isSource ? `To: ${traceFile.target}` : `From: ${traceFile.source}`;
    },
    getTraceFiles(artifactFile: ArtifactFile): TraceFile[] {
      return this.traceFiles.filter(
        (f) => f.source === artifactFile.type || f.target === artifactFile.type
      );
    },
    createAddTracePathButtonDefinition(
      artifactFile: ArtifactFile
    ): ButtonDefinition {
      return {
        type: ButtonType.LIST_MENU,
        label: "New Trace Path",
        buttonIsText: false,
        menuItems: this.menuLabels,
        menuHandlers: this.menuLabels.map(
          (targetType) => () =>
            this.$emit("onAddTracePath", {
              source: artifactFile.type,
              target: targetType,
              isGenerated: DEFAULT_IS_GENERATED,
            } as TraceFile)
        ),
      };
    },
  },
});
</script>
