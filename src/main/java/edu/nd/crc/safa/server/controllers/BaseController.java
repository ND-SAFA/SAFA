package edu.nd.crc.safa.server.controllers;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppConstraints;
import edu.nd.crc.safa.server.entities.api.ResponseCodes;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.api.ServerResponse;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.HttpStatus;
import org.springframework.validation.BindingResult;
import org.springframework.validation.FieldError;
import org.springframework.validation.ObjectError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
public abstract class BaseController {

    protected final ProjectVersionRepository projectVersionRepository;
    protected final ProjectRepository projectRepository;
    protected final ResourceBuilder resourceBuilder;

    @Autowired
    public BaseController(ProjectRepository projectRepository,
                          ProjectVersionRepository projectVersionRepository,
                          ResourceBuilder resourceBuilder) {
        this.projectVersionRepository = projectVersionRepository;
        this.projectRepository = projectRepository;
        this.resourceBuilder = resourceBuilder;
    }

    @ExceptionHandler(SafaError.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ServerResponse handleServerError(SafaError exception) {
        exception.printError();
        return new ServerResponse(exception, ResponseCodes.FAILURE);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ServerResponse handleValidationError(MethodArgumentNotValidException exception) {
        BindingResult bindingResult = exception.getBindingResult();
        StringBuilder errorMessage = new StringBuilder();
        for (ObjectError error : bindingResult.getAllErrors()) {
            errorMessage.append(createValidationMessage(error)).append("\n");
        }
        SafaError error = new SafaError(errorMessage.toString());
        error.setDetails(exception.getMessage());
        return new ServerResponse(error, ResponseCodes.FAILURE);
    }

    @ExceptionHandler(DataIntegrityViolationException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ServerResponse handleDataIntegrityViolationException(DataIntegrityViolationException exception) {
        exception.printStackTrace();
        String errorMessage = AppConstraints.getConstraintError(exception);
        SafaError error = new SafaError(errorMessage, exception);
        error.setDetails(exception.getMessage());
        return new ServerResponse(error, ResponseCodes.FAILURE);
    }

    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ServerResponse handleGenericError(Exception ex) {
        ex.printStackTrace();
        SafaError wrapper = new SafaError("An unexpected server error occurred.", ex);
        return new ServerResponse(wrapper, ResponseCodes.FAILURE);
    }

    private String createValidationMessage(ObjectError error) {
        String objectName = error.getObjectName();
        String message = error.getDefaultMessage();
        if (error instanceof FieldError) {
            String fieldName = ((FieldError) error).getField();
            return fieldName + " in " + objectName + " " + message;
        } else {
            return objectName + message;
        }
    }
}
