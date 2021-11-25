package unit.delta;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.services.DeltaService;
import edu.nd.crc.safa.server.services.ProjectRetrievalService;

import org.javatuples.Pair;
import org.springframework.beans.factory.annotation.Autowired;
import unit.ApplicationBaseTest;

public class DeltaBaseTest extends ApplicationBaseTest {

    @Autowired
    DeltaService deltaService;

    @Autowired
    ProjectRetrievalService projectRetrievalService;


    protected Pair<ProjectVersion, ProjectVersion> setupDualVersions(String projectName) throws Exception {
        return setupDualVersions(projectName, true);
    }

    protected Pair<ProjectVersion, ProjectVersion> setupDualVersions(String projectName, boolean uploadFiles) throws Exception {
        dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newVersion(projectName);

        ProjectVersion beforeVersion = dbEntityBuilder.getProjectVersion(projectName, 0);
        ProjectVersion afterVersion = dbEntityBuilder.getProjectVersion(projectName, 1);

        if (uploadFiles) {
            uploadFlatFilesToVersion(beforeVersion, ProjectPaths.PATH_TO_BEFORE_FILES);
            uploadFlatFilesToVersion(afterVersion, ProjectPaths.PATH_TO_AFTER_FILES);
        }

        return new Pair<>(beforeVersion, afterVersion);
    }
}
