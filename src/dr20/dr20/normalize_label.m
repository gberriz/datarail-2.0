function out = normalize_label(label)
  out = lower(regexprep(strtrim(label), ...
                        '\W|(?<=[^\WA-Z_])(?=[A-Z])', '_', ...
                        'emptymatch'));