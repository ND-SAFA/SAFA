package edu.nd.crc.safa.features.models.entities.api;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.tgen.entities.TGenPredictionRequestDTO;
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
                               Map<String, String> sources,
                               Map<String, String> targets,
                               List<TraceAppEntity> traces) {
        super(baseModel, modelPath, sources, targets);
        this.links = traces
            .stream()
            .map(t -> List.of(t.getSourceName(), t.getTargetName()))
            .collect(Collectors.toList());
    }
}
