package edu.nd.crc.safa.importer;

import java.io.File; 
import java.util.Scanner; 
import java.io.IOException; 
import java.util.*; 
import java.nio.file.*;
import java.io.FileWriter;

import com.jsoniter.JsonIterator;
import com.jsoniter.any.Any;

import org.springframework.stereotype.Component;

@Component
public class Flatfile {
    public class MissingFileException extends Exception { 
        public MissingFileException(String errorMessage) {
            super(errorMessage);
        }
    }
    public class Tim {
        List<DataFile> dataFiles; 
        List<LinkFile> linkFiles; 
    }

    public class DataFile {
        public String type; 
        public String file; 
    }

    public class LinkFile {
        public String source; 
        public String target; 
        public String file; 
        public String name; 
    }

    public class DataEntry {
        public String summary; 
        public String id; 
        public String content; 
    }

    public class Artifact {
        public String type;
        public String file;
        public List<DataEntry> entries;
        public Set<String> uniqueIDs; 
    }

    public class Link {
        public String source; 
        public String target; 
        public String sourceType; 
        public String targetType; 
    }

    public class Connection {
        public String name;
        public String file;
        public String sourceType; 
        public String targetType; 
        public List<Link> links; 
    }

    public class ParsedData {
        public List<Artifact> artifacts; 
        public List<Connection> connections; 
    }

    public class ErrorText {
        String text = "";
    }

    public void errorGenerator(String file, int lineNumber, String message, ErrorText errorText){
        String text = String.format("ERROR: CSV: %s LINE: %d DESC: %s \n", file, lineNumber, message);
        errorText.text += text;
    }

    public void uniqueIDChecker(ParsedData parsedData, ErrorText errorText){
        Set<String> totalIDs = new HashSet<String>();
        for (Artifact artifact : parsedData.artifacts){
            totalIDs.addAll(artifact.uniqueIDs);
        }

        for (String ID : totalIDs){
            String warning = "Warning: Files:";
            int count = 0;

            for (Artifact artifact : parsedData.artifacts){
                if (artifact.uniqueIDs.contains(ID)){
                    if (count == 0){
                        warning += String.format(" %s", artifact.file);
                    } else {
                        warning += String.format(", %s", artifact.file);
                    }
                    count++;
                }
            }
            if (count > 1){
                warning += String.format(" each have an entry with the same ID: %s.\n", ID);
                errorText.text += warning;
            }
        }
    }

    public void generateErrorReport(String errorText, String fileName) {
        try {
            File myFile = new File(fileName); 
            if (!myFile.createNewFile()) {
                new FileWriter(fileName, false).close();    // clear file if info already present - overwrite previous error report
            } 
            
            // 
            try {
                Files.write(Paths.get(fileName), errorText.getBytes(), StandardOpenOption.APPEND);
            } catch (IOException e) {
                System.out.println("Could not append text to file.");
            }
        } catch (IOException e) {
            System.out.println("Could not open " + fileName);  
        }
    }

    public void generateInitialDirectories(String projectName) throws Exception {
        
        File file = new File(projectName);

        if (file.mkdir()) {
            String currentDirPath = projectName + "/current"; 
            File currFile = new File(currentDirPath); 
            if (currFile.mkdir()) {
                String testPath = currentDirPath + "/testfile.txt"; 
                File testFile = new File(testPath); 
                if (testFile.createNewFile()) {
                    try {
                        FileWriter myWriter = new FileWriter(testPath);
                        myWriter.write("Test message!!");
                        myWriter.close();
                    } catch (IOException e) {
                        System.out.println("Could not open test file"); 
                    }
                }
            } else {
                System.out.println("Count not create current project directory."); 
            }
        } else {
           System.out.println("Could not create initial project directory.");
        }
    }

    public void generateNextVersion(String projectName, String versionName) {
        
    }

    public String readFileAsString(String fileName) throws Exception { 
        String data = ""; 
        data = new String(Files.readAllBytes(Paths.get(fileName))); 
        return data; 
    }

