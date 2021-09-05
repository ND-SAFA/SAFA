package edu.nd.crc.safa.server.services;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.db.entities.app.AddedArtifact;
import edu.nd.crc.safa.db.entities.app.DeltaArtifact;
import edu.nd.crc.safa.db.entities.app.ModifiedArtifact;
import edu.nd.crc.safa.db.entities.app.ProjectDelta;
import edu.nd.crc.safa.db.entities.app.RemovedArtifact;
import edu.nd.crc.safa.db.entities.sql.Artifact;
import edu.nd.crc.safa.db.entities.sql.ArtifactBody;
import edu.nd.crc.safa.db.entities.sql.ModificationType;
import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.db.repositories.sql.ArtifactBodyRepository;
import edu.nd.crc.safa.db.repositories.sql.ArtifactRepository;
import edu.nd.crc.safa.db.repositories.sql.ProjectVersionRepository;
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

        List<AddedArtifact> added = new ArrayList<>();
        List<ModifiedArtifact> modified = new ArrayList<>();
        List<RemovedArtifact> removed = new ArrayList<>();

        List<Artifact> projectArtifacts = this.artifactRepository.findByProject(project);
        for (Artifact artifact : projectArtifacts) {
            DeltaArtifact deltaArtifact = getModificationOverDelta(artifact, beforeVersion, afterVersion);

            if (deltaArtifact instanceof ModifiedArtifact) {
                modified.add((ModifiedArtifact) deltaArtifact);
            } else if (deltaArtifact instanceof RemovedArtifact) {
                removed.add((RemovedArtifact) deltaArtifact);
            } else if (deltaArtifact instanceof AddedArtifact) {
                added.add((AddedArtifact) deltaArtifact);
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
            .filter(b -> b.getProjectVersionId() <= afterVersion.getVersionId())
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
            if (body.getProjectVersionId() <= version.getVersionId()) {
                return body;
            }
        }
        return null;
    }
}
