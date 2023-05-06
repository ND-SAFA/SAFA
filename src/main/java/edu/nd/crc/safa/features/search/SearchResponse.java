package edu.nd.crc.safa.features.search;

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
    List<UUID> artifactIds = new ArrayList<>();
    /**
     * Artifact bodies of associated matched artifacts.
     */
    List<String> artifactBodies = new ArrayList<>();
}
