function out = fix_barcode(barcode)
  fmt = 'yyyymmddTHHMMSS';
  try
    out = datestr(x2mdate(str2double(barcode), 1), fmt);
  catch exc
    if not(strcmp(exc.identifier, 'MATLAB:datestr:ConvertDateNumber') && ...
           strcmp(exc.message, ['DATESTR failed converting date ' ...
                                'number to date vector.  Date number ' ...
                                'out of range.']))
       rethrow(exc)
    end
    try
      out = datestr(datenum(barcode, 'yyyy-mm-dd HH:MM:SS PM'), fmt);
    catch exc
      if not(strcmp(exc.identifier, 'MATLAB:datenum:ConvertDateString') && ...
             strcmp(exc.message, 'DATENUM failed.'))
        rethrow(exc)
      end
      out = barcode;
    end
  end
