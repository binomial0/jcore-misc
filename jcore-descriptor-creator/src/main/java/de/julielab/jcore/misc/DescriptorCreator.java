package de.julielab.jcore.misc;

import static java.util.stream.Collectors.joining;
import static java.util.stream.Collectors.toList;

import java.io.File;
import java.io.IOException;
import java.io.Writer;
import java.lang.reflect.Modifier;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.apache.commons.lang.StringUtils;
import org.apache.uima.analysis_component.AnalysisComponent;
import org.apache.uima.analysis_engine.AnalysisEngineDescription;
import org.apache.uima.collection.CollectionReader;
import org.apache.uima.collection.CollectionReaderDescription;
import org.apache.uima.fit.factory.AnalysisEngineFactory;
import org.apache.uima.fit.factory.CollectionReaderFactory;
import org.apache.uima.resource.ResourceCreationSpecifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.xml.sax.SAXException;

import de.julielab.java.utilities.FileUtilities;
import io.github.lukehutch.fastclasspathscanner.FastClasspathScanner;

public class DescriptorCreator {


    public static final String DEFAULT_OUTPUT_ROOT = "src" + File.separator + "main" + File.separator + "resources";
    private static final Logger log = LoggerFactory.getLogger(DescriptorCreator.class);
    private static final String DESC = "desc";

    public static void main(String[] args) throws Exception {
        DescriptorCreator creator = new DescriptorCreator();
        creator.run();
    }

    public static String getComponentName() {
        return new File(".").getAbsoluteFile().getParentFile().getName();
    }

    public void run() throws Exception {
        run(DEFAULT_OUTPUT_ROOT);
    }

    public void run(String outputRoot) throws Exception {
        List<Class<? extends CollectionReader>> readers;
        List<Class<? extends AnalysisComponent>> aes;
        readers = findSubclasses(CollectionReader.class);
        aes = findSubclasses(AnalysisComponent.class);

        readers = readers.stream().filter(c -> c.getPackage().getName().contains("de.julielab.jcore.reader"))
                .collect(toList());
        // Since consumers and also multipliers can be or are AnalysisComponents, were may list all component categories here.
        // Also, remove abstract classes
        aes = aes.stream().filter(c -> (c.getModifiers() & Modifier.ABSTRACT) == 0).
                filter(c -> c.getPackage().getName().contains("de.julielab.jcore.ae")
                || c.getPackage().getName().contains("de.julielab.jcore.consumer")
                || c.getPackage().getName().contains("de.julielab.jcore.multiplier")
                || c.getPackage().getName().contains("de.julielab.jcore.reader")).collect(toList());

        if (readers.isEmpty() && aes.isEmpty()) {
            log.warn("No JCoRe UIMA component classes were found.");
        } else {
            if (readers.size() + aes.size() > 1) {
                log.warn(
                        "Multiple JCoRe UIMA component classes were found: {} {}. Multiple descriptors will be created with a running index. Manual curation will be required.",
                        readers, aes);
            }
            int num = 0;
            for (Class<? extends CollectionReader> cls : readers) {
                CollectionReaderDescription d = CollectionReaderFactory.createReaderDescription(cls);
                num += writeComponentDescriptor(outputRoot, cls, d, "collection reader", num);
            }
            for (Class<? extends AnalysisComponent> cls : aes) {
                AnalysisEngineDescription d = AnalysisEngineFactory.createEngineDescription(cls);
                num += writeComponentDescriptor(outputRoot, cls, d, "analysis engine / consumer", num);
            }
        }
    }

    private <T> List<Class<? extends T>> findSubclasses(Class<? extends T> cls) {
        List<Class<? extends T>> components;
        // consumers are also analysis components
        components = new ArrayList<>();
        FastClasspathScanner fcs = new FastClasspathScanner();
        fcs.matchClassesImplementing(cls, components::add).scan();
        return components;
    }

    private int writeComponentDescriptor(String outputRoot, Class<?> cls, ResourceCreationSpecifier d,
                                         String componentType, int num) throws SAXException, IOException {
        String componentName = null;
        if (d instanceof CollectionReaderDescription)
            componentName = ((CollectionReaderDescription) d).getImplementationName();
        if (d instanceof AnalysisEngineDescription)
            componentName = ((AnalysisEngineDescription) d).getImplementationName();
        if (StringUtils.isBlank(componentName))
            componentName = getComponentName();
        String filename = componentName;
        if (num > 0)
            filename += num;
        filename += ".xml";
        List<String> pathElements = Arrays.asList(outputRoot,
                cls.getPackage().getName().replaceAll("\\.", File.separator), DESC, filename);
        File outputPath = new File(pathElements.stream().collect(joining(File.separator)));
        if (!outputPath.getParentFile().exists())
            outputPath.getParentFile().mkdirs();
        log.info("Writing {} descriptor from class {} to {}", componentType, cls, outputPath);
        try (Writer w = FileUtilities.getWriterToFile(outputPath)) {
            d.toXML(w);
            ++num;
        }
        return num;
    }
}
