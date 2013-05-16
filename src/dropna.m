function dset = dropna(dset)
  thr = 0.9 * length(dset);
  dropset = {};
  for v = dset.Properties.VarNames
    v = v{1};
    col = dset.(v);
    if isa(col, 'cell')
      c = sum(cell2mat(cellmap(@isna, col)));
    else
      c = sum(isnan(col));
    end
    if c > thr
      dropset{end + 1} = v;
    end
  end
  if not(isempty(dropset))
    dset = dropcols(dset, dropset);
  end    

  % TODO: drop null rows
