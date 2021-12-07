package edu.nd.crc.safa.server.entities.db;

import edu.nd.crc.safa.server.entities.api.SafaError;

public interface VersionAction {

    void action() throws SafaError;
}
