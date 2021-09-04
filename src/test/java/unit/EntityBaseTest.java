package unit;

import static org.assertj.core.api.Assertions.assertThat;

import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.db.entities.builders.AppBuilder;
import edu.nd.crc.safa.db.entities.builders.EntityBuilder;
import edu.nd.crc.safa.db.entities.builders.JsonBuilder;
import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.db.repositories.sql.ArtifactBodyRepository;
import edu.nd.crc.safa.db.repositories.sql.ArtifactRepository;
import edu.nd.crc.safa.db.repositories.sql.ArtifactTypeRepository;
import edu.nd.crc.safa.db.repositories.sql.ParserErrorRepository;
import edu.nd.crc.safa.db.repositories.sql.ProjectRepository;
import edu.nd.crc.safa.db.repositories.sql.ProjectVersionRepository;
import edu.nd.crc.safa.db.repositories.sql.TraceLinkRepository;
import edu.nd.crc.safa.server.responses.ServerError;
import edu.nd.crc.safa.server.services.FlatFileService;
import edu.nd.crc.safa.server.services.ProjectService;

import org.junit.jupiter.api.BeforeEach;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.multipart.MultipartFile;

public class EntityBaseTest extends SpringBootBaseTest {

    @Autowired
    protected ProjectRepository projectRepository;

    @Autowired
    protected ProjectVersionRepository projectVersionRepository;

    @Autowired
    protected ArtifactTypeRepository artifactTypeRepository;

    @Autowired
    protected ArtifactRepository artifactRepository;

    @Autowired
    protected ArtifactBodyRepository artifactBodyRepository;

    @Autowired
    protected TraceLinkRepository traceLinkRepository;

    @Autowired
    protected FlatFileService flatFileService;

    @Autowired
    protected ParserErrorRepository parserErrorRepository;

    @Autowired
    protected ProjectService projectService;

    @Autowired
    protected EntityBuilder entityBuilder;

    @Autowired
    protected AppBuilder appBuilder;

    @Autowired
    protected JsonBuilder jsonBuilder;

    @BeforeEach
    public void createData() {
        entityBuilder.createEmptyData();
        appBuilder.createEmptyData();
    }

    public ProjectVersion createProjectUploadedResources(String projectName) throws ServerError, IOException {
        ProjectVersion projectVersion = createProjectWithNewVersion(projectName);
        Project project = projectVersion.getProject();
        List<MultipartFile> files = MultipartHelper.createMultipartFilesFromDirectory(
            ProjectPaths.PATH_TO_TEST_RESOURCES,
            "files");
        List<String> uploadedFileNames = flatFileService.uploadFlatFiles(project, files);
        assertThat(uploadedFileNames.size())
            .as("test resources uploaded")
            .isEqualTo(TestConstants.N_FILES);
        return projectVersion;
    }

    public ProjectVersion createProjectWithNewVersion(String projectName) {
        return entityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .getProjectVersion(projectName, 0);
    }
}
