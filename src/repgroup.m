function out = repgroup(dset, keycols)
  sep = native2unicode(28);
  n = length(dset);
  c = zeros(n);
  seen = containers.Map()
  for i = 1:n
    k = dataset2cell(dset(i, keycols));
    k = strjoin(k(2, :), sep);
    c(i) = seen(k) = mapget(seen, k, -1) + 1;
  end
