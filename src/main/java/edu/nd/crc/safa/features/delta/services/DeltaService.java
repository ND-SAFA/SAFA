package edu.nd.crc.safa.features.delta.services;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.features.delta.entities.app.EntityDelta;
import edu.nd.crc.safa.features.delta.entities.app.ProjectDelta;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.repositories.TraceLinkVersionRepository;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

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


