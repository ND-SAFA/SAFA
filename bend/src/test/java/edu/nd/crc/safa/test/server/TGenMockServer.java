package edu.nd.crc.safa.test.server;

import edu.nd.crc.safa.config.TGenConfig;
import edu.nd.crc.safa.features.generation.common.CeleryStatus;
import edu.nd.crc.safa.features.generation.common.TGenStatus;
import edu.nd.crc.safa.features.generation.common.TGenTask;

public class TGenMockServer extends SafaMockServer {

    /**
     * Sets the current TGEN endpoint to this mock server after construction.
     */
    @Override
    protected void afterInit() {
        super.afterInit();
        TGenConfig.setEndpoint(this.getRemoteApiUrl());
    }

    /**
     * Sets the next response to expect task, status, and finally job result.
     *
     * @param jobResult The job result.
     */
    public void setJobResponse(Object jobResult) {
        TGenTask task = new TGenTask();
        TGenStatus status = new TGenStatus();
        status.setStatus(CeleryStatus.SUCCESS);

        setResponse(task);
        setResponse(status);
        setResponse(jobResult);
    }
}
