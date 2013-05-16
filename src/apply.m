function dset = apply(fn, dset, varname)
  try
    dset.(varname) = cellmap(fn, dset.(varname));
  catch exc
    if not(strcmp(exc.identifier, 'MATLAB:cellfun:NotACell') && ...
           strcmp(exc.message, ['Input #2 expected to be a cell array, ' ...
                                'was double instead.']))
      rethrow(exc)
    end
    dset.(varname) = arraymap(fn, dset.(varname));
  end