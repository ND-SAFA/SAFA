package edu.nd.crc.safa.features.jobs.builders;

import java.io.IOException;
import java.util.Arrays;
import java.util.UUID;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.services.FileUploadService;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.FlatFileProjectCreationJob;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.springframework.web.multipart.MultipartFile;

/**
 * Builds job for updating project via flat files.
 */
public class UpdateProjectByFlatFileJobBuilder extends AbstractJobBuilder {

    /**
     * ProjectVersion being updated.
     */
    private ProjectVersion projectVersion;

    /**
     * The files to parse
     */
    private MultipartFile[] files;

    /**
     * Whether the code artifacts should be summarized if no summary exists
     */
    private boolean shouldSummarize;

    public UpdateProjectByFlatFileJobBuilder(ServiceProvider serviceProvider,
                                             UUID versionId,
                                             MultipartFile[] files,
                                             boolean shouldSummarize) {
        super(serviceProvider);
        this.projectVersion = this.getServiceProvider().getProjectVersionRepository().findByVersionId(versionId);
        this.files = files;
        this.shouldSummarize = shouldSummarize;
    }

    @Override
    protected AbstractJob constructJobForWork() throws IOException {
        uploadFlatFiles(this.projectVersion.getProject());

        // Step 3 - Create job worker
        return new FlatFileProjectCreationJob(
            this.getJobDbEntity(),
            getServiceProvider(),
            this.projectVersion,
            this.shouldSummarize);
    }

    @Override
    protected String getJobName() {
        return this.projectVersion.getProject().getName();
    }

    @Override
    protected Class<? extends AbstractJob> getJobType() {
        return FlatFileProjectCreationJob.class;
    }

    private void uploadFlatFiles(Project project) throws IOException {
        FileUploadService fileUploadService = this.getServiceProvider().getFileUploadService();
        fileUploadService.uploadFilesToServer(project, Arrays.asList(files));
    }
}
