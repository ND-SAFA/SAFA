package edu.nd.crc.safa.features.jobs.builders;

import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.builder.FlatFileBuilderStore;
import edu.nd.crc.safa.features.flatfiles.builder.steps.UploadFilesStep;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.FlatFileProjectCreationJob;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

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
    private final List<MultipartFile> files;

    /**
     * Whether the uploaded files represents the complete artifactsets.
     */
    private final boolean asCompleteSet;
    /**
     * Whether to summarize artifacts.
     */
    private final boolean summarizeArtifacts;

    public UpdateProjectByFlatFileJobBuilder(SafaUser user,
                                             ServiceProvider serviceProvider,
                                             ProjectVersion projectVersion,
                                             List<MultipartFile> files,
                                             boolean asCompleteSet,
                                             boolean summarizeArtifacts) {
        super(user, serviceProvider);
        this.projectVersion = projectVersion;
        this.files = files;
        this.asCompleteSet = asCompleteSet;
        this.summarizeArtifacts = summarizeArtifacts;
    }

    @Override
    protected AbstractJob constructJobForWork() throws IOException {
        FlatFileBuilderStore store = new FlatFileBuilderStore(
            getUser(),
            this.files,
            this.projectVersion,
            this.asCompleteSet,
            this.summarizeArtifacts,
            false
        );

        UploadFilesStep step = new UploadFilesStep();
        step.perform(store, getServiceProvider());

        // Step 3 - Create job worker
        return new FlatFileProjectCreationJob(
            getUser(),
            this.getJobDbEntity(),
            getServiceProvider(),
            store,
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
