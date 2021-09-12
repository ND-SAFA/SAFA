package edu.nd.crc.safa.server.services;

import java.util.Hashtable;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.server.db.entities.app.AddedArtifact;
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
            }
        }

        return new ProjectDelta(added, modified, removed);
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

        ArtifactBody beforeBody = getBodyAtVersion(bodies, beforeVersion);
        ArtifactBody afterBody = getBodyAtVersion(bodies, afterVersion);

        String artifactName = artifact.getName();
        String beforeContent = beforeBody.getContent();
        String afterContent = afterBody.getContent();

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
                return new ModifiedArtifact(artifactName, beforeContent, afterContent);
            }
        } else {
            switch (afterBody.getModificationType()) {
                case MODIFIED:
                    return new ModifiedArtifact(artifactName, beforeContent, afterContent);
                case ADDED:
                    return new AddedArtifact(artifactName, afterContent);
                case REMOVED:
                    return new RemovedArtifact(artifactName, beforeContent);
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
