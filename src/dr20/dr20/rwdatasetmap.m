function out = rwdatasetmap(fn, dset)
out = cellmap(fn, cellmap(@(i) dset(i, :), ...
                          num2cell((1:length(dset))')));
end
