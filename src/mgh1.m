% -*- mode: matlab -*-
basename = 'bl1';
basename = 'BreastLinesFirstBatch_MGHData_sent';
datapath = fullfile('/Users/berriz/Work/scratch/DR20/data', ...
                    sprintf('%s.xlsx', basename));
warning('off', 'MATLAB:codetools:ModifiedVarnames');
welldata = dataset('XLSFile', datapath, 'Sheet', 'WellDataMapped');

platedata = dataset('XLSFile', datapath, 'Sheet', 'PlateData');
calibration = dataset('XLSFile', datapath, 'Sheet', 'RefSeedSignal', ...
                      'Range', 'A2:V14');
seeded = dataset('XLSFile', datapath, 'Sheet', 'SeededNumbers');
warning('on', 'all');

%% --------------------------------------------------------------------------

calibration.Properties.VarNames{1} = ...
  normalize_label(calibration.Properties.VarNames{1});

% calibration = renamecols(calibration, ...
%                          containers.Map({'MCFDCIS_COM'}, {'MCF10DCIS_COM'}));

calibration = stack(calibration, ...
                    calibration.Properties.VarNames(1, 2:end), ...
                    'newDataVarName', 'signal');

calibration = renamecols(calibration, ...
                         containers.Map({'signal_Indicator'}, {'cell_line'}));

%% --------------------------------------------------------------------------

calibration = apply(@fix_cell_line, calibration, 'cell_line');

calibration = calibration(:, calibration.Properties.VarNames([2 1 3]));

calibration = sortrows(calibration, ...
  calibration.Properties.VarNames(1, 1:2), {'ascend', 'descend'});

calibration.cell_line = nominal(calibration.cell_line);

cls = transpose(cellstr(unique(calibration.cell_line)));
coeff_ca = cell(1, length(cls) + 1);
coeff_ca{1} = strsplit('cell_line intercept slope');
i = 2;
for c = cls
  cl = c{1};
  subds = calibration(calibration.cell_line==cl, ...
                      {'seed_cell_number_ml', 'signal'});
  cffs = coeffvalues(fit(double(subds.seed_cell_number_ml), ...
                         double(subds.signal), 'poly1'));
  coeff_ca{i} = [c num2cell(cffs)];
  i = i + 1;
end
coeff = cell2dataset(vertcat(coeff_ca{:}));
clear('cls', 'c', 'cl', 'subds', 'cffs', 'coeff_ca');

%% --------------------------------------------------------------------------

% cls = unique(calibration.cell_line)
% coeff_ca = cell(1, 
% for c = cellstr(unique(calibration.cell_line))'
%   cl = c{1};
%   subds = calibration(calibration.cell_line==cl, ...
%       {'seed_cell_number_ml', 'signal'});
%   cffs = coeffvalues(fit(double(subds.seed_cell_number_ml), ...
%                          double(subds.signal), 'poly1'));
% end

% coeff = LinearModel.fit(calibration, ...
%                         'CategoricalVars', ...
%                         calibration.Properties.VarNames{1}, ...
%                         'PredictorVars', ...
%                         calibration.Properties.VarNames{2}, ...
%                         'ResponseVar', ...
%                         calibration.Properties.VarNames{3});

%% --------------------------------------------------------------------------

seeded = renamecols(seeded, @normalize_label);
seeded = dropcols(seeded, strsplit('read_date cell_id'));
seeded = apply(@fix_barcode, seeded, 'barcode');
seeded = apply(@strip_hms, seeded, 'cell_line');

seeded = join(seeded, coeff, 'Type', 'fullouter');
clear('coeff');

%% --------------------------------------------------------------------------

platedata = renamecols(platedata, @normalize_label);

platedata.time = cellmap(@extract_time, platedata.protocol_name);
platedata = apply(@fix_barcode, platedata, 'barcode');

for s = strsplit('qcscore pass_fail manual_flag')
  platedata = apply(@maybe_to_int, platedata, s{1});
end

platedata = keepcols(platedata, strsplit(['barcode time qcscore pass_fail ', ...
                                          'manual_flag']));

%% --------------------------------------------------------------------------

welldata = renamecols(welldata, @normalize_label);
welldata = renamecols(welldata, containers.Map( ...
  strsplit('cell_name compound_no compound_conc'), ...
  strsplit('cell_line compound_number compound_concentration')));

welldata = dropna(welldata);

welldata = apply(@fix_barcode, welldata, 'barcode');

for s = strsplit('compound_number column')
  welldata = apply(@maybe_to_int, welldata, s{1});
end

welldata.rcat = mapcells(welldata.sample_code, containers.Map( ...
  strsplit('BDR BL CRL'), strsplit('1 2 3')), '0');

welldata.compound_concentration_log10 = ...
  arrayfun(@log10, welldata.compound_concentration);

welldata = dropcols(welldata, ...
                    strsplit(['cell_id well_id sample_code ' ...
                              'compound_concentration']));

%% --------------------------------------------------------------------------

welldata = join(welldata, seeded, 'Type', 'leftouter');
clear('seeded');

welldata = join(welldata, platedata, 'Type', 'leftouter');
clear('platedata');

%     welldata = pd.merge(welldata, platedata, on=u'barcode', how='left')
%     del platedata

%     def repgroup(v=None,
%                  _keycols=(u'rcat cell_line compound_number '
%                            u'compound_concentration_log10 time').split(),
%                  _memo=dict(),
%                  _reset=False):

%     welldata[u'replicate_group_id'] = welldata.apply(repgroup, axis=1)

%     bggroup = groupid_updater(u'barcode', u'background_id', BACKGROUND)
%     welldata[u'background_id'] = welldata.apply(bggroup, axis=1)
%     del bggroup

%     ctrlgroup = groupid_updater(u'barcode', u'control_id', CONTROL)
%     welldata[u'control_id'] = welldata.apply(ctrlgroup, axis=1)
%     del ctrlgroup

%     welldata = \
%       welldata.reindex_axis(
%         (u'rcat replicate_group_id background_id control_id '
%          u'cell_line compound_number compound_concentration_log10 time '
%          u'signal '
%          u'barcode seeding_density_cells_ml coefficient intercept '
%          u'estimated_seeding_signal row column modified created '
%          u'qcscore pass_fail manual_flag'.split()),
%         axis=1)

%     welldata.to_csv(tsv_path('test_dataset'), '\t',
%                     index=False,
%                     float_format='%.1f')

%% --------------------------------------------------------------------------


%     groups = transpose(cellstr(unique(ds.group)));
%     coeff_ca = cell(1, length(groups) + 1);
%     coeff_ca{1} = strsplit('group intercept slope');
%     i = 2;
%     for c = groups
%       subds = ds(ds.group == c{1}, {'x', 'y'});
%       cvs = coeffvalues(fit(double(subds.x), double(subds.y), 'poly1'));
%       coeff_ca{i} = [c num2cell(cvs)];
%       i = i + 1;
%     end
%     coeff = cell2dataset(vertcat(coeff_ca{:}));
