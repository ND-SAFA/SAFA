package edu.nd.crc.safa.features.models.entities.api;

import java.util.List;
import java.util.UUID;
import javax.validation.Valid;
import javax.validation.constraints.NotEmpty;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.models.entities.ModelAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Represents a request to train model on given data
 */
@NoArgsConstructor
@Data
public class TrainingRequest {
    @Valid UUID projectId;
    @NotEmpty
    List<ArtifactAppEntity> sources;
    @NotEmpty
    List<ArtifactAppEntity> targets;
    @NotEmpty
    List<TraceAppEntity> traces;
    @Valid ModelAppEntity model;
}
