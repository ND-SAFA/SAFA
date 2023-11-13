package edu.nd.crc.safa.features.jobs.builders;

import java.io.IOException;
import java.util.UUID;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.FlatFileProjectCreationJob;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.utilities.CommitJobUtility;
import edu.nd.crc.safa.utilities.FlatFileUtility;
import edu.nd.crc.safa.utilities.ProjectOwner;

import org.springframework.web.multipart.MultipartFile;

/**
 * Builds job for updating project via flat files.
 */
public class CreateProjectByFlatFileJobBuilder extends AbstractJobBuilder {

    /**
     * The files to parse
     */
    private final MultipartFile[] files;

    private final String projectName;
    private final String projectDescription;

    private final boolean shouldSummarize;
    private final UUID teamId;
    private final UUID orgId;

    public CreateProjectByFlatFileJobBuilder(ServiceProvider serviceProvider, MultipartFile[] files, SafaUser user,
                                             String projectName, String projectDescription, boolean shouldSummarize,
                                             UUID teamId, UUID orgId) {
        super(user, serviceProvider);
        this.files = files;
        this.projectName = projectName;
        this.projectDescription = projectDescription;
        this.shouldSummarize = shouldSummarize;
        this.teamId = teamId;
        this.orgId = orgId;
    }

    @Override
    protected AbstractJob constructJobForWork() throws IOException {
        SafaUser user = getUser();
        ProjectOwner owner =
            ProjectOwner.fromUUIDs(getServiceProvider(), teamId, orgId, user);
        ProjectCommitDefinition commit = CommitJobUtility.createProject(getServiceProvider(), owner, this.projectName,
            this.projectDescription, getUser());
        Project project = commit.getCommitVersion().getProject();
        String uploadLocation = FlatFileUtility.uploadFlatFiles(this.getServiceProvider(), project, this.files);

        // Step 3 - Create job worker
        return new FlatFileProjectCreationJob(
            user,
            this.getJobDbEntity(),
            this.getServiceProvider(),
            commit,
            uploadLocation,
            this.shouldSummarize,
            true);
    }

    @Override
    protected String getJobName() {
        return this.projectName;
    }

    @Override
    protected Class<? extends AbstractJob> getJobType() {
        return FlatFileProjectCreationJob.class;
    }
}
