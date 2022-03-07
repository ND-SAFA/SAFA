package unit;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;

import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.builders.AppEntityBuilder;
import edu.nd.crc.safa.builders.DbEntityBuilder;
import edu.nd.crc.safa.builders.JsonBuilder;
import edu.nd.crc.safa.builders.TestUtil;
import edu.nd.crc.safa.server.authentication.SafaUserService;
import edu.nd.crc.safa.server.entities.api.StringCreator;
import edu.nd.crc.safa.server.repositories.entities.ArtifactRepository;
import edu.nd.crc.safa.server.repositories.entities.ArtifactTypeRepository;
import edu.nd.crc.safa.server.repositories.entities.ArtifactVersionRepository;
import edu.nd.crc.safa.server.repositories.CommitErrorRepository;
import edu.nd.crc.safa.server.repositories.documents.DocumentRepository;
import edu.nd.crc.safa.server.repositories.projects.ProjectMembershipRepository;
import edu.nd.crc.safa.server.repositories.projects.ProjectRepository;
import edu.nd.crc.safa.server.repositories.projects.ProjectVersionRepository;
import edu.nd.crc.safa.server.repositories.projects.SafaUserRepository;
import edu.nd.crc.safa.server.repositories.entities.TraceLinkRepository;
import edu.nd.crc.safa.server.repositories.entities.TraceLinkVersionRepository;
import edu.nd.crc.safa.server.services.FileUploadService;
import edu.nd.crc.safa.server.services.ProjectService;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.json.JSONArray;
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

    @Autowired
    TestUtil testUtil;

    public static JSONObject jsonCreator(String content) {
        return content.length() == 0 ? new JSONObject() : new JSONObject(content);
    }

    public static JSONArray arrayCreator(String content) {
        return content.length() == 0 ? new JSONArray() : new JSONArray(content);
    }

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
                                  ResultMatcher test) throws Exception {
        return sendRequestWithCreator(request, test, "", EntityBaseTest::jsonCreator);
    }

    public JSONObject sendRequest(MockHttpServletRequestBuilder request,
                                  ResultMatcher test,
                                  String authorizationToken) throws Exception {
        return sendRequestWithCreator(request, test, authorizationToken, EntityBaseTest::jsonCreator);
    }

    public <T> T sendRequestWithCreator(MockHttpServletRequestBuilder request,
                                        ResultMatcher test,
                                        String authorizationToken,
                                        StringCreator<T> stringCreator) throws Exception {
        if (!authorizationToken.equals("")) {
            request = request.header("Authorization", authorizationToken);
        }
        return sendRequestWithResponse(request, test, stringCreator);
    }

    public <T> T sendRequestWithResponse(MockHttpServletRequestBuilder request,
                                         ResultMatcher test,
                                         StringCreator<T> stringCreator) throws Exception {

        MvcResult response = mockMvc
            .perform(request)
            .andExpect(test)
            .andReturn();

        return testUtil.apiResponseAsJsonObject(response, stringCreator);
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
