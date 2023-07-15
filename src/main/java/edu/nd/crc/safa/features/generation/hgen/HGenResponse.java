package edu.nd.crc.safa.features.generation.hgen;

import java.util.List;

import edu.nd.crc.safa.features.generation.common.ITGenResponse;
import edu.nd.crc.safa.features.generation.common.TGenDataset;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class HGenResponse extends TGenDataset implements ITGenResponse {
    List<String> logs;
}
