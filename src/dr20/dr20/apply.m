function dset = apply(fn, dset, varname)
var = dset.(varname);
if isa(var, 'nominal')
  dset.(varname) = nominal(cellmap(fn, cellstr(var)));
elseif isa(var, 'cell')
  dset.(varname) = cellmap(fn, var);
else
  dset.(varname) = arraymap(fn, var);
end
