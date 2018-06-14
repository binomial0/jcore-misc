#set($symbol_pound='#')
#set($symbol_dollar='$')
#set($symbol_escape='\')

package ${package};

import org.apache.uima.collection.CollectionException;
import org.apache.uima.fit.component.JCasCollectionReader_ImplBase;
import org.apache.uima.jcas.JCas;
import org.apache.uima.UimaContext;
import org.apache.uima.resource.ResourceInitializationException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.apache.uima.util.Progress;
import org.apache.uima.util.ProgressImpl;

import java.io.IOException;

public class ${uimaReaderClassname} extends JCasCollectionReader_ImplBase {

	private final static Logger log = LoggerFactory.getLogger(${uimaReaderClassname}.class);

	/**
	 * This method is called a single time by the framework at component
	 * creation. Here, descriptor parameters are read and initial setup is done.
	 */
    @Override
    public void initialize(UimaContext context) throws ResourceInitializationException {
		super.initialize(context);
		// TODO
	}

	/**
	 * This method is called for each document going through the component. This
	 * is where the actual work happens.
	 */
    @Override
    public void getNext(JCas jCas) throws CollectionException {
		// TODO
	}

    @Override
    public void close() throws IOException {
        // TODO
    }

    @Override
    public Progress[] getProgress() {
        // TODO
        return new Progress[] { new ProgressImpl(0, 0, "TODO") };
    }

    @Override
    public boolean hasNext() throws IOException, CollectionException {
        // TODO
        return false;
    }

}
