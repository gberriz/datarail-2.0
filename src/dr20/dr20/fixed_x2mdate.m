function DateNumber = fixed_x2mdate(ExcelDateNumber, Convention)
%X2MDATE Excel Serial Date Number Form to MATLAB Serial Date Number Form
%
%   DateNumber = x2mdate(ExcelDateNumber, Convention)
%
%   Summary: This function converts serial date numbers from the Excel serial
%            date number format to the MATLAB serial date number format.
%
%   Inputs: ExcelDateNumber - Nx1 or 1xN vector of serial date numbers in
%           Excel serial date number form
%           Convention - Nx1 or 1xN vector or scalar flag value indicating
%              which date convention was used in Excel to convert the date
%              strings to serial date numbers; possible values are:
%              a) Convention = 0 - 1900 date system in which a serial date
%                 number of one corresponds to the date 1-Jan-1900
%                 (default).  Note: Excel erroneously treats the year 1900
%                 as a leap year, which we account for here.
%              b) Convention = 1 - 1904 date system in which a serial date
%                 number of zero corresponds to the date 1-Jan-1904
%
%   Outputs: Nx1 or 1xN vector of serial date numbers in MATLAB serial date
%            number form
%
%   Example: StartDate = 35746
%            Convention = 0;
%
%            EndDate = x2mdate(StartDate, Convention);
%
%            returns:
%
%            EndDate = 729706
%
%   See also M2XDATE.

%   Copyright 1995-2012 The MathWorks, Inc.

% Return empty if empty date input
if isempty(ExcelDateNumber)
    DateNumber = ExcelDateNumber;
    return
end

% Excel date number must be numeric.
if ~all(isnumeric(ExcelDateNumber(:)))
    error(message('finance:x2mdate:nonNumericInput'));
end

% Check the number of arguments in and set defaults
if nargin < 2
    Convention = zeros(size(ExcelDateNumber));
end

% Make sure input date numbers are positive
if any(ExcelDateNumber(:) <= 0)
    error(message('finance:x2mdate:invalidInputs'))
end

% Do any needed scalar expansion on the convention flag and parse
if any(size(Convention) ~= size(ExcelDateNumber)) && (max(size(Convention)) ~= 1)
    error(message('finance:x2mdate:invalidConventionFlagSize'))
elseif length(Convention(:)) == 1
    Convention = Convention * ones(size(ExcelDateNumber));
end

if any(Convention ~= 0 & Convention ~= 1)
    error(message('finance:x2mdate:invalidConventionFlag'))
end

% Get the shape of the input for later reshaping of the output
[RowSize, ColumnSize] = size(ExcelDateNumber);

% Set conversion factor for both (1900 & 1904) date systems
X2MATLAB1900 = 693961;
X2MATLAB1904 = 695422;

% Convert to the MATLAB serial date number
actual1900Idx = (Convention == 0) & (ExcelDateNumber < 61);
if any(actual1900Idx(:))
    Temp(actual1900Idx) = ExcelDateNumber(actual1900Idx) + X2MATLAB1900;
end

% Excel erroneously believes 1900 was a leap year, so after February 28,
% 1900, we adjust to account for this.
corrected1900Idx = (Convention == 0) & (ExcelDateNumber >= 61);
if any(corrected1900Idx(:))
    Temp(corrected1900Idx) = ExcelDateNumber(corrected1900Idx) + X2MATLAB1900 - 1;
end

% Using the 1904 convention there is no issue with the incorrect leap year.
y1904Idx = find(Convention == 1);
if any(y1904Idx(:))
    Temp(y1904Idx) = ExcelDateNumber(y1904Idx) + X2MATLAB1904;
end

% Reshape the output
DateNumber = reshape(Temp, RowSize, ColumnSize);
