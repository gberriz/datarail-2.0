function out = repgroup(dset, keycols)
sep = native2unicode(28);
subds = dset(:, keycols);
clear('dset');
n = length(subds);
c = zeros(n, 'uint8');
seen = containers.Map();
for i = 1:n
  k = dataset2cell(subds(i, :));
  k = strjoin(cellmap(@num2str, k(2, :)), sep);
  r = mapget(seen, k, -1) + 1;
  c(i) = r;
  seen(k) = r;
end
out = arraymap(@num2str, c);
