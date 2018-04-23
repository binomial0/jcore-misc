package de.julielab.jcore.misc;

import static java.util.stream.Collectors.joining;
import static org.junit.Assert.assertTrue;

import java.io.File;
import java.io.IOException;
import java.util.Arrays;
import java.util.Optional;
import java.util.stream.Stream;

import org.apache.commons.io.FileUtils;
import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.Test;

public class DescriptorCreatorTest {
	
	@BeforeClass
	@AfterClass
	public static void shutdown() throws IOException {
		FileUtils.deleteDirectory(new File(Arrays.asList("src", "test", "resources", "de").stream().collect(joining(File.separator))));
	}
	@Test
	public void testRun() throws Exception {
		DescriptorCreator creator = new DescriptorCreator();
		String outputRoot = "src" + File.separator + "test" + File.separator + "resources" + File.separator;
		creator.run(outputRoot);	
		File crDir = new File(outputRoot + Stream.of("de", "julielab", "jcore", "reader", "testreader", "desc").collect(joining(File.separator)));
		File aeDir = new File(outputRoot + Stream.of("de", "julielab", "jcore", "ae", "testae", "desc").collect(joining(File.separator)));
		File consumerDir = new File(outputRoot + Stream.of("de", "julielab", "jcore", "consumer", "testconsumer", "desc").collect(joining(File.separator)));
		
		assertTrue(crDir.exists());
		assertTrue(aeDir.exists());
		assertTrue(consumerDir.exists());
		
		assertTrue(containsDescriptor(crDir));
		assertTrue(containsDescriptor(aeDir));
		assertTrue(containsDescriptor(consumerDir));
	}

	private boolean containsDescriptor(File dir) {
		return Stream.of(dir.list()).filter(f -> f.contains(".xml")).findAny().isPresent();
	}
}
