package unit.jobs;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.UUID;

import edu.nd.crc.safa.builders.requests.FlatFileRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.app.JobStatus;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.repositories.JobDbRepository;
import edu.nd.crc.safa.features.jobs.services.JobService;
import edu.nd.crc.safa.features.notifications.NotificationService;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import org.json.JSONObject;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.beans.factory.annotation.Autowired;
import unit.flatfile.BaseFlatFileTest;

public abstract class JobBaseFlatFileTest extends BaseFlatFileTest {

    @Autowired
    public JobService jobService;

    @Autowired
    public NotificationService notificationService;

    @Autowired
    public JobDbRepository jobDbRepository;

    @Autowired
    public ServiceProvider serviceProvider;

    String projectName = "test-before-files";
    ProjectVersion projectVersion;

    @BeforeEach
    public void createDefaultProject() {
        this.projectVersion = dbEntityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);
    }

    public UUID createJobFromDefaultProject() throws Exception {
        JSONObject jobSubmissionResponse = FlatFileRequest
            .withRoute(AppRoutes.Jobs.FLAT_FILE_PROJECT_UPDATE_JOB)
            .withVersion(projectVersion)
            .getFlatFileHelper()
            .postWithFilesInDirectory(ProjectPaths.PATH_TO_DEFAULT_PROJECT);

        return UUID.fromString(jobSubmissionResponse.getString("id"));
    }

    public JobDbEntity verifyJobWasCompleted(UUID jobId, int nSteps) {
        JobDbEntity jobDbEntity = jobService.getJobById(jobId);
        assertThat(jobDbEntity.getCurrentStep()).isEqualTo(nSteps);
        assertThat(jobDbEntity.getCurrentProgress()).isEqualTo(100);
        assertThat(jobDbEntity.getStatus()).isEqualTo(JobStatus.COMPLETED);

        // Step - Assert that start is before completed.
        assert jobDbEntity.getCompletedAt() != null;
        int comparison = jobDbEntity.getCompletedAt().compareTo(jobDbEntity.getStartedAt());
        assertThat(comparison).isEqualTo(1);

        // Step - Assert that lastUpdatedBy is after start.
        comparison = jobDbEntity.getLastUpdatedAt().compareTo(jobDbEntity.getStartedAt());
        assertThat(comparison).isEqualTo(1);

        return jobDbEntity;
    }
}
