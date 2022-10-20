package edu.nd.crc.safa.features.models.entities.api;

import java.util.List;
import javax.validation.constraints.NotEmpty;

import edu.nd.crc.safa.features.models.tgen.entities.TracingRequest;

import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Represents a request to train model on given data
 */
@NoArgsConstructor
@Data
public class TrainingRequest {
    @NotEmpty
    List<TracingRequest> requests;
}
