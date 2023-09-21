package edu.nd.crc.safa.features.jobs.builders;

import java.io.IOException;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.FlatFileProjectCreationJob;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.utilities.CommitJobUtility;
import edu.nd.crc.safa.utilities.FlatFileUtility;

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

    public CreateProjectByFlatFileJobBuilder(ServiceProvider serviceProvider, MultipartFile[] files, SafaUser user,
                                             String projectName, String projectDescription, boolean shouldSummarize) {
        super(serviceProvider, user);
        this.files = files;
        this.projectName = projectName;
        this.projectDescription = projectDescription;
        this.shouldSummarize = shouldSummarize;
    }

    @Override
    protected AbstractJob constructJobForWork() throws IOException {
        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
        ProjectCommitDefinition commit = CommitJobUtility.createProject(getServiceProvider(), user, this.projectName,
            this.projectDescription);
        Project project = commit.getCommitVersion().getProject();
        String uploadLocation = FlatFileUtility.uploadFlatFiles(this.getServiceProvider(), project, this.files);

        // Step 3 - Create job worker
        return new FlatFileProjectCreationJob(
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
