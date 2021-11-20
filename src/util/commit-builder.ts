import { Artifact, Commit, ProjectVersion } from "@/types";
import { appModule, projectModule } from "@/store";

export class CommitBuilder {
  commit: Commit;

  constructor(version: ProjectVersion) {
    this.commit = {
      commitVersion: version,
      artifacts: {
        added: [],
        removed: [],
        modified: [],
      },
      traces: {
        added: [],
        removed: [],
        modified: [],
      },
    };
  }

  static withCurrentVersion(): CommitBuilder {
    const version = projectModule.getProject.projectVersion;
    if (version === undefined) {
      throw Error("No project version is selected.");
    }
    return new CommitBuilder(version);
  }
  withNewArtifact(artifact: Artifact): CommitBuilder {
    this.commit.artifacts.added.push(artifact);
    return this;
  }
  get(): Commit {
    return this.commit;
  }
}
