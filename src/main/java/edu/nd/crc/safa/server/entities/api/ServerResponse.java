package edu.nd.crc.safa.server.entities.api;

public class ServerResponse {
    private Object body;
    private int status;

    public ServerResponse(Object body) {
        this.body = body;
        this.status = ResponseCodes.SUCCESS;
    }

    public ServerResponse(Object body, int errorCode) {
        this.body = body;
        this.status = errorCode;
    }

    public Object getBody() {
        return this.body;
    }

    public void setBody(Object body) {
        this.body = body;
    }

    public int getStatus() {
        return this.status;
    }

    public void setStatus(int status) {
        this.status = status;
    }
}
