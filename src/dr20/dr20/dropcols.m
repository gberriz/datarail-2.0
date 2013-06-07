function dset = dropcols(dset, dropset)
colset = dset.Properties.VarNames;
invalid = setdiff(dropset, colset);

if length(invalid) > 0
  error('DR20:dropcols:UnknownVarNames', ...
        'Unknown variable names: %s', strjoin(invalid, ', '));
end

dset = dset(:, setdiff(colset, dropset));
