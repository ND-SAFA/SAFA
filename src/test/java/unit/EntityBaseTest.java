package unit;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;

import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.builders.AppBuilder;
import edu.nd.crc.safa.builders.EntityBuilder;
import edu.nd.crc.safa.builders.JsonBuilder;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.db.repositories.ArtifactBodyRepository;
import edu.nd.crc.safa.server.db.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.db.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.server.db.repositories.ParserErrorRepository;
import edu.nd.crc.safa.server.db.repositories.ProjectRepository;
import edu.nd.crc.safa.server.db.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.db.repositories.TraceLinkRepository;
import edu.nd.crc.safa.server.messages.ServerError;
import edu.nd.crc.safa.server.services.FlatFileService;
import edu.nd.crc.safa.server.services.ProjectService;

import org.json.JSONObject;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.ResultMatcher;
import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;
import org.springframework.test.web.servlet.request.MockMultipartHttpServletRequestBuilder;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
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

    public void uploadFlatFilesToVersion(ProjectVersion projectVersion,
                                         String pathToFileDir) throws Exception {
        String beforeRouteName = String.format("/projects/versions/%s/flat-files",
            projectVersion.getVersionId().toString());
        MockMultipartHttpServletRequestBuilder beforeRequest = createMultiPartRequest(beforeRouteName,
            pathToFileDir);
        sendRequest(beforeRequest, MockMvcResultMatchers.status().isCreated());
    }

    public ProjectVersion createProjectAndUploadBeforeFiles(String projectName) throws ServerError, IOException {
        ProjectVersion projectVersion = createProjectWithNewVersion(projectName);
        Project project = projectVersion.getProject();
        List<MultipartFile> files = MultipartHelper.createMultipartFilesFromDirectory(
            ProjectPaths.PATH_TO_BEFORE_FILES,
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

    public void sendPut(String routeName, JSONObject body, ResultMatcher test) throws Exception {
        sendRequest(put(routeName)
                .content(body.toString())
                .contentType(MediaType.APPLICATION_JSON),
            test);
    }

    public JSONObject sendPost(String routeName, JSONObject body, ResultMatcher test) throws Exception {
        return sendRequest(post(routeName)
                .content(body.toString())
                .contentType(MediaType.APPLICATION_JSON),
            test);
    }

    public JSONObject sendGet(String routeName, ResultMatcher test) throws Exception {
        return sendRequest(get(routeName), test);
    }

    public JSONObject sendRequest(MockHttpServletRequestBuilder request,
                                  ResultMatcher test) throws Exception {
        MvcResult response = mockMvc
            .perform(request)
            .andExpect(test)
            .andReturn();
        return TestUtil.asJson(response);
    }

    public MockMultipartHttpServletRequestBuilder createMultiPartRequest(String routeName, String pathToFiles)
        throws IOException {
        String attributeName = "files";

        List<MockMultipartFile> files =
            MultipartHelper.createMockMultipartFilesFromDirectory(pathToFiles, attributeName);
        MockMultipartHttpServletRequestBuilder request = multipart(routeName);

        for (MockMultipartFile file : files) {
            request.file(file);
        }

        return request;
    }
}
