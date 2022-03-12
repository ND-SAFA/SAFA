package edu.nd.crc.safa.server.controllers;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppConstraints;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.db.Document;
import edu.nd.crc.safa.server.repositories.documents.DocumentRepository;

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

    protected final ResourceBuilder resourceBuilder;

    @Autowired
    public BaseController(ResourceBuilder resourceBuilder) {
        this.resourceBuilder = resourceBuilder;
    }

    @ExceptionHandler(SafaError.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public SafaError handleServerError(SafaError safaError) {
        safaError.printError();
        return safaError;
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public SafaError handleValidationError(MethodArgumentNotValidException exception) {
        BindingResult bindingResult = exception.getBindingResult();
        StringBuilder errorMessage = new StringBuilder();
        for (ObjectError error : bindingResult.getAllErrors()) {
            errorMessage.append(createValidationMessage(error)).append("\n");
        }
        SafaError error = new SafaError(errorMessage.toString());
        error.setDetails(exception.getMessage());
        return error;
    }

    @ExceptionHandler(DataIntegrityViolationException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public SafaError handleDataIntegrityViolationException(DataIntegrityViolationException exception) {
        exception.printStackTrace();
        String errorMessage = AppConstraints.getConstraintError(exception);
        SafaError error = new SafaError(errorMessage, exception);
        error.setDetails(exception.getMessage());
        return error;
    }

    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public SafaError handleGenericError(Exception ex) {
        ex.printStackTrace();
        return new SafaError("An unexpected server error occurred.", ex);
    }

    protected Document getDocumentById(DocumentRepository documentRepository,
                                       UUID documentId) throws SafaError {
        Optional<Document> documentOptional = documentRepository.findById(documentId);
        if (documentOptional.isPresent()) {
            return documentOptional.get();
        } else {
            throw new SafaError("Could not find document with given id:" + documentId);
        }
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
