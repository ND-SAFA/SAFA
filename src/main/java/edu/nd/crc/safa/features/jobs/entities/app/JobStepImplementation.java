package edu.nd.crc.safa.features.jobs.entities.app;

import java.lang.reflect.Method;

import edu.nd.crc.safa.features.jobs.entities.IJobStep;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@AllArgsConstructor
@Getter
@Setter
public class JobStepImplementation {
    private IJobStep annotation;
    private Method method;
}
