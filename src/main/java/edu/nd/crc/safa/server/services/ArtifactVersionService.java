package edu.nd.crc.safa.server.services;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.AppConstraints;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.api.ServerResponse;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.ModificationType;
import edu.nd.crc.safa.server.entities.db.ParserError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectParsingActivities;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.server.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.server.repositories.ParserErrorRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.stereotype.Service;

/**
 * Responsible for providing an interface to modify artifacts in a project by calculating
 * and storing their changes between the previous version.
 *
 * @author Alberto Rodriguez
 */
@Service
public class ArtifactVersionService {

    ArtifactRepository artifactRepository;
    ArtifactTypeRepository artifactTypeRepository;
    ArtifactVersionRepository artifactVersionRepository;
    ProjectVersionRepository projectVersionRepository;
    ParserErrorRepository parserErrorRepository;

    DeltaService deltaService;

    @Autowired
    public ArtifactVersionService(ArtifactRepository artifactRepository,
                                  ArtifactTypeRepository artifactTypeRepository,
                                  ArtifactVersionRepository artifactVersionRepository,
                                  ProjectVersionRepository projectVersionRepository,
                                  ParserErrorRepository parserErrorRepository,
                                  DeltaService deltaService) {
        this.artifactRepository = artifactRepository;
        this.artifactTypeRepository = artifactTypeRepository;
        this.artifactVersionRepository = artifactVersionRepository;
        this.projectVersionRepository = projectVersionRepository;
        this.parserErrorRepository = parserErrorRepository;
        this.deltaService = deltaService;
    }

    /**
     * Calculates the changes in each artifact body from the previous versions and stores
     * changes at given ProjectVersion.
     *
     * @param projectVersion   The ProjectVersion associated with calculated artifact changes.
     * @param projectArtifacts List of artifact's in a project whose version will be stored.
     * @throws SafaError Throws error if any database related errors arise during saving the new artifacts/
     */
    public void setArtifactsAtVersion(ProjectVersion projectVersion,
                                      List<ArtifactAppEntity> projectArtifacts) throws SafaError {
        List<ArtifactVersion> allArtifactBodies = calculateArtifactBodiesAtVersion(projectVersion, projectArtifacts);
        for (ArtifactVersion body : allArtifactBodies) {
            saveArtifactBody(body);
        }
    }

    /**
     * Calculates changes between previous artifact versions and stores them at given project version.
     *
     * @param projectVersion The ProjectVersion containing given version of artifact.
     * @param artifact       The artifact at a given versions which is being stored.
     * @throws SafaError Throws an error is saving entity violates any Database Constraints
     */
    public void setArtifactAtProjectVersion(ProjectVersion projectVersion, ArtifactAppEntity artifact)
        throws SafaError {
        ArtifactVersion artifactVersion = calculateArtifactBodyAtVersion(projectVersion,
            artifact.id,
            artifact.name,
            artifact.type,
            artifact.summary,
            artifact.body);
        if (artifactVersion == null) {
            return;
        }
        saveArtifactBody(artifactVersion);
    }

    /**
     * Deletes artifact with given name within given project.
     *
     * @param projectVersion The version to record the deletion happening in.
     * @param artifactName   The name of the artifact to be deleted.
     * @return ServerResponse with success message.
     */
    public ServerResponse deleteArtifactBody(
        ProjectVersion projectVersion,
        String artifactName) {
        Optional<ArtifactVersion> bodyToRemove = this.artifactVersionRepository.findByProjectVersionAndArtifactName(projectVersion,
            artifactName);
        bodyToRemove.ifPresentOrElse(artifactBody -> {
            artifactBody.setModificationType(ModificationType.REMOVED);
            artifactBody.setSummary("");
            artifactBody.setContent("");
            this.artifactVersionRepository.save(artifactBody);
        }, () -> {
            Project project = projectVersion.getProject();
            Optional<Artifact> artifactQuery = this.artifactRepository.findByProjectAndName(project, artifactName);
            artifactQuery.ifPresent((artifact -> {
                ArtifactVersion artifactVersion = new ArtifactVersion(
                    projectVersion,
                    ModificationType.REMOVED,
                    artifact,
                    "", "");
                this.artifactVersionRepository.save(artifactVersion);
            }));
        });
        return new ServerResponse(String.format("%s successfully deleted.", artifactName));
    }


