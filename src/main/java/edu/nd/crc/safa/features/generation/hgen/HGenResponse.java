package edu.nd.crc.safa.features.generation.hgen;

import java.util.List;

import edu.nd.crc.safa.features.generation.tgen.api.TGenDataset;
import edu.nd.crc.safa.features.generation.tgen.api.responses.ITGenResponse;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class HGenResponse extends TGenDataset implements ITGenResponse {
    List<String> logs;
}
