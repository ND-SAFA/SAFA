package unit;

import static org.assertj.core.api.Assertions.assertThat;

import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.constants.ProjectPaths;
import edu.nd.crc.safa.database.repositories.ArtifactRepository;
import edu.nd.crc.safa.database.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.database.repositories.ProjectRepository;
import edu.nd.crc.safa.database.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.entities.ArtifactType;
import edu.nd.crc.safa.entities.Project;
import edu.nd.crc.safa.entities.ProjectVersion;
import edu.nd.crc.safa.output.error.ServerError;
import edu.nd.crc.safa.services.FlatFileService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.multipart.MultipartFile;
import unit.utilities.TestFileUtility;

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
    protected FlatFileService flatFileService;

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

    public ProjectVersion createProjectWithTestResources(String projectName) throws ServerError, IOException {
        ProjectVersion projectVersion = createProjectWithNewVersion(projectName);
        Project project = projectVersion.getProject();
        List<MultipartFile> files = TestFileUtility.createMultipartFilesFromDirectory(
            ProjectPaths.PATH_TO_TEST_RESOURCES,
            "files");
        List<String> uploadedFileNames = flatFileService.uploadFlatFiles(project, files);
        assertThat(uploadedFileNames.size()).as("test resources uploaded").isEqualTo(N_TEST_RESOURCES);
        return projectVersion;
    }
}
