function out = mfilepath(varargin)
nvargs = length(varargin);

if nvargs > 1
  error('DR20:mfilepath:TooManyArguments', ...
        'requires at most 1 arguments');
end

if nvargs == 0
  offset = 0
else
  offset = varargin{1};
end

tmp = dbstack('-completenames');
out = tmp(1 + offset).file;
