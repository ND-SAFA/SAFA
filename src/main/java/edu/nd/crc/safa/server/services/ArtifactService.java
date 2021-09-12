package edu.nd.crc.safa.server.services;

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

    @Autowired
    public ArtifactService(ArtifactRepository artifactRepository,
                           ArtifactTypeRepository artifactTypeRepository,
                           ArtifactBodyRepository artifactBodyRepository) {
        this.artifactRepository = artifactRepository;
        this.artifactTypeRepository = artifactTypeRepository;
        this.artifactBodyRepository = artifactBodyRepository;
    }

    public void createOrUpdateArtifacts(ProjectVersion projectVersion,
                                        List<ArtifactAppEntity> artifactsToUpdate) {
        for (ArtifactAppEntity a : artifactsToUpdate) {
            createOrUpdateArtifact(projectVersion, a);
        }
    }

    public Triplet<ArtifactType, Artifact, ArtifactBody> createOrUpdateArtifact(ProjectVersion projectVersion,
                                                                                ArtifactAppEntity a) {
        return createOrUpdateArtifact(projectVersion,
            a.name,
            a.type,
            a.summary,
            a.body);
    }

    /**
     * Returns the entities corresponding to artifact's type, body, and identifier within the project.
     *
     * @param projectVersion - The version that will be associated with the artifact's initial creation.
     * @param artifactName   - The artifact's unique name with given project.
     * @param typeName       - The name of the artifact's type (e.g. requirement).
     * @param summary        - Summary of the artifact's content. Can be null or empty string.
     * @param content        - The initial content of the artifact being saved.
     * @return Triplet of unsaved entities consisting of artifact's type, identifier, and initial body.
     */
    public Triplet<ArtifactType, Artifact, ArtifactBody> createOrUpdateArtifact(
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

        ArtifactBody artifactBody = createOrUpdateArtifactBody(projectVersion,
            artifact,
            new ArtifactAppEntity(typeName,
                artifactName,
                summary,
                content));
        if (artifactBody != null) {
            this.artifactBodyRepository.save(artifactBody);
        }

        return new Triplet<>(artifactType, artifact, artifactBody);
    }

    /**
     * Creates an artifact's body such that its modification type is calculated relative to the
     * last registered change. If not change is detected then the body is added as a new change.
     *
     * @param projectVersion - The version associated with the change created.
     * @param artifact       - The registered artifact in the project associated with the project version.
     * @param appEntity      - The artifact's new changes in the form of the domain model.
     * @return ArtifactBody - unsaved database entity with given changes and modification type.
     */
    private ArtifactBody createOrUpdateArtifactBody(ProjectVersion projectVersion,
                                                    Artifact artifact,
                                                    ArtifactAppEntity appEntity) {
        Project project = projectVersion.getProject();
        ArtifactBody artifactBody = null;
        if (appEntity == null) {
            artifactBody = new ArtifactBody(projectVersion,
                ModificationType.REMOVED,
                artifact,
                null,
                null);
        } else {
            Optional<ArtifactBody> previousBody = this.artifactBodyRepository.findLastArtifactBody(project, artifact);
            if (previousBody.isPresent()) {
                if (!previousBody.get().getContent().equals(appEntity.body)) {
                    artifactBody = new ArtifactBody(projectVersion,
                        ModificationType.MODIFIED,
                        artifact,
                        appEntity.summary,
                        appEntity.body);
                }
            } else {
                artifactBody = new ArtifactBody(projectVersion,
                    ModificationType.ADDED,
                    artifact,
                    appEntity.summary,
                    appEntity.body);
            }
        }
        if (artifactBody == null) {
            return null;
        } else {
            Optional<ArtifactBody> bodyQuery =
                this.artifactBodyRepository.findByProjectVersionAndArtifact(projectVersion, artifact);
            if (bodyQuery.isPresent()) {
                artifactBody.setArtifactBodyId(bodyQuery.get().getArtifactBodyId());
            }
            return artifactBody;
        }
    }
}
