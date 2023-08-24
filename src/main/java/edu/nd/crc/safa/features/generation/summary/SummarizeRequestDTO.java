package edu.nd.crc.safa.features.generation.summary;

import java.util.List;
import java.util.UUID;
import javax.annotation.Nullable;

import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * A request to summarize artifacts from the front-end.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class SummarizeRequestDTO {
    /**
     * The artifacts to summarize and their type.
     */
    List<UUID> artifacts;
    @Nullable
    ProjectVersion projectVersion;
}
