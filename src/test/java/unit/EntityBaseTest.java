package unit;

import static org.assertj.core.api.Assertions.assertThat;

import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.configuration.ProjectPaths;
import edu.nd.crc.safa.entities.ArtifactType;
import edu.nd.crc.safa.entities.Project;
import edu.nd.crc.safa.entities.ProjectVersion;
import edu.nd.crc.safa.repositories.ArtifactBodyRepository;
import edu.nd.crc.safa.repositories.ArtifactRepository;
import edu.nd.crc.safa.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.repositories.ParserErrorRepository;
import edu.nd.crc.safa.repositories.ProjectRepository;
import edu.nd.crc.safa.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.repositories.TraceLinkRepository;
import edu.nd.crc.safa.responses.ServerError;
import edu.nd.crc.safa.services.FlatFileService;
import edu.nd.crc.safa.services.ProjectService;

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

    public Project createProject(String projectName) {
        Project project = new Project(projectName);
        projectRepository.save(project);
        return project;
    }

    public ProjectVersion createProjectWithNewVersion(String projectName) {
        Project project = createProject(projectName);
        ProjectVersion newVersion = new ProjectVersion(project);
        this.projectVersionRepository.save(newVersion);
        return newVersion;
    }

    public ArtifactType createArtifactType(Project project, String artifactTypeName) {
        ArtifactType artifactType = new ArtifactType(project, artifactTypeName);
        artifactTypeRepository.save(artifactType);
        return artifactType;
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
}
