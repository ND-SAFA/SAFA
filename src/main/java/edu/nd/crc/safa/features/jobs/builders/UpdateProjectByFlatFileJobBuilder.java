package edu.nd.crc.safa.features.jobs.builders;

import java.io.IOException;
import java.util.Arrays;
import java.util.UUID;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.services.FileUploadService;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.CreateProjectViaFlatFilesJob;
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
    ProjectVersion projectVersion;

    /**
     * The files to parse
     */
    MultipartFile[] files;

    public UpdateProjectByFlatFileJobBuilder(ServiceProvider serviceProvider,
                                             UUID versionId,
                                             MultipartFile[] files) {
        super(serviceProvider);
        this.projectVersion = this.serviceProvider.getProjectVersionRepository().findByVersionId(versionId);
        this.files = files;
    }

    @Override
    protected AbstractJob constructJobForWork() throws IOException {
        uploadFlatFiles(this.projectVersion.getProject());

        // Step 3 - Create job worker
        return new CreateProjectViaFlatFilesJob(
            this.jobDbEntity,
            serviceProvider,
            this.projectVersion,
            files);
    }

    @Override
    protected String getJobName() {
        return this.projectVersion.getProject().getName();
    }

    @Override
    protected Class<? extends AbstractJob> getJobType() {
        return CreateProjectViaFlatFilesJob.class;
    }

    private void uploadFlatFiles(Project project) throws IOException {
        FileUploadService fileUploadService = this.serviceProvider.getFileUploadService();
        fileUploadService.uploadFilesToServer(project, Arrays.asList(files));
    }
}
