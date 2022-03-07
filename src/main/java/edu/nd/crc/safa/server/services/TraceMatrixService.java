package edu.nd.crc.safa.server.services;

import java.util.List;

import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.TraceMatrix;
import edu.nd.crc.safa.server.repositories.entities.traces.TraceMatrixRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Responsible for collecting all parsing errors in a project version.
 */
@Service
public class TraceMatrixService {
    private final TraceMatrixRepository traceMatrixRepository;

    @Autowired
    public TraceMatrixService(TraceMatrixRepository traceMatrixRepository) {
        this.traceMatrixRepository = traceMatrixRepository;
    }

    public void verifyOrCreateTraceMatrix(Project project,
                                          ArtifactType sourceArtifactType,
                                          ArtifactType targetArtifactType) throws SafaError {
        List<TraceMatrix> projectMatrices = this.traceMatrixRepository.findByProject(project);
        for (TraceMatrix tm : projectMatrices) {
            if (tm.getSourceArtifactType().equals(sourceArtifactType)
                && tm.getTargetArtifactType().equals(targetArtifactType)) {
                return;
            } else if (tm.getSourceArtifactType().equals(targetArtifactType)
                && tm.getTargetArtifactType().equals(sourceArtifactType)) {
                throw new SafaError("Trace link goes against existing trace link directions.");
            }
        }
        // Case only exists if no trace matrix exists.
        TraceMatrix newTraceMatrix = new TraceMatrix(project, sourceArtifactType, targetArtifactType);
        this.traceMatrixRepository.save(newTraceMatrix);
    }
}
