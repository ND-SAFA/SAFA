package edu.nd.crc.safa.server.services;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;

import edu.nd.crc.safa.server.entities.app.AddedArtifact;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.DeltaArtifact;
import edu.nd.crc.safa.server.entities.app.ModifiedArtifact;
import edu.nd.crc.safa.server.entities.app.ProjectDelta;
import edu.nd.crc.safa.server.entities.app.RemovedArtifact;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.ModificationType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Responsible for calculating the delta between any two versions.
 */
@Service
public class DeltaService {

    ProjectVersionRepository projectVersionRepository;
    ArtifactRepository artifactRepository;
    ArtifactVersionRepository artifactVersionRepository;

    @Autowired
    public DeltaService(ProjectVersionRepository projectVersionRepository,
                        ArtifactRepository artifactRepository,
                        ArtifactVersionRepository artifactVersionRepository) {
        this.projectVersionRepository = projectVersionRepository;
        this.artifactRepository = artifactRepository;
        this.artifactVersionRepository = artifactVersionRepository;
    }

    /**
     * Calculates artifacts removed, added, and modified between given versions.
     *
     * @param baselineVersion The version whose entities will be held as the baseline.
     * @param targetVersion   The version whose entities will be compared to baseline entities.
     * @return ProjectDelta summarizing changes between versions.
     */
    public ProjectDelta calculateProjectDelta(ProjectVersion baselineVersion, ProjectVersion targetVersion) {

        Project project = baselineVersion.getProject();

        Hashtable<String, AddedArtifact> added = new Hashtable<>();
        Hashtable<String, ModifiedArtifact> modified = new Hashtable<>();
        Hashtable<String, RemovedArtifact> removed = new Hashtable<>();

        List<Artifact> projectArtifacts = this.artifactRepository.getProjectArtifacts(project);
        List<ArtifactAppEntity> missingArtifacts = new ArrayList<>();

        for (Artifact artifact : projectArtifacts) {
            DeltaArtifact deltaArtifact = calculateArtifactModificationBetweenVersions(
                artifact,
                baselineVersion,
                targetVersion);
            if (deltaArtifact == null) {
                continue;
            }
            String deltaArtifactId = deltaArtifact.getArtifactId();
            if (deltaArtifact instanceof ModifiedArtifact) {
                modified.put(deltaArtifactId, (ModifiedArtifact) deltaArtifact);
            } else if (deltaArtifact instanceof RemovedArtifact) {
                removed.put(deltaArtifactId, (RemovedArtifact) deltaArtifact);
            } else if (deltaArtifact instanceof AddedArtifact) {
                added.put(deltaArtifactId, (AddedArtifact) deltaArtifact);
                String typeName = artifact.getType().getName();
                String artifactId = artifact.getArtifactId().toString();
                String artifactName = artifact.getName();
                String summary = ((AddedArtifact) deltaArtifact).getAfterSummary();
                String body = ((AddedArtifact) deltaArtifact).getAfter();
                ArtifactAppEntity addedArtifactBody = new ArtifactAppEntity(
                    artifactId,
                    typeName,
                    artifactName,
                    summary,
                    body);
                missingArtifacts.add(addedArtifactBody);
            }
        }

        return new ProjectDelta(added, modified, removed, missingArtifacts);
    }

    /**
     * Creates an artifact's body such that its modification type is calculated relative to the
     * last registered change. If not change is detected then the body is added as a new change.
     *
     * @param projectVersion - The version associated with the change created.
     * @param artifact       - The registered artifact in the project associated with the project version.
     * @param appEntity      - The artifact's new changes in the form of the domain model.
     * @return ArtifactBody - unsaved ArtifactBody with changes OR null if no change is detected.
     */
    public ArtifactVersion calculateArtifactVersion(ProjectVersion projectVersion,
                                                    Artifact artifact,
                                                    ArtifactAppEntity appEntity) {
        ModificationType modificationType = artifactVersionRepository
            .calculateModificationTypeForAppEntity(projectVersion, artifact, appEntity);

        if (modificationType == null) {
            return null;
        }

        ArtifactVersion artifactVersion = createArtifactVersionFromModification(
            projectVersion,
            modificationType,
            artifact,
            appEntity);

        this.artifactVersionRepository
            .findByProjectVersionAndArtifact(projectVersion, artifact)
            .ifPresent(version -> artifactVersion.setArtifactBodyId(version.getArtifactBodyId()));
        return artifactVersion;
    }

    private DeltaArtifact calculateArtifactModificationBetweenVersions(Artifact artifact,
                                                                       ProjectVersion beforeVersion,
                                                                       ProjectVersion afterVersion) {
        String artifactName = artifact.getName();
        List<ArtifactVersion> bodies = this.artifactVersionRepository.findByArtifact(artifact);

        ArtifactVersion beforeBody = this.artifactVersionRepository.getEntityAtVersion(bodies,
            beforeVersion);
        ArtifactVersion afterBody = this.artifactVersionRepository.getEntityAtVersion(bodies,
            afterVersion);

        ModificationType modificationType = this.artifactVersionRepository
            .calculateModificationType(beforeBody, afterBody);

        if (modificationType == null) {
            return null;
        }

        return createDeltaArtifactFrom(modificationType, artifactName, beforeBody, afterBody);
    }

    private ArtifactVersion createArtifactVersionFromModification(
        ProjectVersion projectVersion,
        ModificationType modificationType,
        Artifact artifact,
        ArtifactAppEntity artifactAppEntity
    ) {
        switch (modificationType) {
            case ADDED:
                return new ArtifactVersion(projectVersion,
                    ModificationType.ADDED,
                    artifact,
                    artifactAppEntity.summary,
                    artifactAppEntity.body);
            case MODIFIED:
                return new ArtifactVersion(projectVersion,
                    ModificationType.MODIFIED,
                    artifact,
                    artifactAppEntity.summary,
                    artifactAppEntity.body);
            case REMOVED:
                return new ArtifactVersion(projectVersion,
                    ModificationType.REMOVED,
                    artifact,
                    "",
                    "");
            default:
                throw new RuntimeException("Missing case in delta service.");
        }
    }

    private DeltaArtifact createDeltaArtifactFrom(ModificationType modificationType,
                                                  String artifactName,
                                                  ArtifactVersion beforeBody,
                                                  ArtifactVersion afterBody) {
        switch (modificationType) {
            case MODIFIED:
                return new ModifiedArtifact(artifactName,
                    beforeBody.getContent(),
                    beforeBody.getSummary(),
                    afterBody.getContent(),
                    afterBody.getSummary());
            case ADDED:
                return new AddedArtifact(artifactName, afterBody.getContent(), afterBody.getSummary());
            case REMOVED:
                return new RemovedArtifact(artifactName, beforeBody.getContent(), beforeBody.getSummary());
            default:
                return null;
        }
    }
}


