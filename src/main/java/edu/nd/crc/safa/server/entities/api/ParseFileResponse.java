package edu.nd.crc.safa.server.entities.api;

import java.util.List;

/**
 * Defines an interface for retrieving errors after parsing a datafile .
 */
public interface ParseFileResponse {

    List<String> getErrors();

    void setErrors(List<String> errors);
}
