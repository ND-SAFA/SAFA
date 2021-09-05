package edu.nd.crc.safa.server.services;

import java.util.List;
import java.util.stream.Collectors;
import javax.transaction.Transactional;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.db.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.db.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.db.entities.app.TraceApplicationEntity;
import edu.nd.crc.safa.db.entities.sql.Artifact;
import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.db.repositories.sql.ArtifactBodyRepository;
import edu.nd.crc.safa.db.repositories.sql.ArtifactRepository;
import edu.nd.crc.safa.db.repositories.sql.ArtifactTypeRepository;
import edu.nd.crc.safa.db.repositories.sql.ParserErrorRepository;
import edu.nd.crc.safa.db.repositories.sql.ProjectRepository;
import edu.nd.crc.safa.db.repositories.sql.ProjectVersionRepository;
import edu.nd.crc.safa.db.repositories.sql.TraceLinkRepository;
import edu.nd.crc.safa.server.responses.ProjectCreationResponse;
import edu.nd.crc.safa.server.responses.ProjectErrors;
import edu.nd.crc.safa.server.responses.ServerError;
import edu.nd.crc.safa.utilities.OSHelper;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class ProjectService {
    /**
     * Responsible for all providing an API for performing the
     * business logic involved in ProjectsController.
     */
    ProjectRepository projectRepository;
    ProjectVersionRepository projectVersionRepository;
    ArtifactRepository artifactRepository;
    ArtifactTypeRepository artifactTypeRepository;
    ArtifactBodyRepository artifactBodyRepository;
    TraceLinkRepository traceLinkRepository;
    ParserErrorRepository parserErrorRepository;
    ParserErrorService parserErrorService;
    SynchronizeService synchronizeService;
    ArtifactService artifactService;
    TraceLinkService traceLinkService;

    @Autowired
    public ProjectService(ProjectRepository projectRepository,
                          ProjectVersionRepository projectVersionRepository,
                          ArtifactRepository artifactRepository,
                          ArtifactTypeRepository artifactTypeRepository,
                          ArtifactBodyRepository artifactBodyRepository,
                          TraceLinkRepository traceLinkRepository,
                          ParserErrorRepository parserErrorRepository,
                          ParserErrorService parserErrorService,
                          SynchronizeService synchronizeService,
                          ArtifactService artifactService,
                          TraceLinkService traceLinkService) {
        this.projectRepository = projectRepository;
        this.projectVersionRepository = projectVersionRepository;
        this.artifactRepository = artifactRepository;
        this.artifactTypeRepository = artifactTypeRepository;
        this.artifactBodyRepository = artifactBodyRepository;
        this.traceLinkRepository = traceLinkRepository;
        this.parserErrorRepository = parserErrorRepository;
        this.parserErrorService = parserErrorService;
        this.synchronizeService = synchronizeService;
        this.artifactService = artifactService;
        this.traceLinkService = traceLinkService;
    }

    @Transactional
    public ProjectCreationResponse createProject(ProjectAppEntity appEntity) {
        Project project = new Project(appEntity);
        this.projectRepository.save(project);
        ProjectVersion projectVersion = new ProjectVersion(project);
        this.projectVersionRepository.save(projectVersion);

        if (appEntity.artifacts != null) {
            artifactService.addNewArtifacts(appEntity.getArtifacts(), projectVersion);
        }

        if (appEntity.traces != null) {
            traceLinkService.createTraceLinks(appEntity.getTraces(), projectVersion);
        }

        ProjectAppEntity projectAppEntity = createApplicationEntity(projectVersion);
        ProjectErrors projectErrors = this.parserErrorService.collectionProjectErrors(projectVersion);
        return new ProjectCreationResponse(projectAppEntity, projectErrors);
    }

    @Transactional
    public ProjectCreationResponse updateProject(ProjectAppEntity appEntity) throws ServerError {
        Project project = new Project(appEntity);
        this.projectRepository.save(project);

        ProjectVersion newProjectVersion = new ProjectVersion(project);
        this.projectVersionRepository.save(newProjectVersion);

        List<Artifact> projectArtifacts = this.artifactRepository.findByProject(project);
        artifactService.updateExistingArtifacts(projectArtifacts, newProjectVersion, appEntity);
        List<ArtifactAppEntity> newArtifacts = appEntity.findNewArtifacts(projectArtifacts);
        artifactService.addNewArtifacts(newArtifacts, newProjectVersion);

        //TODO: Update trace links

        ProjectErrors projectErrors = this.parserErrorService.collectionProjectErrors(newProjectVersion);
        return new ProjectCreationResponse(appEntity, projectErrors); // TODO: Actually retrieve new object
    }

    public ProjectAppEntity createApplicationEntity(ProjectVersion newProjectVersion) {
        Project project = newProjectVersion.getProject();
        List<ArtifactAppEntity> artifacts = this.artifactBodyRepository
            .findByProjectVersion(newProjectVersion)
            .stream()
            .map(ArtifactAppEntity::new)
            .collect(Collectors.toList());
        List<TraceApplicationEntity> traces = this.traceLinkRepository
            .findByProject(project)
            .stream()
            .map(TraceApplicationEntity::new)
            .collect(Collectors.toList());
        return new ProjectAppEntity(project, artifacts, traces);
    }

    public void deleteProject(Project project) throws ServerError {
        this.projectRepository.delete(project);
        OSHelper.deletePath(ProjectPaths.getPathToStorage(project));
    }
}
