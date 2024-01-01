package edu.nd.crc.safa.features.billing.services;

import edu.nd.crc.safa.features.artifacts.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.springframework.stereotype.Service;

@Service
public class CostEstimationService {

    private final ArtifactVersionRepository artifactVersionRepository;

    public CostEstimationService(ArtifactVersionRepository artifactVersionRepository) {
        this.artifactVersionRepository = artifactVersionRepository;
    }

    /**
     * Estimates the cost of an hgen run
     *
     * @param projectVersion The project version we will generate on
     * @param numLayers Number of layers to generate
     * @return The number of credits the run will use
     */
    public int estimateHgen(ProjectVersion projectVersion, int numLayers) {
        int numArtifacts = artifactVersionRepository.countByProjectVersion(projectVersion);
        return (int) Math.ceil(numArtifacts * (2 - (1 / Math.pow(2, numLayers - 1))));
    }

}
