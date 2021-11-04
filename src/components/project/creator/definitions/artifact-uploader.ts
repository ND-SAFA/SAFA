import { parseArtifactFile } from "@/api/parse-api";
import { ParseArtifactFileResponse } from "@/types/api";
import { ArtifactFile } from "@/types/common-components";
import { Artifact } from "@/types/domain/artifact";
import { ArtifactMap, IGenericFilePanel, IGenericUploader } from "./types";

type ArtifactPanel = IGenericFilePanel<ArtifactMap, ArtifactFile>;

export function createArtifactUploader(): IGenericUploader<
  ArtifactMap,
  string,
  ArtifactFile
> {
  return {
    panels: [],
    createNewPanel,
  };
}

function createNewPanel(artifactName: string): ArtifactPanel {
  const emptyArtifactFile: ArtifactFile = createArtifactFile(artifactName);
  return {
    title: artifactName,
    entityNames: [],
    projectFile: emptyArtifactFile,
    getIsValid(): boolean {
      return isArtifactPanelValid(this);
    },
    clearPanel(): void {
      return clearPanel(this);
    },
    parseFile(artifactMap: ArtifactMap, file: File): Promise<void> {
      return createParsedArtifactFile(artifactMap, this, file);
    },
  };
}

function createArtifactFile(artifactType: string): ArtifactFile {
  return {
    type: artifactType,
    file: undefined,
    artifacts: [],
    errors: [],
  };
}

function isArtifactPanelValid(panel: ArtifactPanel): boolean {
  return (
    panel.projectFile.file !== undefined &&
    panel.projectFile.errors.length === 0
  );
}

function clearPanel(panel: ArtifactPanel): void {
  panel.projectFile = {
    ...panel.projectFile,
    file: undefined,
    artifacts: [],
    errors: [],
  };
  panel.entityNames = [];
}

function createParsedArtifactFile(
  artifactMap: ArtifactMap,
  panel: ArtifactPanel,
  file: File
): Promise<void> {
  return parseArtifactFile(panel.projectFile.type, file).then(
    (res: ParseArtifactFileResponse) => {
      const { artifacts, errors } = res;
      const validArtifacts: Artifact[] = [];
      artifacts.forEach((a) => {
        const error = getArtifactError(artifactMap, a);
        if (error === undefined) {
          validArtifacts.push(a);
        } else {
          errors.push(error);
        }
      });

      panel.projectFile = {
        ...panel.projectFile,
        artifacts: validArtifacts,
        errors,
        file,
      };
      panel.entityNames = artifacts.map((a) => a.name);
    }
  );
}

function getArtifactError(
  artifactMap: ArtifactMap,
  artifact: Artifact
): string | undefined {
  if (artifact.name in artifactMap) {
    return "Found duplicate artifact: " + artifact.name;
  }
}
