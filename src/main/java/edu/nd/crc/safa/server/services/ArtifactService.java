package edu.nd.crc.safa.server.services;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.Optional;

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

import org.javatuples.Triplet;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class ArtifactService {

    ArtifactRepository artifactRepository;
    ArtifactTypeRepository artifactTypeRepository;
    ArtifactBodyRepository artifactBodyRepository;

    DeltaService deltaService;

    @Autowired
    public ArtifactService(ArtifactRepository artifactRepository,
                           ArtifactTypeRepository artifactTypeRepository,
                           ArtifactBodyRepository artifactBodyRepository,
                           DeltaService deltaService) {
        this.artifactRepository = artifactRepository;
        this.artifactTypeRepository = artifactTypeRepository;
        this.artifactBodyRepository = artifactBodyRepository;
        this.deltaService = deltaService;
    }

    public void createOrUpdateArtifacts(ProjectVersion projectVersion,
                                        List<ArtifactAppEntity> artifactsToUpdate) {
        Hashtable<String, ArtifactAppEntity> entitiesSeen = new Hashtable<>();
        for (ArtifactAppEntity a : artifactsToUpdate) {
            createOrUpdateArtifact(projectVersion,
                a.name,
                a.type,
                a.summary,
                a.body);
            entitiesSeen.put(a.getName(), a);
        }

        for (Artifact projectArtifact : this.artifactRepository.findByProject(projectVersion.getProject())) {
            if (entitiesSeen.containsKey(projectArtifact.getName())) {
                continue;
            }
            ArtifactBody removedBody = deltaService.calculateArtifactChange(projectVersion, projectArtifact, null);
            this.artifactBodyRepository.save(removedBody);
        }
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
    private void createOrUpdateArtifact(
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

        ArtifactBody artifactBody = deltaService.calculateArtifactChange(projectVersion,
            artifact,
            new ArtifactAppEntity(typeName,
                artifactName,
                summary,
                content));

        if (artifactBody != null) {
            this.artifactBodyRepository.save(artifactBody);
        }

        new Triplet<>(artifactType, artifact, artifactBody);
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
