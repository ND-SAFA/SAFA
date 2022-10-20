package edu.nd.crc.safa.features.models.tgen.entities;

import java.util.ArrayList;
import java.util.List;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.features.models.entities.ModelAppEntity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
@Data
public class TracingPayload {
    /**
     * The method to generate trace links with.
     */
    @NotNull
    BaseGenerationModels method;
    /**
     * The model to use to generate trace links.
     */
    ModelAppEntity model;
    /**
     * The artifact levels to trace.
     */
    List<ArtifactLevel> artifactLevels = new ArrayList<>();

    @JsonIgnore
    public int getSize() {
        return this.artifactLevels.size();
    }
}
