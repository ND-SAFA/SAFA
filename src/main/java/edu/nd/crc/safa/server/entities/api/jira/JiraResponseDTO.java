package edu.nd.crc.safa.server.entities.api.jira;

import lombok.AllArgsConstructor;
import lombok.Data;
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
        IMPORTED("imported");

        private final String value;
    }

}
