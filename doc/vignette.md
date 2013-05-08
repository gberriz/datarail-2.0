(based on src/mgh1.py, a script to munge MGH dataset)

1. datasets = read_datasets('/path/to/file', format=tsv)

2. calibration = dataset.calibration
   calibration.rename_columns(callback_or_dict, inplace=True)

3. ??? calibration.pivot(...)
   calibration.rename_index(callback_or_string, inplace=True)

4. coeff = calibration.groupby('cell_name').ols(xcol='seed_cell_number_ml',
                                                ycol='signal')

5. seeded = dataset.seeded
   seeded.rename_columns(callback_or_dict, inplace=True)
   seeded.drop_columns(callback_or_sequence, inplace=True)

6. seeded.barcode.apply(fix_barcode, inplace=True)

7. seeded.join(coeff, on='cell_name', how='outer', inplace=True)

8. seeded.estimated_seeding_signal = \
        np.round(seeded.intercept +
                 seeded.seeding_density_cells_ml * seeded.coefficient)

9. platedata = dataset.platedata
   platedata.keep_columns(callback_or_sequence, inplace=True)

10. welldata = dataset.welldata
    ??? welldata.dropna(criterion_callback, how='all, inplace=True)
