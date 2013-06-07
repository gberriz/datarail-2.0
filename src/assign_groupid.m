function out = assign_groupid(dset, key, col, rcat, varargin)
  ip = inputParser;
  addRequired(ip, 'dset', @isdataset);
  addRequired(ip, 'key', @ischar);
  addRequired(ip, 'col', @ischar);
  addRequired(ip, 'rcat', @ischar);
  addParamValue(ip, 'default', '', @ischar);
  parse(ip, dset, key, col, rcat, varargin{:});

  default = ip.Results.default;
  havecol = ismember(col, dset.Properties.VarNames);
  memo = containers.Map();

  function gid = inner(v)
    rc = v.rcat{1};
    if isequal(rc, '0') || isequal(rc, rcat)
      k = v.(key){1};
      if ~isKey(memo, k)
        memo(k) = sprintf('%d', length(memo));
      end
      gid = memo(k);
    else
      if havecol
        gid = v.(col){1};
      else
        gid = false;
      end
      if ~gid
        gid = default;
      end
    end
  end

  out = rwdatasetmap(@inner, dset);
end
