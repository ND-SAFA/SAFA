package edu.nd.crc.safa.features.models.entities.api;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.tgen.entities.api.TGenPredictionRequestDTO;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
@Data
public class TGenTrainingRequest extends TGenPredictionRequestDTO {
    List<List<String>> links;

    public TGenTrainingRequest(String baseModel,
                               String modelPath,
                               List<Map<String, String>> sources,
                               List<Map<String, String>> targets,
                               List<TraceAppEntity> traces) {
        super(baseModel, modelPath, true, sources, targets, new HashMap<>());
        this.links = traces
            .stream()
            .map(t -> List.of(t.getSourceName(), t.getTargetName()))
            .collect(Collectors.toList());
    }
}
