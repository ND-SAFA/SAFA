package edu.nd.crc.safa.features.jobs.builders;

import java.io.IOException;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.builder.FlatFileBuilderStore;
import edu.nd.crc.safa.features.flatfiles.builder.steps.UploadFilesStep;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.FlatFileProjectCreationJob;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.utilities.CommitJobUtility;
import edu.nd.crc.safa.utilities.ProjectOwner;

import org.springframework.web.multipart.MultipartFile;

/**
 * Builds job for updating project via flat files.
 */
public class CreateProjectByFlatFileJobBuilder extends AbstractJobBuilder {

    private final List<MultipartFile> files;
    private final String projectName;
    private final String projectDescription;
    private final boolean shouldSummarize;
    private final UUID teamId;
    private final UUID orgId;

    public CreateProjectByFlatFileJobBuilder(ServiceProvider serviceProvider, List<MultipartFile> files, SafaUser user,
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

        FlatFileBuilderStore store = new FlatFileBuilderStore(
            user,
            this.files,
            commit.getCommitVersion(),
            true,
            this.shouldSummarize,
            false
        );

        UploadFilesStep step = new UploadFilesStep();
        step.perform(store, getServiceProvider());

        // Step 3 - Create job worker
        return new FlatFileProjectCreationJob(
            user,
            this.getJobDbEntity(),
            this.getServiceProvider(),
            store,
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
