package edu.nd.crc.safa.features.jobs.builders;

import java.io.IOException;
import java.util.Arrays;
import java.util.UUID;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.services.FileUploadService;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.app.JobType;
import edu.nd.crc.safa.features.jobs.entities.jobs.FlatFileProjectCreationJob;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.springframework.web.multipart.MultipartFile;

/**
 * Builds job for updating project via flat files.
 */
public class UpdateProjectByFlatFileJobBuilder extends AbstractJobBuilder<ProjectVersion> {

    /**
     * ID of ProjectVersion being updated.
     */
    UUID versionId;

    /**
     * The files to parse
     */
    MultipartFile[] files;

    public UpdateProjectByFlatFileJobBuilder(ServiceProvider serviceProvider,
                                             UUID versionId,
                                             MultipartFile[] files) {
        super(serviceProvider);
        this.versionId = versionId;
        this.files = files;
    }

    @Override
    protected ProjectVersion constructIdentifier() {
        return this.serviceProvider
            .getProjectVersionRepository()
            .findByVersionId(versionId);
    }

    @Override
    AbstractJob constructJobForWork() throws IOException {
        uploadFlatFiles(this.identifier.getProject());

        // Step 3 - Create job worker
        return new FlatFileProjectCreationJob(
            this.jobDbEntity,
            serviceProvider,
            this.identifier,
            files);
    }

    @Override
    String getJobName() {
        return this.identifier.getProject().getName();
    }

    @Override
    JobType getJobType() {
        return JobType.PROJECT_CREATION_VIA_FLAT_FILE;
    }

    private void uploadFlatFiles(Project project) throws IOException {
        FileUploadService fileUploadService = this.serviceProvider.getFileUploadService();
        fileUploadService.uploadFilesToServer(project, Arrays.asList(files));
    }
}
