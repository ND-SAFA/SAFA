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
            DeltaArtifact deltaArtifact = this.artifactVersionRepository
                .calculateArtifactModificationBetweenVersions(
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
}


