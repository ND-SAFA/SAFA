package edu.nd.crc.safa.server.services;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.server.entities.api.ServerError;
import edu.nd.crc.safa.server.entities.api.ServerResponse;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactBody;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.ModificationType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ArtifactBodyRepository;
import edu.nd.crc.safa.server.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;

import org.springframework.beans.factory.annotation.Autowired;
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
    ArtifactBodyRepository artifactBodyRepository;
    ProjectVersionRepository projectVersionRepository;

    DeltaService deltaService;

    @Autowired
    public ArtifactVersionService(ArtifactRepository artifactRepository,
                                  ArtifactTypeRepository artifactTypeRepository,
                                  ArtifactBodyRepository artifactBodyRepository,
                                  ProjectVersionRepository projectVersionRepository,
                                  DeltaService deltaService) {
        this.artifactRepository = artifactRepository;
        this.artifactTypeRepository = artifactTypeRepository;
        this.artifactBodyRepository = artifactBodyRepository;
        this.projectVersionRepository = projectVersionRepository;
        this.deltaService = deltaService;
    }

    /**
     * Calculates contents of each artifact at given version and returns bodies at version.
     *
     * @param projectVersion - The version of the artifact bodies that are returned
     * @return list of artifact bodies in project at given version
     */
    public List<ArtifactBody> getArtifactBodiesAtVersion(ProjectVersion projectVersion) {
        Hashtable<String, List<ArtifactBody>> artifactBodyTable =
            groupProjectArtifactBodiesByArtifactName(projectVersion);
        return calculateArtifactBodiesAtProjectVersion(projectVersion, artifactBodyTable);
    }

    /**
     * Calculates the changes in each artifact body from the previous versions and stores
     * changes at given ProjectVersion.
     *
     * @param projectVersion   The ProjectVersion associated with calculated artifact changes.
     * @param projectArtifacts List of artifact's in a project whose version will be stored.
     * @throws ServerError Throws error if any database related errors arise during saving the new artifacts/
     */
    public void setArtifactsAtVersion(ProjectVersion projectVersion,
                                      List<ArtifactAppEntity> projectArtifacts) throws ServerError {
        List<ArtifactBody> allArtifactBodies = calculateArtifactBodiesAtVersion(projectVersion, projectArtifacts);
        for (ArtifactBody body : allArtifactBodies) {
            saveArtifactBody(body);
        }
    }

    /**
     * Calculates changes between previous artifact versions and stores them at given project version.
     *
     * @param projectVersion The ProjectVersion containing given version of artifact.
     * @param artifact       The artifact at a given versions which is being stored.
     * @throws ServerError Throws an error is saving entity violates any Database Constraints
     */
    public void setArtifactAtProjectVersion(ProjectVersion projectVersion, ArtifactAppEntity artifact)
        throws ServerError {
        ArtifactBody artifactBody = calculateArtifactBodyAtVersion(projectVersion,
            artifact.name,
            artifact.type,
            artifact.summary,
            artifact.body);
        if (artifactBody == null) {
            return;
        }
        saveArtifactBody(artifactBody);
    }

    /**
     * Deletes artifact with given name within given project.
     *
     * @param versionId    UUID of versionId of associated project version.
     * @param artifactName The name of the artifact to be deleted.
     * @return ServerResponse with success message.
     */
    public ServerResponse deleteArtifactBody(
        UUID versionId,
        String artifactName) {
        ProjectVersion projectVersion = this.projectVersionRepository.findByVersionId(versionId);
        Optional<ArtifactBody> bodyToRemove = this.artifactBodyRepository.findByProjectVersionAndArtifactName(projectVersion,
            artifactName);
        bodyToRemove.ifPresentOrElse(artifactBody -> {
            artifactBody.setModificationType(ModificationType.REMOVED);
            artifactBody.setSummary("");
            artifactBody.setContent("");
            this.artifactBodyRepository.save(artifactBody);
        }, () -> {
            Project project = projectVersion.getProject();
            Optional<Artifact> artifactQuery = this.artifactRepository.findByProjectAndName(project, artifactName);
            artifactQuery.ifPresent((artifact -> {
                ArtifactBody artifactBody = new ArtifactBody(
                    projectVersion,
                    ModificationType.REMOVED,
                    artifact,
                    "", "");
                this.artifactBodyRepository.save(artifactBody);
            }));
        });
        return new ServerResponse(String.format("%s successfully deleted.", artifactName));
    }

    private List<ArtifactBody> calculateArtifactBodiesAtProjectVersion(
        ProjectVersion projectVersion,
        Hashtable<String, List<ArtifactBody>> artifactBodiesByArtifactName) {
        List<ArtifactBody> artifacts = new ArrayList<>();
        for (String key : artifactBodiesByArtifactName.keySet()) {
            List<ArtifactBody> bodyVersions = artifactBodiesByArtifactName.get(key);
            ArtifactBody latest = null;
            for (ArtifactBody body : bodyVersions) {
                if (body.getProjectVersion().isLessThanOrEqualTo(projectVersion)) {
                    if (latest == null || body.getProjectVersion().isGreaterThan(latest.getProjectVersion())) {
                        latest = body;
                    }
                }
            }

            if (latest != null && latest.getModificationType() != ModificationType.REMOVED) {
                artifacts.add(latest);
            }
        }
        return artifacts;
    }

    private List<ArtifactBody> calculateArtifactBodiesAtVersion(
        ProjectVersion projectVersion,
        List<ArtifactAppEntity> projectArtifacts) {
        Hashtable<String, ArtifactAppEntity> artifactsUpdated = new Hashtable<>();
        List<ArtifactBody> updatedArtifactBodies = projectArtifacts
            .stream()
            .map(a -> {
                artifactsUpdated.put(a.getName(), a);
                return calculateArtifactBodyAtVersion(projectVersion,
                    a.name,
                    a.type,
                    a.summary,
                    a.body);
            })
            .filter(Objects::nonNull)
            .collect(Collectors.toList());

        List<ArtifactBody> removedArtifactBodies = this.artifactRepository
            .getProjectArtifacts(projectVersion.getProject())
            .stream()
            .filter(a -> !artifactsUpdated.containsKey(a.getName()))
            .map(a -> deltaService.calculateArtifactChange(projectVersion, a, null))
            .filter(Objects::nonNull)
            .collect(Collectors.toList());

        List<ArtifactBody> allArtifactBodies = new ArrayList<>(updatedArtifactBodies);
        allArtifactBodies.addAll(removedArtifactBodies);
        return allArtifactBodies;
    }

    private ArtifactBody calculateArtifactBodyAtVersion(
        ProjectVersion projectVersion,
        String artifactName,
        String typeName,
        String summary,
        String content) {

        Project project = projectVersion.getProject();
        Optional<ArtifactType> artifactTypeQuery = this.artifactTypeRepository
            .findByProjectAndNameIgnoreCase(project, typeName);
        ArtifactType artifactType = artifactTypeQuery.orElseGet(() -> new ArtifactType(project, typeName));
        this.artifactTypeRepository.save(artifactType);

        Optional<Artifact> artifactQuery = this.artifactRepository.findByProjectAndName(project, artifactName);
        Artifact artifact = artifactQuery.orElseGet(() -> new Artifact(project, artifactType, artifactName));
        this.artifactRepository.save(artifact);

        return deltaService.calculateArtifactChange(projectVersion,
            artifact,
            new ArtifactAppEntity(typeName,
                artifactName,
                summary,
                content));
    }

    private Hashtable<String, List<ArtifactBody>> groupProjectArtifactBodiesByArtifactName(
        ProjectVersion projectVersion) {
        Hashtable<String, List<ArtifactBody>> artifactBodyTable = new Hashtable<>();
        List<ArtifactBody> projectBodies = this.artifactBodyRepository.findByProject(projectVersion.getProject());
        for (ArtifactBody body : projectBodies) {
            String artifactId = body.getArtifact().getArtifactId().toString();
            if (artifactBodyTable.containsKey(artifactId)) {
                artifactBodyTable.get(artifactId).add(body);
            } else {
                List<ArtifactBody> newList = new ArrayList<>();
                newList.add(body);
                artifactBodyTable.put(artifactId, newList);
            }
        }
        return artifactBodyTable;
    }

    private void saveArtifactBody(ArtifactBody artifactBody) throws ServerError {
        try {
            this.artifactBodyRepository.save(artifactBody);
        } catch (Exception e) {
            String error = String.format("An error occurred while saving artifact: %s", artifactBody.getName());
            throw new ServerError(error, e);
        }
    }
}
