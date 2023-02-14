package edu.nd.crc.safa.features.flatfiles.parser.tim;

import javax.validation.constraints.NotEmpty;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class TimArtifactDefinition {
    @NotEmpty
    private String type;

    @NotEmpty
    private String fileName;
}
