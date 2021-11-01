package edu.nd.crc.safa.server.entities.api;

import java.util.List;

public interface ParseFileResponse {

    List<String> getErrors();

    void setErrors(List<String> errors);
}