    private List<ArtifactVersion> calculateArtifactBodiesAtVersion(
        ProjectVersion projectVersion,
        List<ArtifactAppEntity> projectArtifacts) throws SafaError {
        Hashtable<String, ArtifactAppEntity> artifactsUpdated = new Hashtable<>();
        List<ArtifactVersion> updatedArtifactBodies = new ArrayList<>();
        for (ArtifactAppEntity a : projectArtifacts) {
            artifactsUpdated.put(a.getName(), a);
            try {
                ArtifactVersion artifactVersion = calculateArtifactBodyAtVersion(projectVersion,
                    a.getId(),
                    a.name,
                    a.type,
                    a.summary,
                    a.body);
                updatedArtifactBodies.add(artifactVersion);
            } catch (DataIntegrityViolationException e) {
                ParserError parserError = new ParserError(
                    projectVersion,
                    "Could not parse artifact " + a.getName() + ": " + AppConstraints.getConstraintError(e),
                    ProjectParsingActivities.PARSING_ARTIFACTS);
                this.parserErrorRepository.save(parserError);

            }
        }
        updatedArtifactBodies = updatedArtifactBodies
            .stream()
            .filter(Objects::nonNull)
            .collect(Collectors.toList());

        List<ArtifactVersion> removedArtifactBodies = this.artifactRepository
            .getProjectArtifacts(projectVersion.getProject())
            .stream()
            .filter(a -> !artifactsUpdated.containsKey(a.getName()))
            .map(a -> deltaService.calculateArtifactChange(projectVersion, a, null))
            .filter(Objects::nonNull)
            .collect(Collectors.toList());

        List<ArtifactVersion> allArtifactBodies = new ArrayList<>(updatedArtifactBodies);
        allArtifactBodies.addAll(removedArtifactBodies);
        return allArtifactBodies;
    }

    private ArtifactVersion calculateArtifactBodyAtVersion(
        ProjectVersion projectVersion,
        String artifactId,
        String artifactName,
        String typeName,
        String summary,
        String content) throws SafaError {

        Project project = projectVersion.getProject();
        Optional<ArtifactType> artifactTypeQuery = this.artifactTypeRepository
            .findByProjectAndNameIgnoreCase(project, typeName);
        ArtifactType artifactType = artifactTypeQuery.orElseGet(() -> new ArtifactType(project, typeName));
        this.artifactTypeRepository.save(artifactType);
        Artifact artifact;

        if (artifactId == null || artifactId.equals("")) {
            artifact = new Artifact(project, artifactType, artifactName);
        } else {
            Optional<Artifact> artifactQuery = this.artifactRepository.findById(UUID.fromString(artifactId));
            if (artifactQuery.isPresent()) {
                artifact = artifactQuery.get();
                artifact.setType(artifactType);
                artifact.setName(artifactName);
            } else {
                throw new RuntimeException("Could not find artifact with id:" + artifactId);
            }
        }
        this.artifactRepository.save(artifact);

        return deltaService.calculateArtifactChange(projectVersion,
            artifact,
            new ArtifactAppEntity(
                artifactId,
                typeName,
                artifactName,
                summary,
                content));
    }
    
    private void saveArtifactBody(ArtifactVersion artifactVersion) throws SafaError {
        try {
            this.artifactVersionRepository.save(artifactVersion);
        } catch (Exception e) {
            String error = String.format("An error occurred while saving artifact: %s", artifactVersion.getName());
            throw new SafaError(error, e);
        }
    }
}
