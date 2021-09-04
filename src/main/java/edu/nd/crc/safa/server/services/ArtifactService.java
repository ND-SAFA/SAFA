package edu.nd.crc.safa.server.services;

import java.util.Optional;

import edu.nd.crc.safa.db.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.db.entities.sql.Artifact;
import edu.nd.crc.safa.db.entities.sql.ArtifactBody;
import edu.nd.crc.safa.db.entities.sql.ArtifactType;
import edu.nd.crc.safa.db.entities.sql.ModificationType;
import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.db.repositories.sql.ArtifactBodyRepository;
import edu.nd.crc.safa.db.repositories.sql.ArtifactRepository;
import edu.nd.crc.safa.db.repositories.sql.ArtifactTypeRepository;
import edu.nd.crc.safa.server.responses.ServerError;

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

    public ArtifactBody updateArtifactBody(ProjectVersion projectVersion,
                                           Artifact artifact,
                                           ArtifactAppEntity appEntity) throws ServerError {
        ArtifactBody body;
        Project project = projectVersion.getProject();
        this.artifactBodyRepository.findLastArtifactBody(project, artifact);

        if (appEntity == null) {
            return new ArtifactBody(projectVersion,
                ModificationType.REMOVED,
                artifact,
                null,
                null);
        } else {
            Optional<ArtifactBody> previousBody = this.artifactBodyRepository.findLastArtifactBody(project, artifact);
            if (previousBody.isPresent()) {
                if (!previousBody.get().getContent().equals(appEntity.body)) {
                    return new ArtifactBody(projectVersion,
                        ModificationType.MODIFIED,
                        artifact,
                        appEntity.summary,
                        appEntity.body);
                } else {
                    return null; // No change
                }
            } else {
                String errorMessage = String.format("%s was created but contains no body.");
                throw new ServerError(errorMessage);
            }
        }
    }

    public Triplet<ArtifactType, Artifact, ArtifactBody> createArtifact(ProjectVersion projectVersion,
                                                                        ArtifactAppEntity a) {
        //TODO: Return object and save in batch
        Project project = projectVersion.getProject();
        Optional<ArtifactType> artifactTypeQuery = this.artifactTypeRepository
            .findByProjectAndNameIgnoreCase(project, a.getType());
        ArtifactType artifactType;
        if (!artifactTypeQuery.isPresent()) {
            artifactType = new ArtifactType(project, a.getType());
            this.artifactTypeRepository.save(artifactType);
        } else {
            artifactType = artifactTypeQuery.get();
        }

        Optional<Artifact> artifactQuery = this.artifactRepository.findByProjectAndName(project, a.getName());
        Artifact artifact = artifactQuery.orElseGet(() -> new Artifact(project, artifactType, a.getName()));
        this.artifactRepository.save(artifact);
        ArtifactBody artifacyBody = new ArtifactBody(projectVersion, ModificationType.ADDED, artifact, a.summary, a.body);
        this.artifactBodyRepository.save(artifacyBody);
        return new Triplet<>(artifactType, artifact, artifacyBody);
    }
}
