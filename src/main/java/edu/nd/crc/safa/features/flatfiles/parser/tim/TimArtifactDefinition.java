package edu.nd.crc.safa.features.flatfiles.parser.tim;

import jakarta.validation.constraints.NotEmpty;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class TimArtifactDefinition {
    @NotEmpty
    @NotNull
    private String type;

    @NotEmpty
    @NotNull
    private String fileName;
}
