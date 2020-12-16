package edu.nd.crc.safa.importer;

import java.io.File; 
import java.util.Scanner; 
import java.io.IOException; 
import java.util.*; 
import java.nio.file.*;
import java.io.FileWriter; 

import com.jsoniter.JsonIterator;

// import org.springframework.beans.factory.annotation.Autowired;
// import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class Flatfile {
    public static class Tim {
        List<DataFile> dataFiles; 
        List<LinkFile> linkFiles; 
    }

    public static class DataFile {
        public String type; 
        public String file; 
    }

    public static class LinkFile {
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

    public static String readFileAsString(String fileName) throws Exception { 
        String data = ""; 
        data = new String(Files.readAllBytes(Paths.get(fileName))); 
        return data; 
    }

    public static List<DataFile> readDatafile(JsonIterator iterator) throws Exception {
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

    public static LinkFile readLink(JsonIterator iterator, String linkName) throws Exception {
        LinkFile linkFile = new LinkFile();
        linkFile.name = linkName;
        for (String attr = iterator.readObject(); attr != null; attr = iterator.readObject()){
            if (attr.equals("Source")){
                linkFile.source = iterator.readString();
            } else if (attr.equals("Target")) {
                linkFile.target = iterator.readString();
            } else {
                linkFile.file = iterator.readString();
            }
        }
        return linkFile;
    }


    public static Tim parseTim(String fileName) throws Exception{
        String data = readFileAsString(fileName);
        JsonIterator iterator = JsonIterator.parse(data);
        Tim tim = new Tim();
        List<DataFile> dataFiles = new ArrayList<DataFile>();
        List<LinkFile> linkFiles = new ArrayList<LinkFile>();
        for (String field = iterator.readObject(); field != null; field = iterator.readObject()){
            if (field.equals("DataFiles")) {
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
            if (headersArray[i].equals("ID")) {
                dataEntry.id = data.get(i); 
            }
            else if (headersArray[i].equals("Summary")) {
                dataEntry.summary = data.get(i); 
            }
            else if (headersArray[i].equals("Content")) {
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
    
    public List<Artifact> parseDataFiles(Tim tim, ErrorText errorText) throws Exception {
        /* Parse Data Files */  
        List<Artifact> artifacts = new ArrayList<Artifact>(); 
        String RELATIVE_PATH = "flatfile_data/SAFA-DroneResponseData/";
        
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

    public List<Connection> parseConnectionFiles(Tim tim, List<Artifact> artifacts, ErrorText errorText) throws Exception {
        /* Parse TIM files */ 
        List<Connection> connections = new ArrayList<Connection>(); 

        for (LinkFile t : tim.linkFiles) {

            Connection connection   = new Connection(); 
            connection.name         = t.name;
            connection.file         = t.file;
            connection.sourceType   = t.source; 
            connection.targetType   = t.target;
            connection.links        = new ArrayList<Link>(); 

            String RELATIVE_PATH = "flatfile_data/SAFA-DroneResponseData/";
            String path = RELATIVE_PATH + t.file;  
            File dataFile = new File(path); 
            Scanner rowScanner = new Scanner(dataFile); 
            String headers = rowScanner.nextLine(); 
            String[] headersArray = headers.split(",");
            
            int lineNumber = 2;

            while (rowScanner.hasNextLine()) {
    
                String data = rowScanner.nextLine(); 
                Link link = new Link(); 
                String[] dataArray = data.split(",");

                if (dataArray.length < 2) {     /* skip invalid lines - error report */ 
                    continue; 
                }

                /* Account for CSV Headers not always in same order */ 
                for (int i = 0; i < 2; i++) {
                    if (headersArray[i].equals("Source")) {
                        link.source = dataArray[i]; 
                    }
                    else if (headersArray[i].equals("Target")) {
                        link.target = dataArray[i]; 
                    }
                }
                
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

    public ParsedData parseFiles(String fileName) {
        
        ParsedData parsedData = new ParsedData();
        ErrorText errorText = new ErrorText();

        try {
            Tim tim = parseTim(fileName); 
            List<Artifact> artifacts = parseDataFiles(tim, errorText);
            
            parsedData.artifacts = artifacts;
            parsedData.connections = parseConnectionFiles(tim, artifacts, errorText);
            uniqueIDChecker(parsedData, errorText);
            generateErrorReport(errorText.text, "flatfile_data/ErrorReport.txt"); 
            //generateInitialDirectories("testProject"); 
            //generateNextVersion("testProject", "nextVersionName"); 
        } catch(Exception e) {
            e.printStackTrace(); 
        }
        return parsedData; 

    }
}