function out = cellmap(fn, cellarray)
out = cellfun(fn, cellarray, 'UniformOutput', false);
