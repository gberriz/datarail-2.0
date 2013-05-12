* The DICTIONARY

  Each project should have a global "dictionary" that serves to map
  project-internal nomenclature to nomenclature suitable for
  scientific communication.

  In its simplest form, a dictionary would consist of a table of
  key-value pairs.  The key would be the project-internal term, and
  the value would be an fully-specified referent suitable for use in
  publications to refer unambiguously to the entity in question.  The
  values (referents) of the keys may appear at most once in any
  dictionary.  This means that no referent (value) can be referred to
  by two different project-internal names (keys).

  (It would facilitate quality control if restrictions are imposed on
  the what is considered a valid key.  For example, the keys could be
  restricted to the lower-case letters a-z, the digits 0-9, and the
  underscore _.  In contrast, there would be few restrictions on what
  could be considered a valid value.  They could include whitespace,
  upper-case letters, punctuation, characters outside of the English
  alphabet, etc.)

  One possibly subtle/tricky issue is that the dictionary should not
  only include entries for entities such as the names of cell lines,
  and other reagents, but also for the names of the experimental
  factors themselves.  IOW, a project's dictionary would not only
  include pairs like, e.g.,

    ifngamma: Interferon-γ
    sirolimus: Rapamycin

  but also

    cell_line: Cell Lines
    small_molecule: Inhibitors
    protein: ligand
