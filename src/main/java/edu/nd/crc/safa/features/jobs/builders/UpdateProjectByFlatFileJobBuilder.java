package edu.nd.crc.safa.features.jobs.builders;

import java.io.IOException;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.FlatFileProjectCreationJob;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.FlatFileUtility;

import org.springframework.web.multipart.MultipartFile;

/**
 * Builds job for updating project via flat files.
 */
public class UpdateProjectByFlatFileJobBuilder extends AbstractJobBuilder {

    /**
     * ProjectVersion being updated.
     */
    private final ProjectVersion projectVersion;

    /**
     * The files to parse
     */
    private final MultipartFile[] files;

    /**
     * Whether the code artifacts should be summarized if no summary exists
     */
    private final boolean shouldSummarize;

    public UpdateProjectByFlatFileJobBuilder(SafaUser user,
                                             ServiceProvider serviceProvider,
                                             ProjectVersion projectVersion,
                                             MultipartFile[] files,
                                             boolean shouldSummarize) {
        super(user, serviceProvider);
        this.projectVersion = projectVersion;
        this.files = files;
        this.shouldSummarize = shouldSummarize;
    }

    @Override
    protected AbstractJob constructJobForWork() throws IOException {
        String uploadLocation = FlatFileUtility.uploadFlatFiles(getServiceProvider(),
            this.projectVersion.getProject(),
            this.files);
        ProjectCommitDefinition commit = new ProjectCommitDefinition(projectVersion, false);

        // Step 3 - Create job worker
        return new FlatFileProjectCreationJob(
            getUser(),
            this.getJobDbEntity(),
            getServiceProvider(),
            commit,
            uploadLocation,
            this.shouldSummarize,
            false);
    }

    @Override
    protected String getJobName() {
        return this.projectVersion.getProject().getName();
    }

    @Override
    protected Class<? extends AbstractJob> getJobType() {
        return FlatFileProjectCreationJob.class;
    }
}