    public List<DataFile> readDatafile(JsonIterator iterator) throws Exception {
        List<DataFile> dataFiles = new ArrayList<DataFile>();
        for (String artifact = iterator.readObject(); artifact != null; artifact = iterator.readObject()){
            DataFile data = new DataFile();
            data.type = artifact;
            for (String file = iterator.readObject(); file != null; file = iterator.readObject()){
                data.file = iterator.readString();
                dataFiles.add(data);
            }
        }
        return dataFiles;
    }

    public LinkFile readLink(JsonIterator iterator, String linkName) throws Exception {
        LinkFile linkFile = new LinkFile();
        linkFile.name = linkName;
        Boolean generated = false;

        for (String attr = iterator.readObject(); attr != null; attr = iterator.readObject()){
            if (attr.toLowerCase().equals("source")){
                linkFile.source = iterator.readString();
            } else if (attr.toLowerCase().equals("target")) {
                linkFile.target = iterator.readString();
            } else if (attr.toLowerCase().equals("generatelinks")){
                generated = iterator.readString().toLowerCase().equals("true") ? true : false;
            } else {
                linkFile.file = iterator.readString();
            }
        }

        if (generated){
            linkFile.file = "/GENERATED/" + linkFile.file;
        }

        return linkFile;
    }


    public Tim parseTim(String fileName) throws Exception{
        String data = readFileAsString(fileName);
        JsonIterator iterator = JsonIterator.parse(data);
        Tim tim = new Tim();
        List<DataFile> dataFiles = new ArrayList<DataFile>();
        List<LinkFile> linkFiles = new ArrayList<LinkFile>();
        for (String field = iterator.readObject(); field != null; field = iterator.readObject()){
            if (field.toLowerCase().equals("datafiles")) {
                dataFiles = readDatafile(iterator);
            } 
            else {
                linkFiles.add(readLink(iterator, field));
            }
        }
        tim.dataFiles = dataFiles;
        tim.linkFiles = linkFiles;
        return tim;
    }

    public DataEntry createDataEntry(String[] headersArray, List<String> data) {
        DataEntry dataEntry = new DataEntry(); 
        for (int i = 0; i < 3; i++) {
            if (headersArray[i].toLowerCase().equals("id")) {
                dataEntry.id = data.get(i); 
            }
            else if (headersArray[i].toLowerCase().equals("summary")) {
                dataEntry.summary = data.get(i); 
            }
            else if (headersArray[i].toLowerCase().equals("content")) {
                dataEntry.content = data.get(i); 
            }
        }
        return dataEntry;
    }
    
    public boolean linkValidator(Connection connection, List<Artifact> artifacts, Link link, ErrorText errorText, int lineNumber){
        boolean validSource = false;
        String sourceFile = "N/A";

        for (Artifact artifact : artifacts){
            if (artifact.type.equals(connection.sourceType)){
                sourceFile = artifact.file;
                validSource = artifact.uniqueIDs.contains(link.source);
                break;
            }
        }

        boolean validTarget = false;
        String targetFile = "N/A";

        for (Artifact artifact : artifacts){
            if (artifact.type.equals(connection.targetType)){
                targetFile = artifact.file;
                validTarget = artifact.uniqueIDs.contains(link.target);
                break;
            }
        }

        if (!validSource){
            String sourceMessage = String.format("Entry Ignored Because Source CSV: %s Does not contain ID: %s.", sourceFile, link.source);
            errorGenerator(connection.file, lineNumber, sourceMessage, errorText);
        }

        if (!validTarget){
            String targetMessage = String.format("Entry Ignored Because Target CSV: %s Does not contain ID: %s.", targetFile, link.target);
            errorGenerator(connection.file, lineNumber, targetMessage, errorText);
        } 
        
        return validSource && validTarget;
    }
    
