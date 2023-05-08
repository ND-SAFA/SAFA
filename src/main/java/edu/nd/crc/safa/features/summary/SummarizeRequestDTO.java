package edu.nd.crc.safa.features.summary;

import java.util.List;
import javax.annotation.Nullable;

import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * A request to summarize artifacts from the front-end.
 */
@Data
@NoArgsConstructor
public class SummarizeRequestDTO {
    /**
     *
     */
    List<TGenSummaryArtifact> artifacts;
    /**
     * The model to use for summaries.
     */
    @Nullable
    String model;
}
