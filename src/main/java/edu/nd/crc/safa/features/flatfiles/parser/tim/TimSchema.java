package edu.nd.crc.safa.features.flatfiles.parser.tim;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class TimSchema {

    @NotNull
    private List<TimArtifactDefinition> artifacts;

    @NotNull
    private List<TimTraceDefinition> traces;
}
