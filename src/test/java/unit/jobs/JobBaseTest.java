package unit.jobs;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.UUID;

import edu.nd.crc.safa.builders.requests.FlatFileRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.app.JobStatus;
import edu.nd.crc.safa.server.entities.db.JobDbEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.JobDbRepository;
import edu.nd.crc.safa.server.services.NotificationService;
import edu.nd.crc.safa.server.services.ServiceProvider;
import edu.nd.crc.safa.server.services.jobs.JobService;

import org.json.JSONObject;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.beans.factory.annotation.Autowired;
import unit.flatfile.FlatFileBaseTest;

public class JobBaseTest extends FlatFileBaseTest {

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
            .withRoute(AppRoutes.Jobs.flatFileProjectUpdateJob)
            .withVersion(projectVersion)
            .getFlatFileHelper()
            .uploadFlatFilesToVersion(ProjectPaths.PATH_TO_DEFAULT_PROJECT);

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
