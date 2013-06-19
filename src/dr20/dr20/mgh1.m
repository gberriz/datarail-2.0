% -*- mode: matlab -*-

% basename = 'bl1';
basename = 'BreastLinesFirstBatch_MGHData_sent';
datapath = fullfile(mfiledir(), '..', '..', '..', 'data', ...
                    sprintf('%s.xlsx', basename));
outpath = fullfile(mfiledir(), '..', '..', '..', ...
                   'dataframes', 'mgh', ...
                   sprintf('ml_%s.mat', basename));
clear basename;

%% ------------------------------------------------------------------------

warning('off', 'MATLAB:codetools:ModifiedVarnames');
welldata = dataset('XLSFile', datapath, 'Sheet', 'WellDataMapped');
platedata = dataset('XLSFile', datapath, 'Sheet', 'PlateData');
calibration = dataset('XLSFile', datapath, 'Sheet', 'RefSeedSignal', ...
                      'Range', 'A2:V14');
seeded = dataset('XLSFile', datapath, 'Sheet', 'SeededNumbers');
warning('on', 'all');
clear datapath;

%% ------------------------------------------------------------------------

calibration.Properties.VarNames{1} = ...
  normalize_label(calibration.Properties.VarNames{1});

calibration = stack(calibration, ...
                    calibration.Properties.VarNames(1, 2:end), ...
                    'newDataVarName', 'signal');

calibration = renamecols(calibration, ...
                         containers.Map({'signal_Indicator'}, ...
                                        {'cell_line'}));

%% ------------------------------------------------------------------------

calibration = apply(@fix_cell_line, calibration, 'cell_line');

calibration = calibration(:, calibration.Properties.VarNames([2 1 3]));

calibration = sortrows(calibration, ...
  calibration.Properties.VarNames(1, 1:2), {'ascend', 'descend'});

calibration.cell_line = nominal(calibration.cell_line);

cls = transpose(cellstr(unique(calibration.cell_line, 'stable')));
coeff_ca = cell(1, length(cls) + 1);
coeff_ca{1} = strsplit('cell_line slope intercept');
i = 2;
index = {'seed_cell_number_ml', 'signal'};
for c = cls
  subds = sortrows(calibration(calibration.cell_line==c{1}, index), ...
                   index{1});
  cffs = coeffvalues(fit(double(subds.seed_cell_number_ml(3:end)), ...
                         double(subds.signal(3:end)), 'poly1'));
  coeff_ca{i} = [c num2cell(cffs)];
  i = i + 1;
end
coeff = cell2dataset(vertcat(coeff_ca{:}));
clear i cls index csubds cffs coeff_ca calibration;

%% ------------------------------------------------------------------------

seeded = renamecols(seeded, @normalize_label);
seeded = dropcols(seeded, strsplit('read_date cell_id'));
seeded = apply(@fix_barcode, seeded, 'barcode');
seeded = apply(@strip_hms, seeded, 'cell_line');

seeded = join(seeded, coeff, 'Type', 'fullouter', 'MergeKeys', true);
clear coeff;

seeded.estimated_seeding_signal = ...
  round(seeded.intercept + ...
        seeded.seeding_density_cells_ml .* seeded.slope);

seeded.seeding_density_cells_ml = round(seeded.seeding_density_cells_ml);
seeded.intercept = roundp(seeded.intercept, 1);
seeded.slope = roundp(seeded.slope, 1);

%% ------------------------------------------------------------------------

platedata = renamecols(platedata, @normalize_label);

platedata.time = cellmap(@extract_time, platedata.protocol_name);

for s = strsplit('qcscore pass_fail manual_flag')
  platedata = apply(@maybe_to_int, platedata, s{1});
end
clear s;

platedata = keepcols(platedata, strsplit(['barcode time qcscore ', ...
                                          'pass_fail manual_flag']));

%% ------------------------------------------------------------------------

welldata = renamecols(welldata, @normalize_label);
welldata = renamecols(welldata, containers.Map( ...
  strsplit('cell_name compound_no compound_conc'), ...
  strsplit('cell_line compound_number compound_concentration')));

welldata = dropna(welldata);

%% ------------------------------------------------------------------------

for s = strsplit('compound_number column')
  welldata = apply(@maybe_to_int, welldata, s{1});
end
clear s;

welldata.rcat = mapcells(welldata.sample_code, containers.Map( ...
  strsplit('BDR BL CRL'), strsplit('1 2 3')), '0');

welldata.compound_concentration_log10 = ...
  arraymap(@(x) sprintf('%f', log10(x)), welldata.compound_concentration);

welldata = dropcols(welldata, ...
                    strsplit(['cell_id well_id sample_code ' ...
                              'compound_concentration']));

%% ------------------------------------------------------------------------

welldata = join(welldata, seeded, 'Type', 'leftouter', 'MergeKeys', true);
clear seeded;

welldata = join(welldata, platedata, 'Type', 'leftouter', 'MergeKeys', ...
                true);
clear platedata;

%% ------------------------------------------------------------------------

welldata.replicate_group_id = repgroup(welldata, ...
    strsplit(['rcat cell_line compound_number ' ...
              'compound_concentration_log10 time']));

welldata.background_id = ...
    assign_groupid(welldata, 'barcode', 'background_id', '2');

welldata.control_id = ...
    assign_groupid(welldata, 'barcode', 'control_id', '3');

welldata = ...
    welldata(:, strsplit(['rcat replicate_group_id background_id '...
                          'control_id cell_line compound_number ' ...
                          'compound_concentration_log10 time signal ' ...
                          'barcode seeding_density_cells_ml intercept ' ...
                          'slope estimated_seeding_signal row column ' ...
                          'modified created qcscore pass_fail ' ...
                          'manual_flag']));

%% ------------------------------------------------------------------------

% export(welldata, 'file', outpath);
save(outpath, 'welldata');
clear outpath;
