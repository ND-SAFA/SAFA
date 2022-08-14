package features.jobs.base;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.UUID;

import edu.nd.crc.safa.builders.requests.FlatFileRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.repositories.JobDbRepository;
import edu.nd.crc.safa.features.jobs.services.JobService;
import edu.nd.crc.safa.features.notifications.NotificationService;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import features.flatfiles.base.BaseFlatFileTest;
import org.json.JSONObject;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.web.servlet.ResultMatcher;

public abstract class AbstractUpdateProjectViaFlatFileTest extends BaseFlatFileTest {

    @Autowired
    public JobService jobService;

    @Autowired
    public NotificationService notificationService;

    @Autowired
    public JobDbRepository jobDbRepository;

    @Autowired
    public ServiceProvider serviceProvider;

    protected String projectName = "test-before-files";
    protected ProjectVersion projectVersion;

    @BeforeEach
    public void createDefaultProject() {
        this.projectVersion = dbEntityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);
    }

    /**
     * Uploads project files at given directory to update project by flat files route.
     *
     * @param pathToProjectFiles Path to project files.
     * @return {@link UUID} ID of update project job.
     * @throws Exception If HTTP error occurs.
     */
    public UUID updateProjectViaFlatFiles(String pathToProjectFiles) throws Exception {
        JSONObject response = updateProjectViaFlatFiles(pathToProjectFiles, status().is2xxSuccessful());
        return UUID.fromString(response.getString("id"));
    }

    public JSONObject updateProjectViaFlatFiles(String pathToProjectFiles, ResultMatcher resultMatcher) throws Exception {
        JSONObject kwargs = new JSONObject();
        kwargs.put(ProjectVariables.AS_COMPLETE_SET, false);
        return FlatFileRequest
            .withRoute(AppRoutes.Jobs.FLAT_FILE_PROJECT_UPDATE_JOB)
            .withVersion(projectVersion)
            .getFlatFileHelper()
            .postWithFilesInDirectory(pathToProjectFiles, resultMatcher, kwargs);
    }
}
