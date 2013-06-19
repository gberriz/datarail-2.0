% -*- mode: matlab -*-
basename = 'CNI2_BASAL_2011';
datapath = fullfile(mfiledir(), '..', '..', '..', 'data', ...
                    sprintf('%s.xlsx', basename));
outpath = fullfile(mfiledir(), '..', '..', '..', ...
                   'dataframes', 'mgh', ...
                   sprintf('ml_%s.tsv', basename));
clear basename;

%% ------------------------------------------------------------------------
warning('off', 'MATLAB:codetools:ModifiedVarnames');
data = dataset('XLSFile', datapath);
warning('on', 'all');
clear datapath;

%% ------------------------------------------------------------------------

data.Properties.VarNames{1} = ...
  normalize_label(data.Properties.VarNames{1});

data = stack(data, ...
             data.Properties.VarNames(1, 2:end), ...
             'newDataVarName', 'level');

data = renamecols(data, ...
                  containers.Map({'level_Indicator'}, {'kinase'}));

data = apply(@fix_kinase, data, 'kinase');

%% ------------------------------------------------------------------------
export(data, 'file', outpath);
clear outpath;
