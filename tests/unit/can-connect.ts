import { expect } from "chai";
import {
  ArtifactIdentifierInformation,
  artifactTypesAreValid,
} from "../../src/cytoscape";
import { SafetyCaseType } from "../../src/types";

function generateSafetyNode(
  safetyCaseType: SafetyCaseType
): ArtifactIdentifierInformation {
  return {
    type: "node",
    safetyCaseType: safetyCaseType,
    artifactType: safetyCaseType,
  };
}
function generateNode(type: string): ArtifactIdentifierInformation {
  return {
    type: "node",
    artifactType: type,
  };
}
describe("Tests ability for links to connect", () => {
  it("Context -> Goal", () => {
    const sourceData: ArtifactIdentifierInformation = generateSafetyNode(
      SafetyCaseType.CONTEXT
    );

    const targetData: ArtifactIdentifierInformation = generateSafetyNode(
      SafetyCaseType.GOAL
    );
    const result = artifactTypesAreValid(sourceData, targetData);
    expect(result).to.be.true;
  });

  it("Artifact -> Strategy", () => {
    const sourceData: ArtifactIdentifierInformation =
      generateNode("requirement");

    const targetData: ArtifactIdentifierInformation = generateSafetyNode(
      SafetyCaseType.STRATEGY
    );
    const result = artifactTypesAreValid(sourceData, targetData);
    expect(result).to.be.true;
  });
});
