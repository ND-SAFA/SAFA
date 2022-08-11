package features.base;

import edu.nd.crc.safa.authentication.SafaUserService;
import edu.nd.crc.safa.builders.JsonBuilder;
import edu.nd.crc.safa.builders.entities.DbEntityBuilder;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactRepository;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.features.artifacts.repositories.FTAArtifactRepository;
import edu.nd.crc.safa.features.artifacts.repositories.SafetyCaseArtifactRepository;
import edu.nd.crc.safa.features.documents.repositories.DocumentArtifactRepository;
import edu.nd.crc.safa.features.documents.repositories.DocumentRepository;
import edu.nd.crc.safa.features.errors.repositories.CommitErrorRepository;
import edu.nd.crc.safa.features.flatfiles.services.FileUploadService;
import edu.nd.crc.safa.features.projects.repositories.ProjectRepository;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.traces.repositories.TraceLinkRepository;
import edu.nd.crc.safa.features.traces.repositories.TraceLinkVersionRepository;
import edu.nd.crc.safa.features.users.repositories.ProjectMembershipRepository;
import edu.nd.crc.safa.features.users.repositories.SafaUserRepository;
import edu.nd.crc.safa.features.versions.repositories.ProjectVersionRepository;

import com.fasterxml.jackson.databind.ObjectMapper;
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
    protected DocumentArtifactRepository documentArtifactRepository;

    @Autowired
    protected ProjectService projectService;

    @Autowired
    protected SafaUserService safaUserService;

    @Autowired
    protected DbEntityBuilder dbEntityBuilder;

    @Autowired
    protected JsonBuilder jsonBuilder;

    @Autowired
    protected SafetyCaseArtifactRepository safetyCaseArtifactRepository;

    @Autowired
    protected FTAArtifactRepository ftaArtifactRepository;

    ObjectMapper objectMapper = new ObjectMapper();

    @BeforeEach
    public void createNewBuilders() {
        dbEntityBuilder.createEmptyData();
        jsonBuilder.createEmptyData();
    }
}
