package edu.nd.crc.safa.features.jobs.builders;

import java.io.IOException;
import java.util.Arrays;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.services.FileUploadService;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.FlatFileProjectCreationJob;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

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

    public CreateProjectByFlatFileJobBuilder(ServiceProvider serviceProvider, MultipartFile[] files,
                                             SafaUser user, String projectName, String projectDescription) {
        super(serviceProvider, user);
        this.files = files;
        this.projectName = projectName;
        this.projectDescription = projectDescription;
    }

    @Override
    protected AbstractJob constructJobForWork() throws IOException {
        String uploadLocation = ProjectPaths.Storage.createTemporaryDirectory();
        String projectPath = ProjectPaths.Storage.getStorageRelativePath(uploadLocation);
        FileUploadService fileUploadService = this.serviceProvider.getFileUploadService();
        fileUploadService.uploadFilesToServer(projectPath, Arrays.asList(files));

        // Step 3 - Create job worker
        return new FlatFileProjectCreationJob(
            this.jobDbEntity,
            this.serviceProvider,
            this.user,
            this.projectName,
            this.projectDescription,
            uploadLocation);
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
