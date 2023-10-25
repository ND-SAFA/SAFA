import { defineStore } from "pinia";

import {
  ArtifactMap,
  CreatorFilePanel,
  ParseApiHook,
  TraceLinkSchema,
} from "@/types";
import { extractTraceId } from "@/util";
import { useApi } from "@/hooks";
import { parseArtifactFile, parseTraceFile } from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing file parsing API requests.
 */
export const useParseApi = defineStore("useParseApi", (): ParseApiHook => {
  const parseApi = useApi("parseApi");

  /**
   * Returns any errors for the given trace links.
   *
   * @param panel - The panel for uploading trace links.
   * @param artifactMap - A collection of all artifacts.
   * @param traces - The traces to check for errors.
   * @return The error message, if there is one.
   */
  function getTraceErrors(
    panel: CreatorFilePanel,
    artifactMap: ArtifactMap,
    traces: TraceLinkSchema[]
  ): string[] {
    const errors: string[] = [];

    traces.forEach(({ sourceName, targetName }) => {
      if (!(sourceName in artifactMap)) {
        errors.push(`Artifact ${sourceName} does not exist`);
      } else if (!(targetName in artifactMap)) {
        errors.push(`Artifact ${targetName} does not exist`);
      } else {
        const sourceArtifact = artifactMap[sourceName];
        const targetArtifact = artifactMap[targetName];

        if (sourceArtifact.type !== panel.type) {
          errors.push(`${sourceArtifact.name} is not of type ${panel.type}`);
        }

        if (targetArtifact.type !== panel.toType) {
          errors.push(`${targetArtifact.name} is not of type ${panel.toType}`);
        }
      }
    });

    return errors;
  }

  async function handleParseProjectFile(
    panel: CreatorFilePanel,
    artifactMap: ArtifactMap
  ): Promise<void> {
    await parseApi.handleRequest(
      async () => {
        if (!panel.file) return;

        const [fileType = "", fileTargetType = ""] =
          panel.file.name?.split(".")[0]?.split("2") || [];

        panel.loading = true;
        panel.type = panel.type || fileType;

        if (panel.variant === "artifact") {
          await parseArtifactFile(panel.type, panel.file).then(
            ({ entities, errors }) => {
              panel.artifacts = entities;
              panel.parseErrorMessage =
                errors.length === 0 ? undefined : errors.join(", ");
              panel.itemNames = entities.map(({ name }) => name);

              entities.forEach((artifact) => {
                artifactMap[artifact.name] = artifact;
              });
            }
          );
        } else {
          panel.toType = panel.toType || fileTargetType;

          await parseTraceFile(panel.file).then(({ entities, errors }) => {
            panel.traces = entities;

            errors.push(...getTraceErrors(panel, artifactMap, entities));

            panel.parseErrorMessage =
              errors.length === 0 ? undefined : errors.join(", ");
            panel.itemNames = entities.map(extractTraceId);
          });
        }
      },
      {
        onError: () => (panel.errorMessage = "Unable to parse this file"),
        onComplete: () => (panel.loading = false),
      }
    );
  }

  return { handleParseProjectFile };
});

export default useParseApi(pinia);
