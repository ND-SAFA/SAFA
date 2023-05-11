package edu.nd.crc.safa.features.hgen;

import java.util.List;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class TGenHGenResponse {
    /**
     * Generates artifacts for each cluster.
     */
    List<String> artifacts;
}
