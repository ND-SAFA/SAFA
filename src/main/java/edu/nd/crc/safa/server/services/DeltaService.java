package edu.nd.crc.safa.server.services;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import edu.nd.crc.safa.server.db.entities.app.AddedArtifact;
import edu.nd.crc.safa.server.db.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.db.entities.app.DeltaArtifact;
import edu.nd.crc.safa.server.db.entities.app.ModifiedArtifact;
import edu.nd.crc.safa.server.db.entities.app.ProjectDelta;
import edu.nd.crc.safa.server.db.entities.app.RemovedArtifact;
import edu.nd.crc.safa.server.db.entities.sql.Artifact;
import edu.nd.crc.safa.server.db.entities.sql.ArtifactBody;
import edu.nd.crc.safa.server.db.entities.sql.ModificationType;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.db.repositories.ArtifactBodyRepository;
import edu.nd.crc.safa.server.db.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.db.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.responses.ServerError;

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

    public ProjectDelta calculateDelta(ProjectVersion beforeVersion, ProjectVersion afterVersion) throws ServerError {
        if (!beforeVersion.getProject().getProjectId().equals(afterVersion.getProject().getProjectId())) {
            throw new ServerError("Expected versions to correspond to the same project");
        }

        Project project = beforeVersion.getProject();

        Hashtable<String, AddedArtifact> added = new Hashtable<>();
        Hashtable<String, ModifiedArtifact> modified = new Hashtable<>();
        Hashtable<String, RemovedArtifact> removed = new Hashtable<>();

        List<Artifact> projectArtifacts = this.artifactRepository.findByProject(project);
        List<ArtifactAppEntity> missingArtifacts = new ArrayList<>();

        for (Artifact artifact : projectArtifacts) {
            DeltaArtifact deltaArtifact = getModificationOverDelta(artifact, beforeVersion, afterVersion);
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
     * @return ArtifactBody - unsaved database entity with given changes and modification type.
     */
    public ArtifactBody calculateArtifactChange(ProjectVersion projectVersion,
                                                Artifact artifact,
                                                ArtifactAppEntity appEntity) {
        Project project = projectVersion.getProject();
        ArtifactBody artifactBody = null;
        Optional<ArtifactBody> previousBodyQuery = this.artifactBodyRepository.findLastArtifactBody(project, artifact);
        if (previousBodyQuery.isPresent()) {
            ArtifactBody previousBody = previousBodyQuery.get();
            if (appEntity == null) {
                artifactBody = new ArtifactBody(projectVersion,
                    ModificationType.REMOVED,
                    artifact,
                    null,
                    null);
            } else if (previousBody.getModificationType() == ModificationType.REMOVED) {
                artifactBody = new ArtifactBody(projectVersion,
                    ModificationType.ADDED,
                    artifact,
                    appEntity.summary,
                    appEntity.body);
            } else if (!previousBody.getContent().equals(appEntity.body)) {
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

    public DeltaArtifact getModificationOverDelta(Artifact artifact,
                                                  ProjectVersion beforeVersion,
                                                  ProjectVersion afterVersion) {
        List<ArtifactBody> bodies = this.artifactBodyRepository.findByArtifact(artifact);
        bodies = bodies
            .stream()
            .filter(artifactBody -> artifactBody
                .getProjectVersion()
                .isLessThanOrEqualTo(afterVersion))
            .collect(Collectors.toList());

        String artifactName = artifact.getName();

        ArtifactBody beforeBody = getBodyAtVersion(bodies, beforeVersion);
        ArtifactBody afterBody = getBodyAtVersion(bodies, afterVersion);

        if (beforeBody == null) {
            if (afterBody == null) {
                return null;
            }
            return new AddedArtifact(artifactName, afterBody.getContent(), afterBody.getSummary());
        }

        String beforeContent = beforeBody.getContent();
        String beforeSummary = beforeBody.getSummary();

        String afterContent = afterBody.getContent();
        String afterSummary = afterBody.getSummary();

        if (beforeBody.hasSameId(afterBody)) {
            return null; // no change
        } else if (beforeBody.getModificationType() == afterBody.getModificationType()) {
            // added or modified at two the two versions = compare contents
            if (beforeBody.getModificationType() == ModificationType.REMOVED) { // both removed = no change
                return null;
            }
            if (beforeContent.equals(afterContent)) { // no change - same body
                return null;
            } else {
                return new ModifiedArtifact(artifactName, beforeContent, beforeSummary, afterContent, afterSummary);
            }
        } else {
            switch (afterBody.getModificationType()) {
                case MODIFIED:
                    return new ModifiedArtifact(artifactName, beforeContent, beforeSummary, afterContent, afterSummary);
                case ADDED:
                    return new AddedArtifact(artifactName, afterContent, afterSummary);
                case REMOVED:
                    return new RemovedArtifact(artifactName, beforeContent, beforeSummary);
                default:
                    throw new RuntimeException("New modification type is not supported");
            }
        }
    }

    public ArtifactBody getBodyAtVersion(List<ArtifactBody> bodies, ProjectVersion version) {
        for (int i = bodies.size() - 1; i >= 0; i--) {
            ArtifactBody body = bodies.get(i);
            if (body
                .getProjectVersion()
                .isLessThanOrEqualTo(version)) {
                return body;
            }
        }
        return null;
    }
}
