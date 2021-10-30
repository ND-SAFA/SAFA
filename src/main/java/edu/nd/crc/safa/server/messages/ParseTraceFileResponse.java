package edu.nd.crc.safa.server.messages;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.server.db.entities.app.TraceApplicationEntity;

public class ParseTraceFileResponse {

    List<TraceApplicationEntity> traces;
    List<String> errors;

    public ParseTraceFileResponse() {
        this.traces = new ArrayList<>();
        this.errors = new ArrayList<>();
    }

    public List<TraceApplicationEntity> getTraces() {
        return traces;
    }

    public void setTraces(List<TraceApplicationEntity> traces) {
        this.traces = traces;
    }

    public List<String> getErrors() {
        return errors;
    }

    public void setErrors(List<String> errors) {
        this.errors = errors;
    }
}
