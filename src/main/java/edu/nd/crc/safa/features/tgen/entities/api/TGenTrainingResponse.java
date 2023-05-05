package edu.nd.crc.safa.features.models.tgen.entities.api;

import java.util.Map;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class TGenTrainingResponse extends AbstractTGenResponse {
    int global_step;
    double training_loss;
    Map<String, Double> metrics;
}
