* structure/format of "input spreadsheets".
* structure/format of archive files (HDF5?).
* functionality required for processing input spreadsheets
** (comments on pandas)
* conventions for "fiduciary measurements" (aka "reference
  measurements"), such as controls, background


---


good
* the index (including multiindex)
* the special Series object: to be used for columns, index, etc.
* (groupby objects)

bad
* closed rather than half-open slices
* hierarchical columns

ugly
* ix


* inplace vs new
** technical: how to use views and/or garbage collection to reduce the
   memory requirements

* read excel, csv, tsv
* dropna

* rename columns
* reorder columns
* drop columns
* keep columns (drop all but the specified columns)
* apply

    seeded.cell_name = seeded.cell_name.apply(str.upper)

  (it'd be nice if apply for the Series object had an inplace option,
  so the above would be written as

    seeded.cell_name.apply(str.upper, inplace=True)

* set_index (including multiindex)
* reset_index (default index)

* modify columns:
** replace column: either set_column or directly assign to column
** append
** insert

* ???
    calibration = pd.DataFrame(calibration.stack()
                               .swaplevel(0, 1)
                               .sortlevel(), columns=[u'signal'])

* merge (i.e. like SQL's JOIN)
* groupby

* logical addressing
* splitting brick according to criterion
* filterobj

    def filterobj(test, obj):
      return obj[test(obj)]

    # filterobj(lambda x: x["mean"] >= 0,
    #           gb.xs(u'R', level=1) - gb.xs(u'L', level=1))


* assign replicates
* test for factoriality

