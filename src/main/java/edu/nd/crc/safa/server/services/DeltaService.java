package edu.nd.crc.safa.server.services;

import edu.nd.crc.safa.server.entities.app.delta.EntityDelta;
import edu.nd.crc.safa.server.entities.app.delta.ProjectDelta;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.artifacts.ArtifactVersionRepository;
import edu.nd.crc.safa.server.repositories.traces.TraceLinkVersionRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Responsible for calculating the delta between any two versions.
 */
@Service
public class DeltaService {

    private final ArtifactVersionRepository artifactVersionRepository;
    private final TraceLinkVersionRepository traceLinkVersionRepository;

    @Autowired
    public DeltaService(ArtifactVersionRepository artifactVersionRepository,
                        TraceLinkVersionRepository traceLinkVersionRepository) {
        this.artifactVersionRepository = artifactVersionRepository;
        this.traceLinkVersionRepository = traceLinkVersionRepository;
    }

    /**
     * Calculates artifacts removed, added, and modified between given versions.
     *
     * @param baselineVersion The version whose entities will be held as the baseline.
     * @param targetVersion   The version whose entities will be compared to baseline entities.
     * @return ProjectDelta summarizing changes between versions.
     */
    public ProjectDelta calculateProjectDelta(ProjectVersion baselineVersion, ProjectVersion targetVersion) {
        EntityDelta<ArtifactAppEntity> artifactDelta =
            this.artifactVersionRepository.calculateEntityDelta(baselineVersion,
                targetVersion);
        EntityDelta<TraceAppEntity> traceDelta =
            this.traceLinkVersionRepository.calculateEntityDelta(baselineVersion,
                targetVersion);
        return new ProjectDelta(artifactDelta, traceDelta);
    }
}


