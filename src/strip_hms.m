function out = fix_barcode(label)
out = regexprep(label, '_HMS$', '');
