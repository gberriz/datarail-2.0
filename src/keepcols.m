function dset = keepcols(dset, keepset)

  invalid = setdiff(keepset, dset.Properties.VarNames);

  if length(invalid) > 0
    error('DR20:keepcols:UnknownVarNames', ...
          'Unknown variable names: %s', strjoin(invalid, ', '));
  end

  dset = dset(:, keepset);
