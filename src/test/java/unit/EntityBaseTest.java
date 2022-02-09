package unit;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;

import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.builders.AppEntityBuilder;
import edu.nd.crc.safa.builders.DbEntityBuilder;
import edu.nd.crc.safa.builders.JsonBuilder;
import edu.nd.crc.safa.server.authentication.SafaUserService;
import edu.nd.crc.safa.server.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.server.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.server.repositories.CommitErrorRepository;
import edu.nd.crc.safa.server.repositories.DocumentRepository;
import edu.nd.crc.safa.server.repositories.ProjectMembershipRepository;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.repositories.SafaUserRepository;
import edu.nd.crc.safa.server.repositories.TraceLinkRepository;
import edu.nd.crc.safa.server.repositories.TraceLinkVersionRepository;
import edu.nd.crc.safa.server.services.FileUploadService;
import edu.nd.crc.safa.server.services.ProjectService;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.json.JSONObject;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.ResultMatcher;
import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;
import org.springframework.test.web.servlet.request.MockMultipartHttpServletRequestBuilder;

/**
 * Provides layer of access to entities in database.
 */
public abstract class EntityBaseTest extends SpringBootBaseTest {

    @Autowired
    protected ProjectRepository projectRepository;

    @Autowired
    protected ProjectVersionRepository projectVersionRepository;

    @Autowired
    protected ArtifactTypeRepository artifactTypeRepository;

    @Autowired
    protected ArtifactRepository artifactRepository;

    @Autowired
    protected ArtifactVersionRepository artifactVersionRepository;

    @Autowired
    protected TraceLinkRepository traceLinkRepository;

    @Autowired
    protected TraceLinkVersionRepository traceLinkVersionRepository;

    @Autowired
    protected FileUploadService fileUploadService;

    @Autowired
    protected CommitErrorRepository commitErrorRepository;

    @Autowired
    protected SafaUserRepository safaUserRepository;

    @Autowired
    protected ProjectMembershipRepository projectMembershipRepository;

    @Autowired
    protected DocumentRepository documentRepository;

    @Autowired
    protected ProjectService projectService;

    @Autowired
    protected SafaUserService safaUserService;

    @Autowired
    protected DbEntityBuilder dbEntityBuilder;

    @Autowired
    protected AppEntityBuilder appBuilder;

    @Autowired
    protected JsonBuilder jsonBuilder;

    @Autowired
    ObjectMapper objectMapper;

    @BeforeEach
    public void createNewBuilders() {
        dbEntityBuilder.createEmptyData();
        appBuilder.createEmptyData();
        jsonBuilder.createEmptyData();
    }

    protected MockHttpServletRequestBuilder addJsonBody(MockHttpServletRequestBuilder request,
                                                        Object body) {
        return request
            .content(body.toString())
            .contentType(MediaType.APPLICATION_JSON);
    }


    public JSONObject sendRequest(MockHttpServletRequestBuilder request,
                                  ResultMatcher test,
                                  String authorizationToken
    ) throws Exception {
        MockHttpServletRequestBuilder authorizedRequest = request.header("Authorization", authorizationToken);
        return sendRequest(authorizedRequest, test);
    }

    public JSONObject sendRequest(MockHttpServletRequestBuilder request,
                                  ResultMatcher test) throws Exception {

        MvcResult response = mockMvc
            .perform(request)
            .andExpect(test)
            .andReturn();

        return TestUtil.apiResponseAsJson(response);
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

    public MockMultipartHttpServletRequestBuilder createSingleFileRequest(String routeName, String pathToFile)
        throws IOException {
        String attributeName = "file";

        MockMultipartFile file = MultipartHelper.createFile(pathToFile, attributeName);
        MockMultipartHttpServletRequestBuilder request = multipart(routeName);
        request.file(file);

        return request;
    }

    public JSONObject toJson(Object object) throws JsonProcessingException {
        String objectJsonString = objectMapper.writeValueAsString(object);
        return new JSONObject(objectJsonString);
    }
}
