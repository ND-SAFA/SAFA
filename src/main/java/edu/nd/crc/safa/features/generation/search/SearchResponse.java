package edu.nd.crc.safa.features.generation.search;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * The response from the search endpoint.
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class SearchResponse {
    /**
     * The matched artifact ids.
     */
    private List<UUID> artifactIds = new ArrayList<>();
}
