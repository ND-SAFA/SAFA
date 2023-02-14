package edu.nd.crc.safa.features.flatfiles.parser.tim;

import javax.validation.constraints.NotEmpty;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class TimTraceDefinition {
    @NotEmpty
    private String sourceType;

    @NotEmpty
    private String targetType;

    private String fileName;

    private Boolean generateLinks;

    public boolean isValid() {
        return sourceType != null
            && targetType != null
            && (hasFilename() || hasGenerateLinks());
    }

    public boolean generateLinks() {
        return hasGenerateLinks() && generateLinks;
    }

    public boolean hasGenerateLinks() {
        return generateLinks != null;
    }

    public boolean hasFilename() {
        return fileName != null;
    }
}
