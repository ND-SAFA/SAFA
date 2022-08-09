package edu.nd.crc.safa.features.flatfiles.entities;

import java.util.List;

/**
 * Defines an interface for retrieving errors after parsing a datafile .
 */
public interface ParseFileResponse {

    List<String> getErrors();

    void setErrors(List<String> errors);
}
