package edu.nd.crc.safa.features.flatfiles.builder;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.errors.entities.db.CommitError;
import edu.nd.crc.safa.features.projects.entities.db.ProjectEntityType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

public class BuilderUtility {
    /**
     * Creates commit errors and saves them in project commit.
     *
     * @param projectCommitDefinition The commit to store errors in.
     * @param errors                  The error messages.
     * @param projectEntityType       The type of entities causing these errors.
     */
    public static void addErrorsToCommit(ProjectCommitDefinition projectCommitDefinition,
                                         List<String> errors,
                                         ProjectEntityType projectEntityType) {
        ProjectVersion projectVersion = projectCommitDefinition.getCommitVersion();
        List<CommitError> commitErrors =
            errors
                .stream()
                .map(e -> new CommitError(projectVersion, e, projectEntityType))
                .collect(Collectors.toList());
        projectCommitDefinition.getErrors().addAll(commitErrors);
    }
}
