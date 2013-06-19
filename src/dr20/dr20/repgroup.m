function out = repgroup(dset, keycols)

sub = dset(:, keycols);
clear dset;

% assumes that the sub-dataset of DSET specified by the varnames in
% KEYCOLS must consist entirely of strings.

cls = datasetmap(@(x) ...
    unique(cellmap(@class, x)), sub); cls = unique(cat(1, cls{:}));

if ~(length(cls) == 1 && isequal(cls{1}, 'char'))
  error('DR20:regroup:NotAllChar', ...
        'Not all values in KEYCOLS columns are of type ''char''');
end
clear cls;

sub = dataset2cell(sub); sub = sub(2:end, :);
n = length(sub);

keys = cell([n 1]);
key2id = containers.Map();
j = 0;
sep = native2unicode(28);
for i = 1:n
  k = CStr2String(sub(i, :), sep, false);
  keys{i} = k;
  if ~isKey(key2id, k)
    key2id(k) = sprintf('%d', j);
    j = j + 1;
  end
end
clear sub;

out = cellmap(@(x) key2id(x), keys);
