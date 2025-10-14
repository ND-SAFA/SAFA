package edu.nd.crc.safa.features.health;

import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.repositories.ArtifactRepository;
import edu.nd.crc.safa.features.artifacts.services.ArtifactService;
import edu.nd.crc.safa.features.comments.repositories.CommentArtifactRepository;
import edu.nd.crc.safa.features.comments.repositories.CommentConceptRepository;
import edu.nd.crc.safa.features.comments.repositories.CommentRepository;
import edu.nd.crc.safa.features.commits.services.CommitService;
import edu.nd.crc.safa.features.generation.api.GenApi;
import edu.nd.crc.safa.features.generation.api.GenerationDatasetService;
import edu.nd.crc.safa.features.generation.common.GenerationArtifact;
import edu.nd.crc.safa.features.generation.common.GenerationDataset;
import edu.nd.crc.safa.features.health.entities.HealthRequest;
import edu.nd.crc.safa.features.health.entities.HealthResponseDTO;
import edu.nd.crc.safa.features.health.entities.gen.GenHealthResponse;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@AllArgsConstructor
@Service
public class HealthService {

    private final CommentRepository commentRepository;
    private final CommentArtifactRepository commentArtifactRepository;
    private final CommentConceptRepository commentConceptRepository;
    private ArtifactRepository artifactRepository;
    private ArtifactService artifactService;
    private GenApi genApi;
    private CommitService commitService;
    private GenerationDatasetService generationDatasetService;
    private HealthResponseSaver healthResponseSaver;

    /**
     * Performs health tasks on specified artifacts.
     *
     * @param user           The user trigger action and responsible for any changes to the system.
     * @param projectVersion The project version of the artifacts to use.
     * @param request        The request containing target artifacts and tasks to perform.
     * @return HealthResponse containing saved entities.
     */
    public HealthResponseDTO performHealthChecks(SafaUser user,
                                                 ProjectVersion projectVersion,
                                                 HealthRequest request) {
        GenerationDataset dataset = generationDatasetService.retrieveGenerationDataset(projectVersion);
        List<GenerationArtifact> targetArtifacts = extractTargetArtifacts(request, dataset.getArtifacts());
        assert !targetArtifacts.isEmpty();
        GenHealthResponse genResponse = genApi.generateHealthChecks(request.getTasks(),
            dataset,
            targetArtifacts);
        HealthResponseDTO response = new HealthResponseDTO();
        healthResponseSaver.saveHealthChecks(
            user,
            response,
            projectVersion,
            genResponse
        );
        return response;
    }

    /**
     * Retrieves target artifact specified, either by types or by ids.
     *
     * @param requestDTO       The request containing target artifact specification.
     * @param projectArtifacts The artifacts in the project.
     * @return List of artifacts specified in request.
     */
    private List<GenerationArtifact> extractTargetArtifacts(HealthRequest requestDTO,
                                                            List<GenerationArtifact> projectArtifacts) {
        if (!requestDTO.getArtifactTypes().isEmpty()) {
            Set<String> artifactTypeSet = new HashSet<>(requestDTO.getArtifactTypes());
            return projectArtifacts
                .stream()
                .filter(a -> artifactTypeSet.contains(a.getLayerId()))
                .toList();
        } else if (!requestDTO.getArtifactIds().isEmpty()) {
            Set<UUID> artifactIdSet = new HashSet<>(requestDTO.getArtifactIds());
            return projectArtifacts
                .stream()
                .filter(a -> artifactIdSet.contains(a.getInternalId()))
                .toList();

        } else {
            throw new SafaError("Expected request to contain either artifactIds or artifactTypes, got none.");
        }
    }
}
