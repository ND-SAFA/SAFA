package edu.nd.crc.safa.features.flatfiles.parser.tim;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class TimTraceDefinition {
    @NotEmpty
    @NotNull
    private String sourceType;

    @NotEmpty
    @NotNull
    private String targetType;

    private String fileName;

    private Boolean generateLinks;

    private String generationMethod;

    @JsonIgnore
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
