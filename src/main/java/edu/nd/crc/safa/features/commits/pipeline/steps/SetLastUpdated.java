package edu.nd.crc.safa.features.commits.pipeline.steps;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.commits.pipeline.ICommitStep;
import edu.nd.crc.safa.features.commits.services.CommitService;
import edu.nd.crc.safa.features.projects.entities.db.Project;

public class SetLastUpdated implements ICommitStep {
    /**
     * Sets a project's last updated timestamp.
     *
     * @param service The commit service to access database and other services.
     * @param commit  The commit being performed.
     * @param after   The commit final state.
     */
    @Override
    public void performStep(CommitService service, ProjectCommit commit, ProjectCommit after) {
        // Step - Update project last edited
        Project project = commit.getCommitVersion().getProject();
        project.setLastEdited();
        service.getProjectRepository().save(project);
    }
}
