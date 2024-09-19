package edu.nd.crc.safa.features.generation.api;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.services.ArtifactService;
import edu.nd.crc.safa.features.common.ProjectEntities;
import edu.nd.crc.safa.features.generation.common.GenerationArtifact;
import edu.nd.crc.safa.features.generation.common.GenerationDataset;
import edu.nd.crc.safa.features.generation.common.GenerationLink;
import edu.nd.crc.safa.features.projects.services.ProjectRetrievalService;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@AllArgsConstructor
@Service
public class GenerationDatasetService {
    private ProjectRetrievalService projectRetrievalService;
    private ArtifactService artifactService;

    /**
     * Retrieves generation dataset for project version.
     *
     * @param projectVersion Version of artifacts and trace links to include.
     * @return Generation dataset.
     */
    public GenerationDataset retrieveGenerationDataset(ProjectVersion projectVersion) {
        ProjectEntities projectEntities = projectRetrievalService.retrieveProjectEntitiesAtProjectVersion(projectVersion);
        GenerationDataset dataset = new GenerationDataset();
        List<GenerationArtifact> generationArtifacts =
            projectEntities.getArtifacts().stream().map(GenerationArtifact::new).collect(Collectors.toList());
        List<GenerationLink> generationLinks = projectEntities.getTraces().stream().map(GenerationLink::new).collect(Collectors.toList());
        dataset.setArtifacts(generationArtifacts);
        dataset.setLinks(generationLinks);
        // TODO : Add layers
        return dataset;
    }
}
