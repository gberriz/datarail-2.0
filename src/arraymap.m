function out = arraymap(fn, dblarray)
  out = arrayfun(fn, dblarray, 'UniformOutput', false);
