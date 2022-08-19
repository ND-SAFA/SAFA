package edu.nd.crc.safa.features.matrices.controllers;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.matrices.entities.TraceMatrix;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.repositories.TraceMatrixRepository;
import edu.nd.crc.safa.features.types.ArtifactType;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Provides endpoints for retrieving and creating new trace link matrices.
 */
@RestController
public class TraceMatrixController extends BaseController {

    private final TraceMatrixRepository traceMatrixRepository;
    private final ArtifactTypeRepository artifactTypeRepository;

    @Autowired
    public TraceMatrixController(ResourceBuilder resourceBuilder,
                                 ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
        this.traceMatrixRepository = serviceProvider.getTraceMatrixRepository();
        this.artifactTypeRepository = serviceProvider.getArtifactTypeRepository();
    }

    /**
     * Returns list of trace matrices in a specified project.
     *
     * @param projectId UUID of project whose matrices are returned.
     * @return List of project matrices defined in project.
     * @throws SafaError Throws error if project with ID is not found.
     */
    @GetMapping(AppRoutes.TraceMatrix.GET_TRACE_MATRICES)
    public Map<String, List<String>> getTraceMatricesInProject(@PathVariable UUID projectId) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withViewProject();
        List<TraceMatrix> projectTraceMatrices = traceMatrixRepository.findByProject(project);
        Map<String, List<String>> traceLinkDirections = new HashMap<>();
        for (TraceMatrix tm : projectTraceMatrices) {
            String sourceTypeName = tm.getSourceArtifactType().getName();
            String targetTypeName = tm.getTargetArtifactType().getName();
            if (traceLinkDirections.containsKey(sourceTypeName)) {
                traceLinkDirections.get(sourceTypeName).add(targetTypeName);
            } else {
                ArrayList<String> targetTypes = new ArrayList<>();
                targetTypes.add(targetTypeName);
                traceLinkDirections.put(sourceTypeName, targetTypes);
            }
        }

        for (ArtifactType at : this.artifactTypeRepository.findByProject(project)) {
            if (!traceLinkDirections.containsKey(at.getName())) {
                traceLinkDirections.put(at.getName(), new ArrayList<>());
            }
        }
        return traceLinkDirections;
    }

    /**
     * Creates a new trace matrix between given artifact types names in
     * specified project.
     *
     * @param projectId              UUID of project whose versions are returned.
     * @param sourceArtifactTypeName The name of the source artifact type.
     * @param targetArtifactTypeName The name of the target artifact type.
     * @throws SafaError Throws error if project with ID is not found.
     */
    @PostMapping(AppRoutes.TraceMatrix.CREATE_TRACE_MATRIX)
    public void createTraceMatrix(@PathVariable UUID projectId,
                                  @PathVariable String sourceArtifactTypeName,
                                  @PathVariable String targetArtifactTypeName) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withEditProject();
        Optional<TraceMatrix> traceMatrixQuery = traceMatrixRepository.queryForMatrixInProject(project,
            sourceArtifactTypeName, targetArtifactTypeName);
        if (traceMatrixQuery.isPresent()) {
            String error = String.format("Trace matrix already exists between %s and %s.",
                sourceArtifactTypeName,
                targetArtifactTypeName);
            throw new SafaError(error);
        }

        ArtifactType sourceArtifactType = getArtifactType(project, sourceArtifactTypeName);
        ArtifactType targetArtifactType = getArtifactType(project, targetArtifactTypeName);
        TraceMatrix traceMatrix = new TraceMatrix(project, sourceArtifactType, targetArtifactType);
        this.traceMatrixRepository.save(traceMatrix);
    }

    /**
     * Deletes trace matrix with given id if user has edit permission on associated project.
     *
     * @param projectId              The id of the project whose trace matrix is being deleted.
     * @param sourceArtifactTypeName The source artifact type name of the matrix.
     * @param targetArtifactTypeName The target artifact type name of the matrix.
     * @throws SafaError Throws error if user does not have edit permission on project.
     */
    @DeleteMapping(AppRoutes.TraceMatrix.DELETE_TRACE_MATRIX)
    public void deleteTraceMatrix(@PathVariable UUID projectId,
                                  @PathVariable String sourceArtifactTypeName,
                                  @PathVariable String targetArtifactTypeName) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withEditProject();
        Optional<TraceMatrix> traceMatrixOptional = this.traceMatrixRepository.queryForMatrixInProject(
            project,
            sourceArtifactTypeName,
            targetArtifactTypeName
        );
        if (traceMatrixOptional.isPresent()) {
            TraceMatrix traceMatrixToDelete = traceMatrixOptional.get();
            this.resourceBuilder.setProject(traceMatrixToDelete.getProject()).withEditProject();
            this.traceMatrixRepository.delete(traceMatrixToDelete);
        }
    }

    private ArtifactType getArtifactType(Project project, String artifactTypeName) throws SafaError {
        Optional<ArtifactType> artifactTypeQuery = this.artifactTypeRepository.findByProjectAndNameIgnoreCase(project,
            artifactTypeName);
        if (artifactTypeQuery.isEmpty()) {
            throw new SafaError("Could not find artifact type: " + artifactTypeName);
        }
        return artifactTypeQuery.get();
    }
}
