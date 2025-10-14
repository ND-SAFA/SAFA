package edu.nd.crc.safa.test.common;

import edu.nd.crc.safa.features.artifacts.repositories.ArtifactRepository;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactVersionRepositoryImpl;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.documents.repositories.DocumentArtifactRepository;
import edu.nd.crc.safa.features.documents.repositories.DocumentRepository;
import edu.nd.crc.safa.features.email.services.EmailService;
import edu.nd.crc.safa.features.errors.repositories.CommitErrorRepository;
import edu.nd.crc.safa.features.flatfiles.services.FileUploadService;
import edu.nd.crc.safa.features.jobs.services.JobService;
import edu.nd.crc.safa.features.projects.repositories.ProjectRepository;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.traces.repositories.TraceLinkRepository;
import edu.nd.crc.safa.features.traces.repositories.TraceLinkVersionRepository;
import edu.nd.crc.safa.features.types.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.features.users.repositories.SafaUserRepository;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.features.versions.repositories.ProjectVersionRepository;

import lombok.Getter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.mock.mockito.MockBean;

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
    protected DocumentRepository documentRepository;

    @Autowired
    protected DocumentArtifactRepository documentArtifactRepository;

    @Autowired
    protected ProjectService projectService;

    @Autowired
    protected SafaUserService safaUserService;

    @Autowired
    protected JobService jobService;

    @Autowired
    @Getter
    protected ServiceProvider serviceProvider;

    @Autowired
    protected ArtifactVersionRepositoryImpl artifactVersionRepositoryImpl;

    @MockBean
    protected EmailService emailService;

}
