function dset = maybe_rename_varname(dset, fromname, toname)
  [present, idx] = ismember(fromname, dset.Properties.VarNames);
  if present
    dset.Properties.VarNames{idx} = toname;
  end
