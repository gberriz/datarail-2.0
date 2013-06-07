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
sep = native2unicode(28);
for i = 1:n
  keys{i} = CStr2String(sub(i), sep, false);
end
clear sub;

ukeys = unique(keys);
seen = containers.Map(ukeys, zeros(length(ukeys), 1, 'uint8') - 1);
clear ukeys;

c = zeros(n, 1, 'uint8');
for i = 1:n
  k = keys{i};
  r = seen(k) + 1;
  c(i) = r;
  seen(k) = r;
end

out = arraymap(@(x) sprintf('%d', x), c);
