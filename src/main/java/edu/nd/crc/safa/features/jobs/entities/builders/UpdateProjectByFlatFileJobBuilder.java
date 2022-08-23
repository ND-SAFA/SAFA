package edu.nd.crc.safa.features.jobs.entities.builders;

import java.io.IOException;
import java.util.Arrays;
import java.util.UUID;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.services.FileUploadService;
import edu.nd.crc.safa.features.jobs.entities.app.FlatFileProjectCreationJob;
import edu.nd.crc.safa.features.jobs.entities.app.JobType;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
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
    JobDefinition constructJobForWork() throws IOException {
        String projectName = this.identifier.getProject().getName();
        JobDbEntity jobDbEntity = this.serviceProvider
            .getJobService()
            .createNewJob(JobType.FLAT_FILE_PROJECT_CREATION, projectName);

        uploadFlatFiles(this.identifier.getProject());

        // Step 3 - Create job worker
        FlatFileProjectCreationJob flatFileCreationJob = new FlatFileProjectCreationJob(jobDbEntity,
            serviceProvider,
            this.identifier,
            files);

        return new JobDefinition(jobDbEntity, flatFileCreationJob);
    }

    private void uploadFlatFiles(Project project) throws IOException {
        FileUploadService fileUploadService = this.serviceProvider.getFileUploadService();
        fileUploadService.uploadFilesToServer(project, Arrays.asList(files));
    }
}
