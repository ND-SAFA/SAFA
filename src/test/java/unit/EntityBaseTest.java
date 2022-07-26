package unit;

import edu.nd.crc.safa.builders.AppEntityBuilder;
import edu.nd.crc.safa.builders.DbEntityBuilder;
import edu.nd.crc.safa.builders.JsonBuilder;
import edu.nd.crc.safa.flatfiles.services.FileUploadService;
import edu.nd.crc.safa.server.authentication.SafaUserService;
import edu.nd.crc.safa.server.repositories.CommitErrorRepository;
import edu.nd.crc.safa.server.repositories.artifacts.ArtifactTypeRepository;
import edu.nd.crc.safa.server.repositories.artifacts.ArtifactVersionRepository;
import edu.nd.crc.safa.server.repositories.artifacts.ProjectRetriever;
import edu.nd.crc.safa.server.repositories.documents.DocumentArtifactRepository;
import edu.nd.crc.safa.server.repositories.documents.DocumentRepository;
import edu.nd.crc.safa.server.repositories.projects.ProjectMembershipRepository;
import edu.nd.crc.safa.server.repositories.projects.ProjectRepository;
import edu.nd.crc.safa.server.repositories.projects.ProjectVersionRepository;
import edu.nd.crc.safa.server.repositories.projects.SafaUserRepository;
import edu.nd.crc.safa.server.repositories.traces.TraceLinkRepository;
import edu.nd.crc.safa.server.repositories.traces.TraceLinkVersionRepository;
import edu.nd.crc.safa.server.services.ProjectService;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.json.JSONObject;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.beans.factory.annotation.Autowired;

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
    protected ProjectRetriever artifactRepository;

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
    protected DocumentArtifactRepository documentArtifactRepository;

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

    ObjectMapper objectMapper = new ObjectMapper();

    @BeforeEach
    public void createNewBuilders() {
        dbEntityBuilder.createEmptyData();
        appBuilder.createEmptyData();
        jsonBuilder.createEmptyData();
    }

    public JSONObject toJson(Object object) throws JsonProcessingException {
        String objectJsonString = objectMapper.writeValueAsString(object);
        return new JSONObject(objectJsonString);
    }
}
