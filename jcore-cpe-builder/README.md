### Known Issues
The JCoRe CPE Builder is only functional on a very basic level. Please see the [Issues](https://github.com/JULIELab/jcore-misc/issues) for information on what can and can't be done right now.
For instance the it won't let you build a pipeline that features the BioSEM Event Extractor as this component requires `Gene`s as input capabilities.
The only component that can provide this capability at the moment is `JNET`, but the output capability for this component is encoded in a more general `Type`, as this can be configured in several ways.
