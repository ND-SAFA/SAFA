package edu.nd.crc.safa.features.tgen.entities.api;

import lombok.Data;

@Data
public class AbstractTGenResponse {
    int status;
    String exception;
}
