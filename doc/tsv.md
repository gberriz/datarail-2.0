Format for spreadsheets (csv, tsv, excel)
=========================================

Each spreadsheet (or "sheet", for short) consists of a header followed
by a content section.

* The n-th row of the header describes the n-th column of the content
  section.  For example:
` `
    cell_line           string   factor        Name of the cell line
    kinase              string   factor        Name of the measured kinase, with phosphosite
    scan_intensity      float    confounder    Scanning intensity
    transfer_time       integer  confounder    Transfer time for the western blot
    date                string   confounder    Date of the experiment
    control_id          string   confounder    Control set identifier
    background_id       string   confounder    Background set identifier
    replicate_group_id  string   confounder    
    replicate_number    string   confounder    
    intensity           float    measurement   Signal intensity measured with the scanner

* As the example above shows, the rows of (the current version of) the
  header consist of four descriptors of the columns in the content
  section: name, type, category (descibed below), and description
  (optional).

* Therefore, the rows of the content section all have the same number of
  columns as there are rows in the header.

* The main purpose of the header is to *guide the parsing* of the file
  by programmatic tools.

* the columns of the header section are the following

** __name__ : lower-case letters, digits, and underscores only (no
   spaces, punctuation, parentheses, etc.); IOW, cell_line is a valid
   entry for this field, but all of the following are disallowed:

   cell line  
   CellLine
   cell-line

** __type__ : one of a controlled vocabulary of types; (the ones shown
   in the example above are the only ones we have needed so far, but
   additional types, such as date, may be added in the future.)

*** When assigning a type to a column of numeric data, give preference
    to integer over float whenever possible.  For example, a column
    holding the time at which a particular pertubation takes place, in
    minutes, and its possible values are 0, 10, 30, and 90, then this
    column should be given the integer type.  (The rationale for this
    is that floating point numbers introduce formatting and
    arithmetical complications, so it's best to avoid them whenever
    possible.)

** __category__ : this descriptor distinguishes those columns that
   contain measurements (i.e. the quantities that the experiment aims
   to ascertain), from those that contain metadata about those
   measurements; the latter, in turn, are divided into "factors" and
   "confounders".  Factors are variables in the model that motivates
   the experiment, while confounders are variables that are extraneous
   to this model.  Operationally, confounders are distinguished from
   factors in that the former are the part of the available
   information that the subsequent analysis either ignores or aims to
   "analyze away" (e.g. by averaging).

*** The set of factor columns (possibly supplemented by one or more
    replicate columns), serves as a "multikey" with which to identify
    each set of measurements.

*** Replicate numbers can be determined automatically (e.g. by
    sequentially assigning replicate numbers 1, 2, 3, etc., to all
    rows that have the same "signature" of factor values), or they can
    be explicitly provided.  If the latter is the case, this raises
    the question of how to encode into the format which replicates
    belong together.  The simplest scheme is to use the values in the
    factor columns as the criteria for grouping.


** __description__ : unstructured text.


** Open issues:
*** should all fields of the header be required to have some content,
    even if it is na?
*** candidate additional header fields:

**** display name (optional); e.g. "Cell line name" for the cell_line column
**** units (optional)

**** offset (optional)
**** multiplier (optional)
**** log base (optional)

**** allowable values (optional)
***** ordered enumeration for metadata fields; e.g. 0 10 30 90
***** list of special values for data fields; e.g. -Inf, NaN; possibly
      conditions such as > 0

*** especial "row of headers" between the header and content section
    to help connect the rows of the header with the columns of the
    content section;

* I object to making this row mandatory, because it introduces the
  potential for inconsistencies

* A compromise would be to make this row optional, but this would
  require some way to tell parsing programs that a given row was such
  an optional header row