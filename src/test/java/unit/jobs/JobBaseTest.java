package unit.jobs;

import java.util.UUID;

import edu.nd.crc.safa.common.AppRoutes;
import edu.nd.crc.safa.common.ProjectPaths;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.services.NotificationService;
import edu.nd.crc.safa.server.services.jobs.JobService;

import org.json.JSONObject;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.beans.factory.annotation.Autowired;
import unit.flatfile.FlatFileBaseTest;

public class JobBaseTest extends FlatFileBaseTest {

    @Autowired
    JobService jobService;

    @Autowired
    NotificationService notificationService;

    String projectName = "test-before-files";
    ProjectVersion projectVersion;

    @BeforeEach
    public void createDefaultProject() {
        this.projectVersion = dbEntityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);
    }

    protected UUID createJobFromDefaultProject() throws Exception {
        JSONObject response = uploadFlatFilesToVersion(projectVersion,
            ProjectPaths.PATH_TO_BEFORE_FILES,
            AppRoutes.Jobs.flatFileProjectUpdateJob);

        return UUID.fromString(response.getString("id"));
    }
}
