package edu.nd.crc.safa.test.services;

import edu.nd.crc.safa.test.services.builders.BuilderState;
import edu.nd.crc.safa.test.services.requests.CommonProjectRequests;
import edu.nd.crc.safa.test.services.requests.CommonUserRequests;
import edu.nd.crc.safa.test.services.requests.GenCommonRequests;

import lombok.AllArgsConstructor;

@AllArgsConstructor
public class CommonRequestService {

    private BuilderState state;

    public CommonProjectRequests project() {
        return new CommonProjectRequests(this.state);
    }

    public GenCommonRequests generative() {
        return new GenCommonRequests();
    }


    public CommonUserRequests user() {
        return new CommonUserRequests(this.state);
    }
}
