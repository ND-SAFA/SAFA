package edu.nd.crc.safa.features.jira.entities.app;

import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * Simple DTO to wrap status messages for JIRA operations
 */
@AllArgsConstructor
@Getter
public class JiraResponseDTO<T> {

    T payload;

    JiraResponseMessage message;

    @AllArgsConstructor
    public enum JiraResponseMessage {

        CREATED("created"),
        UPDATED("updated"),
        OK("ok"),
        ERROR("error"),
        IMPORTED("imported"),
        CANNOT_PARSE_PROJECT("cannot parse project");

        private final String value;
    }

}
