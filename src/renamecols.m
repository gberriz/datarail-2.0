function dset = renamecols(dset, rule)
  dset.Properties.VarNames = mapcells(dset.Properties.VarNames, rule);
