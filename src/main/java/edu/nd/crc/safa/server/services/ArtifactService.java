package edu.nd.crc.safa.server.services;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Collectors;

import edu.nd.crc.safa.server.db.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.db.entities.sql.Artifact;
import edu.nd.crc.safa.server.db.entities.sql.ArtifactBody;
import edu.nd.crc.safa.server.db.entities.sql.ArtifactType;
import edu.nd.crc.safa.server.db.entities.sql.ModificationType;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.db.repositories.ArtifactBodyRepository;
import edu.nd.crc.safa.server.db.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.db.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.server.messages.ServerError;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class ArtifactService {

    ArtifactRepository artifactRepository;
    ArtifactTypeRepository artifactTypeRepository;
    ArtifactBodyRepository artifactBodyRepository;
    DeltaService deltaService;
    RevisionNotificationService revisionNotificationService;

    @Autowired
    public ArtifactService(ArtifactRepository artifactRepository,
                           ArtifactTypeRepository artifactTypeRepository,
                           ArtifactBodyRepository artifactBodyRepository,
                           DeltaService deltaService,
                           RevisionNotificationService revisionNotificationService) {
        this.artifactRepository = artifactRepository;
        this.artifactTypeRepository = artifactTypeRepository;
        this.artifactBodyRepository = artifactBodyRepository;
        this.deltaService = deltaService;
        this.revisionNotificationService = revisionNotificationService;
    }

    public void setArtifactsAtVersion(ProjectVersion projectVersion,
                                      List<ArtifactAppEntity> artifactsToUpdate) throws ServerError {
        Hashtable<String, ArtifactAppEntity> entitiesSeen = new Hashtable<>();
        List<ArtifactBody> artifactBodies = artifactsToUpdate
            .stream()
            .map(a -> {
                entitiesSeen.put(a.getName(), a);
                return createArtifactBodyAtVersion(projectVersion,
                    a.name,
                    a.type,
                    a.summary,
                    a.body);
            })
            .filter(Objects::nonNull)
            .collect(Collectors.toList());

        List<ArtifactBody> removedBodies = this.artifactRepository
            .findByProject(projectVersion.getProject())
            .stream()
            .filter(a -> !entitiesSeen.containsKey(a.getName()))
            .map(a -> deltaService.calculateArtifactChange(projectVersion, a, null))
            .filter(Objects::nonNull)
            .collect(Collectors.toList());

        List<ArtifactBody> allArtifactBodies = new ArrayList<>(artifactBodies);
        allArtifactBodies.addAll(removedBodies);
        this.artifactBodyRepository.saveAll(allArtifactBodies);
    }

    public void addArtifactToVersion(ProjectVersion projectVersion, ArtifactAppEntity a) throws ServerError {
        ArtifactBody artifactBody = createArtifactBodyAtVersion(projectVersion,
            a.name,
            a.type,
            a.summary,
            a.body);
        if (artifactBody == null) {
            return;
        }
        this.artifactBodyRepository.save(artifactBody);
    }

    /**
     * Returns the entities corresponding to artifact's type, body, and identifier within the project.
     *
     * @param projectVersion - The version that will be associated with the artifact's initial creation.
     * @param artifactName   - The artifact's unique name with given project.
     * @param typeName       - The name of the artifact's type (e.g. requirement).
     * @param summary        - Summary of the artifact's content. Can be null or empty string.
     * @param content        - The initial content of the artifact being saved.
     */
    private ArtifactBody createArtifactBodyAtVersion(
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

    /**
     * Returns a list of ArtifactBody for each artifact in given project such that
     * the ArtifactBody represents the artifact at the version indicated.
     *
     * @param projectVersion - The version of the artifact bodies that are returned
     * @return list of artifact bodies in project at given version
     */
    public List<ArtifactBody> getArtifactBodiesAtVersion(ProjectVersion projectVersion) {
        List<ArtifactBody> artifacts = new ArrayList<>();
        Hashtable<String, List<ArtifactBody>> artifactBodyTable = new Hashtable<>();
        List<ArtifactBody> projectBodies = this.artifactBodyRepository.findByProject(projectVersion.getProject());
        for (ArtifactBody body : projectBodies) {
            String key = body.getArtifact().getArtifactId().toString();
            if (artifactBodyTable.containsKey(key)) {
                artifactBodyTable.get(key).add(body);
            } else {
                List<ArtifactBody> newList = new ArrayList<>();
                newList.add(body);
                artifactBodyTable.put(key, newList);
            }
        }

        for (String key : artifactBodyTable.keySet()) {
            List<ArtifactBody> bodyVersions = artifactBodyTable.get(key);
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
}
