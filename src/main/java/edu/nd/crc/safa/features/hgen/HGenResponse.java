package edu.nd.crc.safa.features.hgen;

import java.util.List;

import edu.nd.crc.safa.features.tgen.api.TGenDataset;
import edu.nd.crc.safa.features.tgen.api.responses.ITGenResponse;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class HGenResponse extends TGenDataset implements ITGenResponse {
    List<String> logs;
}
