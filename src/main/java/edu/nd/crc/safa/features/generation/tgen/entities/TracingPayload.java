package edu.nd.crc.safa.features.generation.tgen.entities;

import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
@Data
public class TracingPayload {
    /**
     * The artifact levels to trace.
     */
    List<ArtifactLevel> artifactLevels = new ArrayList<>();

    @JsonIgnore
    public int getSize() {
        return this.artifactLevels.size();
    }
}
