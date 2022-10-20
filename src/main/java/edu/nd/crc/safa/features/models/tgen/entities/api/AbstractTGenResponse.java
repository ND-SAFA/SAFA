package edu.nd.crc.safa.features.models.tgen.entities.api;

import lombok.Data;

@Data
public class AbstractTGenResponse {
    int status;
    String exception;
}
