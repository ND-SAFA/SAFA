package edu.nd.crc.safa.server.services;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.server.entities.app.AddedArtifact;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.DeltaArtifact;
import edu.nd.crc.safa.server.entities.app.ModifiedArtifact;
import edu.nd.crc.safa.server.entities.app.ProjectDelta;
import edu.nd.crc.safa.server.entities.app.RemovedArtifact;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactBody;
import edu.nd.crc.safa.server.entities.db.ModificationType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ArtifactBodyRepository;
import edu.nd.crc.safa.server.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.utilities.ArtifactBodyFilter;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class DeltaService {

    ProjectVersionRepository projectVersionRepository;
    ArtifactRepository artifactRepository;
    ArtifactBodyRepository artifactBodyRepository;

    @Autowired
    public DeltaService(ProjectVersionRepository projectVersionRepository,
                        ArtifactRepository artifactRepository,
                        ArtifactBodyRepository artifactBodyRepository) {
        this.projectVersionRepository = projectVersionRepository;
        this.artifactRepository = artifactRepository;
        this.artifactBodyRepository = artifactBodyRepository;
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
            DeltaArtifact deltaArtifact = calcualteArtifactModificationBetweenVersions(artifact, baselineVersion, targetVersion);
            if (deltaArtifact == null) {
                continue;
            }
            String artifactName = deltaArtifact.getArtifactId();
            if (deltaArtifact instanceof ModifiedArtifact) {
                modified.put(artifactName, (ModifiedArtifact) deltaArtifact);
            } else if (deltaArtifact instanceof RemovedArtifact) {
                removed.put(artifactName, (RemovedArtifact) deltaArtifact);
            } else if (deltaArtifact instanceof AddedArtifact) {
                added.put(artifactName, (AddedArtifact) deltaArtifact);
                ArtifactAppEntity addedArtifactBody = new ArtifactAppEntity(artifact.getType().getName(),
                    artifact.getName(), ((AddedArtifact) deltaArtifact).getAfterSummary(),
                    ((AddedArtifact) deltaArtifact).getAfter());
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
    public ArtifactBody calculateArtifactChange(ProjectVersion projectVersion,
                                                Artifact artifact,
                                                ArtifactAppEntity appEntity) {
        ArtifactBody artifactBody = null;
        ArtifactBody previousBody =
            getArtifactBodyContentBeforeVersion(this.artifactBodyRepository.findByArtifact(artifact), projectVersion);
        if (previousBody != null) {
            if (appEntity == null) {
                artifactBody = new ArtifactBody(projectVersion,
                    ModificationType.REMOVED,
                    artifact,
                    "",
                    "");
            } else if (previousBody.getModificationType() == ModificationType.REMOVED) {
                artifactBody = new ArtifactBody(projectVersion,
                    ModificationType.ADDED,
                    artifact,
                    appEntity.summary,
                    appEntity.body);
            } else if (!previousBody.getContent().equals(appEntity.body)
                || !previousBody.getSummary().equals(appEntity.summary)) {
                artifactBody = new ArtifactBody(projectVersion,
                    ModificationType.MODIFIED,
                    artifact,
                    appEntity.summary,
                    appEntity.body);
            }
        } else {
            if (appEntity == null) {
                return null;
            }
            artifactBody = new ArtifactBody(projectVersion,
                ModificationType.ADDED,
                artifact,
                appEntity.summary,
                appEntity.body);
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

    private DeltaArtifact calcualteArtifactModificationBetweenVersions(Artifact artifact,
                                                                       ProjectVersion beforeVersion,
                                                                       ProjectVersion afterVersion) {

        String artifactName = artifact.getName();
        List<ArtifactBody> bodies = this.artifactBodyRepository.findByArtifact(artifact);
        ArtifactBody beforeBody = getArtifactBodyContentAtVersion(bodies, beforeVersion);
        ArtifactBody afterBody = getArtifactBodyContentAtVersion(bodies, afterVersion);

        ModificationType modificationType = calculateModificationTypeBetweenArtifactBodies(beforeBody, afterBody);

        if (modificationType == null) {
            return null;
        }

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

    private ModificationType calculateModificationTypeBetweenArtifactBodies(ArtifactBody beforeBody,
                                                                            ArtifactBody afterBody) {
        if (beforeBody == null || afterBody == null) {
            if (beforeBody == afterBody) {
                return null;
            } else if (beforeBody == null) {
                return ModificationType.ADDED;
            } else {
                return ModificationType.REMOVED;
            }
        } else {
            String beforeId = beforeBody.getContent() + beforeBody.getSummary();
            String afterId = afterBody.getContent() + afterBody.getSummary();

            if (beforeId.equals(afterId)) { // no change - same body
                return null;
            } else {
                if (afterBody.getModificationType() == ModificationType.REMOVED) {
                    return ModificationType.REMOVED;
                } else if (beforeBody.getModificationType() == ModificationType.REMOVED) {
                    return ModificationType.ADDED;
                } else {
                    return ModificationType.MODIFIED;
                }
            }
        }
    }

    private ArtifactBody getArtifactBodyContentAtVersion(List<ArtifactBody> bodies, ProjectVersion version) {
        return getMostUpToDateArtifactBodyThroughFilter(bodies, (target) -> target.isLessThanOrEqualTo(version));
    }

    private ArtifactBody getArtifactBodyContentBeforeVersion(List<ArtifactBody> bodies, ProjectVersion version) {
        return getMostUpToDateArtifactBodyThroughFilter(bodies, (target) -> target.isLessThan(version));
    }

    private ArtifactBody getMostUpToDateArtifactBodyThroughFilter(List<ArtifactBody> bodies,
                                                                  ArtifactBodyFilter filter) {
        ArtifactBody closestBodyToVersion = null;
        for (int i = bodies.size() - 1; i >= 0; i--) {
            ArtifactBody currentBody = bodies.get(i);
            ProjectVersion currentBodyVersion = currentBody.getProjectVersion();
            if (filter.compareTo(currentBodyVersion)) {
                if (closestBodyToVersion == null) {
                    closestBodyToVersion = currentBody;
                } else if (currentBodyVersion.isGreaterThan(closestBodyToVersion.getProjectVersion())
                ) {
                    closestBodyToVersion = currentBody;
                }
            }
        }
        return closestBodyToVersion;
    }
}
