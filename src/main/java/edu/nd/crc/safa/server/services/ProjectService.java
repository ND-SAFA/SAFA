package edu.nd.crc.safa.server.services;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import javax.transaction.Transactional;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.db.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.db.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.db.entities.app.TraceApplicationEntity;
import edu.nd.crc.safa.db.entities.sql.Artifact;
import edu.nd.crc.safa.db.entities.sql.ArtifactBody;
import edu.nd.crc.safa.db.entities.sql.ArtifactType;
import edu.nd.crc.safa.db.entities.sql.ParserError;
import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.db.entities.sql.TraceLink;
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

import org.javatuples.Pair;
import org.javatuples.Triplet;
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

    public void deleteProject(Project project) throws ServerError {
        this.projectRepository.delete(project);
        OSHelper.deletePath(ProjectPaths.getPathToStorage(project));
    }

    @Transactional
    public ProjectCreationResponse createOrUpdateProject(ProjectAppEntity appEntity) throws ServerError {
        if (appEntity.projectId != null && !appEntity.projectId.equals("")) {
            return updateProject(appEntity);
        }
        Project project = new Project(appEntity);
        this.projectRepository.save(project);
        ProjectVersion projectVersion = new ProjectVersion(project);
        this.projectVersionRepository.save(projectVersion);

        List<ArtifactType> artifactTypes = new ArrayList<>();
        List<Artifact> artifacts = new ArrayList<>();
        List<ArtifactBody> artifactBodies = new ArrayList<>();
        if (appEntity.artifacts != null) {
            appEntity
                .getArtifacts()
                .forEach(a -> {
                    Triplet<ArtifactType, Artifact, ArtifactBody> result =
                        artifactService.createArtifact(projectVersion,
                            a);
                    artifactTypes.add(result.getValue0());
                    artifacts.add(result.getValue1());
                    artifactBodies.add(result.getValue2());
                });
        }
        this.artifactTypeRepository.saveAll(artifactTypes);
        this.artifactRepository.saveAll(artifacts);
        this.artifactBodyRepository.saveAll(artifactBodies);

        List<TraceLink> newLinks = new ArrayList<>();
        List<ParserError> newErrors = new ArrayList<>();
        if (appEntity.traces != null) {
            appEntity
                .getTraces()
                .forEach(t -> {
                    Pair<TraceLink, ParserError> result = traceLinkService.createTrace(projectVersion, t);
                    if (result.getValue0() != null) {
                        newLinks.add(result.getValue0());
                    }
                    if (result.getValue1() != null) {
                        newErrors.add(result.getValue1());
                    }
                });
        }
        this.traceLinkRepository.saveAll(newLinks);
        this.parserErrorRepository.saveAll(newErrors);

        ProjectAppEntity projectAppEntity = createApplicationEntity(projectVersion);
        ProjectErrors projectErrors = this.parserErrorService.collectionProjectErrors(projectVersion);
        return new ProjectCreationResponse(projectAppEntity, projectErrors);
    }

    public ProjectCreationResponse updateProject(ProjectAppEntity appEntity) throws ServerError {
        Project project = new Project(appEntity);
        this.projectRepository.save(project);
        ProjectVersion projectVersion = new ProjectVersion(project);
        this.projectVersionRepository.save(projectVersion);
        List<Artifact> projectArtifacts = this.artifactRepository.findByProject(project);
        List<ArtifactBody> newBodies = new ArrayList<>();
        for (Artifact artifact : projectArtifacts) {
            String artifactName = artifact.getName();
            ArtifactAppEntity artifactApp = appEntity.getArtifactWithId(artifactName);
            ArtifactBody newBody = artifactService.updateArtifactBody(projectVersion, artifact, artifactApp);
            if (newBody != null) {
                newBodies.add(newBody);
            }
        }
        this.artifactBodyRepository.saveAll(newBodies);

        List<ArtifactType> potentiallyNewArtifactTypes = new ArrayList<>();
        List<Artifact> newArtifacts = new ArrayList<>();
        List<ArtifactBody> newArtifactBodies = new ArrayList<>();
        for (ArtifactAppEntity artifactAppEntity : appEntity.getNewArtifacts(projectArtifacts)) {
            Triplet<ArtifactType, Artifact, ArtifactBody> result = artifactService.createArtifact(projectVersion,
                artifactAppEntity);
            potentiallyNewArtifactTypes.add(result.getValue0());
            newArtifacts.add(result.getValue1());
            newArtifactBodies.add(result.getValue2());
            System.out.println("New Body Id:" + result.getValue2().getName());
        }
        this.artifactTypeRepository.saveAll(potentiallyNewArtifactTypes);
        this.artifactRepository.saveAll(newArtifacts);
        this.artifactBodyRepository.saveAll(newArtifactBodies);

        ProjectErrors projectErrors = this.parserErrorService.collectionProjectErrors(projectVersion);
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
}
