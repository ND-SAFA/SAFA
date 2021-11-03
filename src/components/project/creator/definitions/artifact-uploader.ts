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
    createNewPanel(artifactName: string): ArtifactPanel {
      return createNewPanel(artifactName);
    },
  };
}

function createNewPanel(artifactName: string): ArtifactPanel {
  const emptyArtifactFile: ArtifactFile = createArtifactFile(artifactName);
  const newPanel: ArtifactPanel = {
    title: artifactName,
    entityNames: [],
    projectFile: emptyArtifactFile,
    getIsValid(): boolean {
      return isArtifactPanelValid(this);
    },
    clearFile(): ArtifactPanel {
      return clearPanelFile(this);
    },
    parseFile(
      artifactMap: ArtifactMap,
      file: File
    ): Promise<IGenericFilePanel<ArtifactMap, ArtifactFile>> {
      return createParsedArtifactFile(artifactMap, this, file);
    },
  };
  return newPanel;
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

function clearPanelFile(panel: ArtifactPanel): ArtifactPanel {
  const updatedFile: ArtifactFile = {
    ...panel.projectFile,
    file: undefined,
    artifacts: [],
    errors: [],
  };
  return {
    ...panel,
    projectFile: updatedFile,
    entityNames: [],
  };
}

function createParsedArtifactFile(
  artifactMap: ArtifactMap,
  panel: ArtifactPanel,
  file: File
): Promise<ArtifactPanel> {
  return new Promise((resolve, reject) => {
    const { projectFile } = panel;
    parseArtifactFile(projectFile.type, file)
      .then((res: ParseArtifactFileResponse) => {
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
        const updatedFile: ArtifactFile = {
          ...projectFile,
          artifacts: validArtifacts,
          errors,
          file,
        };

        const updatedPanel: IGenericFilePanel<ArtifactMap, ArtifactFile> = {
          ...panel,
          entityNames: artifacts.map((a) => a.name),
          projectFile: updatedFile,
        };

        resolve(updatedPanel);
      })
      .catch(reject);
  });
}

function getArtifactError(
  artifactMap: ArtifactMap,
  artifact: Artifact
): string | undefined {
  if (artifact.name in artifactMap) {
    return "Found duplicate artifact: " + artifact.name;
  }
}