    public List<Artifact> parseDataFiles(Tim tim, ErrorText errorText, String folderName) throws Exception {
        /* Parse Data Files */  
        List<Artifact> artifacts = new ArrayList<Artifact>(); 
        String RELATIVE_PATH = folderName + '/';
        
        for (DataFile d : tim.dataFiles) {
            String path = RELATIVE_PATH + d.file; 
            File dataFile = new File(path); 
            Scanner rowScanner = new Scanner(dataFile); 
            String headers = rowScanner.nextLine(); 
            String[] headersArray = headers.split(",");

            /* artifact to keep track of type and entries of each artifact */ 
            Artifact artifact = new Artifact(); 
            artifact.type = d.type;
            artifact.file = d.file;
            artifact.entries = new ArrayList<DataEntry>(); 
            artifact.uniqueIDs = new HashSet<String>();

            int index = 0; 
            int headerIndex = 0; 
            String temp = ""; 
            List<String> dataToAdd = new ArrayList<String>();
            int lineNumber = 1;

            while (rowScanner.hasNextLine()) {
                String data = rowScanner.nextLine();
                lineNumber++;
                index = 0; 
                
                while (headerIndex < 3) {      // if line ends but not enough fields, must be # 
                    if (Character.compare(data.charAt(index), '\"') == 0) {
                        index += 1;
                        while (Character.compare(data.charAt(index), '\"') != 0) {
                            temp += data.charAt(index);
                            index += 1; 
                            if (index >= data.length()) {
                                data = rowScanner.nextLine();
                                lineNumber++;

                                while (data.length() < 1) {
                                    data = rowScanner.nextLine();
                                    lineNumber++;
                                }
                                index = 0; 
                            }
                        }
                        headerIndex += 1;
                        index += 2;     // need to move past the following comma 
                        dataToAdd.add(temp); 
                        temp = ""; 
                    }
                    else if (Character.compare(data.charAt(index), ',') == 0) {
                        headerIndex += 1; 
                        index += 1;
                        dataToAdd.add(temp); 
                        temp = ""; 
                    }
                    else {
                        temp += data.charAt(index); 
                        index += 1; 
                    } 
                    if (index >= data.length()) {
                        dataToAdd.add(temp);       
                        temp = ""; 
                        headerIndex += 1; 
                        index = 0; 
                    }
                }
                DataEntry dataEntry = createDataEntry(headersArray, dataToAdd);
                if (artifact.uniqueIDs.contains(dataEntry.id)){
                    String message = String.format("Entry Ignored Because ID: %s Appears Earlier in CSV.", dataEntry.id);
                    errorGenerator(artifact.file, lineNumber, message, errorText);
                } else {
                    artifact.uniqueIDs.add(dataEntry.id);
                    artifact.entries.add(dataEntry); 
                }
                headerIndex = 0; 
                dataToAdd = new ArrayList<String>();
            }
            artifacts.add(artifact); 
            rowScanner.close(); 

        }

        return artifacts; 
    }

    public List<Connection> parseConnectionFiles(Tim tim, List<Artifact> artifacts, ErrorText errorText, String flatfileDir, String generatedDir) throws Exception {
        /* Parse TIM files */ 
        List<Connection> connections = new ArrayList<Connection>(); 

        for (LinkFile t : tim.linkFiles) {
            String path = "";
            Boolean generated = false;

            if (t.file.matches("\\/GENERATED\\/.*")) {
                generated = true;
                // System.out.println("GENERATED!");
                t.file = t.file.replace("/GENERATED/","");

                path = generatedDir + '/' + t.file;
            } else {
                path = flatfileDir + '/' + t.file;  
            }

            Connection connection   = new Connection(); 
            connection.name         = t.name;
            connection.file         = t.file;
            connection.sourceType   = t.source; 
            connection.targetType   = t.target;
            connection.links        = new ArrayList<Link>(); 

            
            File dataFile = new File(path); 
            Scanner rowScanner = new Scanner(dataFile); 
            String headers = rowScanner.nextLine(); 
            String[] headersArray = headers.split(",");
            
            int lineNumber = 2;

            while (rowScanner.hasNextLine()) {
                String data = rowScanner.nextLine(); 
                Link link = new Link(); 
                String[] dataArray = data.split(",");

                if (generated) {
                    Float score = Float.parseFloat(dataArray[2]);
                    // System.out.println(score);
                    if (score < 0.2) { // Skipped because score is less than threshold
                        // System.out.println("Skipped");
                        continue;
                    }
                }

                if (dataArray.length < 2) {     /* skip invalid lines - error report */
                    errorGenerator(connection.file, lineNumber, "Invalid Line: Missing columns. Expecting two columns.", errorText);
                    continue; 
                }

                /* Account for CSV Headers not always in same order */ 
                for (int i = 0; i < 2; i++) {
                    if (headersArray[i].toLowerCase().equals("source")) {
                        link.source = dataArray[i]; 
                    }
                    else if (headersArray[i].toLowerCase().equals("target")) {
                        link.target = dataArray[i]; 
                    }
                }
                
                link.sourceType = connection.sourceType; 
                link.targetType = connection.targetType; 
                if (linkValidator(connection, artifacts, link, errorText, lineNumber)){
                    connection.links.add(link); 
                }
                lineNumber++;
            }
            connections.add(connection); 
            rowScanner.close(); 
        } 

        return connections; 
    }

