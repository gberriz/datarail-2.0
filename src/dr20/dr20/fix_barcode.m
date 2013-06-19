function out = fix_barcode(barcode)

if barcode(1) == 'B'
  out = barcode;
else
  try
    dbl = datenum(barcode, 'yyyy-mm-dd HH:MM:SS PM');
  catch exc
    if not(strcmp(exc.identifier, 'MATLAB:datenum:ConvertDateString') && ...
           strcmp(exc.message, 'DATENUM failed.'))
      rethrow(exc)
    end
%     dbl = fixed_x2mdate(str2double(barcode), 0);
    error('DR20:fix_barcode:UnexpectedPattern', ...
          'Unexpected barcode pattern: %s', barcode);
  end
  out = fmt_date(dbl);
end
