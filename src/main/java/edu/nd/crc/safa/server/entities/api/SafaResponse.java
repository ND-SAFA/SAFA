package edu.nd.crc.safa.server.entities.api;

//TODO: Remove this and replace with actual http codes
public class SafaResponse {
    private Object body;
    private int status;

    public SafaResponse(Object body) {
        this.body = body;
        this.status = ResponseCodes.SUCCESS;
    }

    public SafaResponse(Object body, int errorCode) {
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