    public ParsedData parseFiles(String flatfileDir, String generatedDir) {
        
        ParsedData parsedData = new ParsedData();
        ErrorText errorText = new ErrorText();

        try {
            String timFileName = flatfileDir + '/' + "tim.json";
            Tim tim = parseTim(timFileName); 
            List<Artifact> artifacts = parseDataFiles(tim, errorText, flatfileDir);
            
            parsedData.artifacts = artifacts;
            parsedData.connections = parseConnectionFiles(tim, artifacts, errorText, flatfileDir, generatedDir);
            uniqueIDChecker(parsedData, errorText);

            String errorFileName = flatfileDir + '/' + "ErrorReport.txt";
            generateErrorReport(errorText.text, errorFileName);

            // Prints error file in terminal
            // try (BufferedReader br = new BufferedReader(new FileReader(errorFileName))) {
            //     String line;
            //     while ((line = br.readLine()) != null) {
            //         System.out.println(line);
            //     }
            //  }
            
            //generateInitialDirectories("testProject"); 
            //generateNextVersion("testProject", "nextVersionName"); 
        } catch(Exception e) {
            e.printStackTrace(); 
        }
        return parsedData; 

    }

    public void requiredDataChecker(String dir) throws Exception {
        String filename = dir + "/requiredData.json";
        File myDir = new File(filename);
    
        if (myDir.exists()){
            String data = readFileAsString(filename);
            Any iter = JsonIterator.deserialize(data);
    
            Any uploaded = iter.get("uploadedFiles");
            Any expected = iter.get("expectedFiles");
            Any generated = iter.get("generatedFiles");
            Any expectedGenerated = iter.get("expectedGeneratedFiles");
    
            Set<String> uploadedFiles = new HashSet<String>(); 
            Set<String> expectedFiles = new HashSet<String>();
            Set<String> generatedFiles = new HashSet<String>(); 
            Set<String> expectedGeneratedFiles = new HashSet<String>(); 
            
            for (Any i : uploaded) {
                uploadedFiles.add(i.toString());
            }

            for (Any i : expected) {
                expectedFiles.add(i.toString());
            }

            for (Any i : generated) {
                generatedFiles.add(i.toString());
            }

            for (Any i : expectedGenerated) {
                expectedGeneratedFiles.add(i.toString());
            }
            
            for (String name : expectedFiles){
                if (!uploadedFiles.contains(name)){
                    System.out.println("Throwing MissingFileException");
                    throw new MissingFileException(data);
                }
            }

            for (String name : expectedGeneratedFiles){
                if (!generatedFiles.contains(name)){
                    System.out.println("Throwing MissingFileException");
                    throw new MissingFileException(data);
                }
            }
        }
        else {
            System.out.println("Throwing Missing tim.json exception");
            throw new Exception("Missing tim.json file. Please upload files.");
        }
    }
}