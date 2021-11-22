package edu.nd.crc.safa.server.entities.api;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.server.entities.app.TraceAppEntity;

public class ParseTraceFileResponse implements ParseFileResponse {

    List<TraceAppEntity> traces;
    List<String> errors;

    public ParseTraceFileResponse() {
        this.traces = new ArrayList<>();
        this.errors = new ArrayList<>();
    }

    public List<TraceAppEntity> getTraces() {
        return traces;
    }

    public void setTraces(List<TraceAppEntity> traces) {
        this.traces = traces;
    }

    public List<String> getErrors() {
        return errors;
    }

    public void setErrors(List<String> errors) {
        this.errors = errors;
    }
}
