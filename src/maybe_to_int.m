function out = maybe_to_int(label)
  if isa(label, 'char')
    dbl = str2double(label);
    if isnan(dbl)
      out = label;
      return;
    end
  else
    dbl = label;
  end

  if round(dbl) == dbl
    out = sprintf('%d', dbl);
  else
    out = label;
  end
