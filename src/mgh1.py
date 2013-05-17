if True:

    import warnings as wrn
    import exceptions as exc
    wrn.filterwarnings(u'ignore',
                       message=ur'.*with\s+inplace=True\s+will\s+return\s+None',
                       category=exc.FutureWarning,
                       module=u'pandas')

    import os.path as op
    import pandas as pd
    # from pandas import DataFrame as df, Series as se
    from pandas import Series as se
    # import matplotlib.pyplot as plt
    import numpy as np
    import math as ma
    import sys
    import datetime as dt

    import re

    DATA = u'0'
    DISCARD = u'1'
    BACKGROUND = u'2'
    CONTROL = u'3'
    SEEDING = u'4'

    BASEDIR = op.abspath(op.join(op.dirname(__file__), u'..'))

    # NOTE: for a reduced dataset, pass bl1 as the script's argument
    DEFAULT_BASENAME = u'BreastLinesFirstBatch_MGHData_sent'

    def dropcols(df, colnames):
        return df.drop(colnames.split()
                       if hasattr(colnames, 'split')
                       else colnames, axis=1)

    def dropna(df):
        # require that at least 10% of any column be non-na's
        return df.dropna(axis=1, thresh=len(df)//10).dropna(axis=0, how='all')

    def fix_barcode(b):
        try:
            d = dt.datetime.strptime(b, u'%Y-%m-%d %I:%M:%S %p')
        except (ValueError, TypeError), e:
            msg = unicode(e)
            if (u'does not match format' not in msg and
                u'must be string, not datetime.datetime' not in msg):
                raise
            d = b

        try:
            b = dt.datetime.strftime(d, u'%Y%m%dT%H%M%S')
        except TypeError, e:
            if (u"descriptor 'strftime' requires a 'datetime.date' object "
                u"but received a 'unicode'" not in unicode(e)):
                raise

        return b

    def get_datapath(basedir=BASEDIR):
        datadir = op.join(basedir, u'data')

        args = sys.argv[1:]
        nargs = len(args)
        assert nargs < 2
        filename = '%s.xlsx' % (args[0] if nargs == 1 else DEFAULT_BASENAME)
        return op.join(datadir, filename)

    def groupid_updater(key, col, rcat, default=u''):
        memo=dict()
        def groupid(v=None, _reset=False):
            if _reset: return memo.clear()
            rc = v[u'rcat']
            return (memo.setdefault(v[key], unicode(len(memo)))
                    if (rc == DATA or rc == rcat) else v.get(col, default))

        return groupid

    def keepcols(df, colnames):
        keepset = set(colnames.split()
                      if hasattr(colnames, 'split')
                      else colnames)
        colset = set(df.columns)
        invalid = ' '.join(tuple(keepset.difference(colset)))
        if invalid != '':
            raise ValueError('labels [%s] not contained in axis=1' % invalid)

        return dropcols(df, list(colset.difference(keepset)))

    def log10(s):
        f = float(s)
        return (u'-inf' if f == 0.0 else
                unicode(round(ma.log10(f), 1)))

    def maybe_to_int(x):
        try:
            f = float(x)
            i = int(round(f))
            if f != float(i):
                i = f
        except ValueError, e:
            i = x
        return unicode(i)

    def normalize_label(label,
                        _cleanup_re=re.compile(ur'\W+|(?<=[^\WA-Z_])'
                                               ur'(?=[A-Z])')):
        return (u'none_0' if label is None
                else _cleanup_re.sub(u'_', unicode(label).strip()).lower())

    def regress(df, index=pd.Index((u'coefficient', u'intercept'))):
        xcol = u'seed_cell_number_ml'
        ycol = u'signal'
        sdf = df.sort(columns=[xcol], axis=0)
        # ols = "ordinary least squares"
        ret = pd.ols(x=sdf[xcol][2:], y=sdf[ycol][2:]).beta
        ret.index = index
        return ret

    def repgroup(v=None,
                 _keycols=(u'rcat cell_line compound_number '
                           u'compound_concentration_log10 time').split(),
                 _memo=dict(),
                 _reset=False):
       if _reset: return _memo.clear()
       return _memo.setdefault(tuple(v[_keycols]), unicode(len(_memo)))

    def tsv_path(name, _outputdir=op.join(BASEDIR, u'dataframes/mgh')):
        return op.join(_outputdir, u'%s.tsv' % name)

# ---------------------------------------------------------------------------

    # READING IN THE DATA FROM DISK
    ## 1. datasets = read_datasets('/path/to/file', format=tsv)

    datapath = get_datapath()
    print u'reading data from %s...\t' % datapath,; sys.stdout.flush()
    workbook = pd.ExcelFile(str(datapath))
    del datapath

    welldata = workbook.parse(u'WellDataMapped')

    platedata = workbook.parse(u'PlateData')
    calibration = workbook.parse(u'RefSeedSignal', header=1, skiprows=[0],
                                 skip_footer=7)
    seeded = workbook.parse(u'SeededNumbers')
    del workbook

    print u'done'

# ---------------------------------------------------------------------------

    # CLEANUP CALIBRATION DF

    # At this point, the calibration df looks like this:
    #
    # In [83]: calibration
    # Out[83]: 
    # <class 'pandas.core.frame.DataFrame'>
    # Int64Index: 12 entries, 0 to 11
    # Data columns:
    # Seed cell number/ ml     12  non-null values
    # AU-565                   12  non-null values
    # BT-20                    12  non-null values
    # BT-474                   12  non-null values
    # CAMA-1                   12  non-null values
    # DU-4475                  12  non-null values
    # HCC-1187                 12  non-null values
    # HCC-1395                 12  non-null values
    # HCC-1419                 12  non-null values
    # HCC-1569                 12  non-null values
    # HCC-1806                 12  non-null values
    # HCC-1937                 12  non-null values
    # HCC-1954                 12  non-null values
    # HCC-202                  12  non-null values
    # HCC-2218                 12  non-null values
    # HCC-38                   12  non-null values
    # HCC-70                   12  non-null values
    # MCF7                     12  non-null values
    # MCFDCIS.COM              12  non-null values
    # MDA-MB-361               12  non-null values
    # SK-BR-3                  12  non-null values
    # ZR-75-1                  12  non-null values
    # dtypes: float64(22)


    ## 2. calibration = dataset.calibration
    ##    calibration.rename_columns(callback_or_dict, inplace=True)

    calibration.rename(columns={calibration.columns[0]:
                                    normalize_label(calibration.columns[0])},
                       inplace=True)
    calibration.rename(columns={u'MCFDCIS.COM': u'MCF10DCIS.COM'},
                       inplace=True)

    # At this point, the calibration df looks like this:
    #
    # In [90]: calibration
    # Out[90]: 
    # <class 'pandas.core.frame.DataFrame'>
    # Int64Index: 12 entries, 0 to 11
    # Data columns:
    # seed_cell_number_ml    12  non-null values
    # AU-565                 12  non-null values
    # BT-20                  12  non-null values
    # BT-474                 12  non-null values
    # CAMA-1                 12  non-null values
    # DU-4475                12  non-null values
    # HCC-1187               12  non-null values
    # HCC-1395               12  non-null values
    # HCC-1419               12  non-null values
    # HCC-1569               12  non-null values
    # HCC-1806               12  non-null values
    # HCC-1937               12  non-null values
    # HCC-1954               12  non-null values
    # HCC-202                12  non-null values
    # HCC-2218               12  non-null values
    # HCC-38                 12  non-null values
    # HCC-70                 12  non-null values
    # MCF7                   12  non-null values
    # MCF10DCIS.COM          12  non-null values
    # MDA-MB-361             12  non-null values
    # SK-BR-3                12  non-null values
    # ZR-75-1                12  non-null values
    # dtypes: float64(22)

# ---------------------------------------------------------------------------

    # RESTRUCTURE CALIBRATION DF
    ## 3. ??? calibration.pivot(...)
    ##    calibration.rename_index(callback_or_string, inplace=True)
    calibration = calibration.set_index(calibration.columns[0]).stack()

    # At this point, the calibration df looks like this:
    #
    # In [103]: calibration
    # Out[103]: 
    # seed_cell_number_ml          
    # 100000               AU-565       78860
    #                      BT-20        72860
    #                      BT-474       69704
    #                      CAMA-1       72368
    #                      DU-4475      30296
    #                      HCC-1187     54812
    #                      HCC-1395     50228
    #                      HCC-1419    120692
    #                      HCC-1569    123860
    #                      HCC-1806     62216
    #                      HCC-1937    125140
    #                      HCC-1954     73392
    #                      HCC-202      66912
    #                      HCC-2218    155772
    #                      HCC-38      111900
    # ...
    # 48.828125            HCC-1395          56
    #                      HCC-1419         172
    #                      HCC-1569         184
    #                      HCC-1806          64
    #                      HCC-1937         164
    #                      HCC-1954          48
    #                      HCC-202           80
    #                      HCC-2218          32
    #                      HCC-38            56
    #                      HCC-70            16
    #                      MCF7              28
    #                      MCF10DCIS.COM     88
    #                      MDA-MB-361        92
    #                      SK-BR-3           84
    #                      ZR-75-1          180
    # Length: 252

    calibration = calibration.swaplevel(0, 1)

    # At this point, the calibration df looks like this:
    #
    # In [105]: calibration
    # Out[105]: 
    #           seed_cell_number_ml
    # AU-565    100000                  78860
    # BT-20     100000                  72860
    # BT-474    100000                  69704
    # CAMA-1    100000                  72368
    # DU-4475   100000                  30296
    # HCC-1187  100000                  54812
    # HCC-1395  100000                  50228
    # HCC-1419  100000                 120692
    # HCC-1569  100000                 123860
    # HCC-1806  100000                  62216
    # HCC-1937  100000                 125140
    # HCC-1954  100000                  73392
    # HCC-202   100000                  66912
    # HCC-2218  100000                 155772
    # HCC-38    100000                 111900
    # ...
    # HCC-1395       48.828125               56
    # HCC-1419       48.828125              172
    # HCC-1569       48.828125              184
    # HCC-1806       48.828125               64
    # HCC-1937       48.828125              164
    # HCC-1954       48.828125               48
    # HCC-202        48.828125               80
    # HCC-2218       48.828125               32
    # HCC-38         48.828125               56
    # HCC-70         48.828125               16
    # MCF7           48.828125               28
    # MCF10DCIS.COM  48.828125               88
    # MDA-MB-361     48.828125               92
    # SK-BR-3        48.828125               84
    # ZR-75-1        48.828125              180
    # Length: 252

    calibration = calibration.sortlevel()

    # At this point, the calibration df looks like this:
    #
    # In [107]: calibration
    # Out[107]: 
    #         seed_cell_number_ml
    # AU-565  100000.000000          78860
    #         50000.000000           33868
    #         25000.000000           21608
    #         12500.000000           10584
    #         6250.000000             6092
    #         3125.000000             2652
    #         1562.500000             1404
    #         781.250000               552
    #         390.625000               392
    #         195.312500               172
    #         97.656250                 68
    #         48.828125                 52
    # BT-20   100000.000000          72860
    #         50000.000000           35092
    #         25000.000000           19948
    # ...
    # SK-BR-3  195.312500                472
    #          97.656250                 200
    #          48.828125                  84
    # ZR-75-1  100000.000000          129812
    #          50000.000000            61732
    #          25000.000000            35596
    #          12500.000000            20520
    #          6250.000000             11828
    #          3125.000000              6448
    #          1562.500000              3396
    #          781.250000               1940
    #          390.625000                816
    #          195.312500                364
    #          97.656250                 164
    #          48.828125                 180
    # Length: 252

    calibration = pd.DataFrame(calibration, columns=[u'signal'])

    # At this point, the calibration df looks like this:
    #
    # In [109]: calibration
    # Out[109]: 
    # <class 'pandas.core.frame.DataFrame'>
    # MultiIndex: 252 entries, (AU-565, 100000.0) to (ZR-75-1, 48.828125)
    # Data columns:
    # signal    252  non-null values
    # dtypes: float64(1)

    calibration.index.names[0] = u'cell_line'

    # At this point, the calibration df looks like this:
    #
    # In [111]: calibration
    # Out[111]: 
    # <class 'pandas.core.frame.DataFrame'>
    # MultiIndex: 252 entries, (AU-565, 100000.0) to (ZR-75-1, 48.828125)
    # Data columns:
    # signal    252  non-null values
    # dtypes: float64(1)

    calibration.reset_index(inplace=True)

    # <class 'pandas.core.frame.DataFrame'>
    # Int64Index: 252 entries, 0 to 251
    # Data columns:
    # cell_line              252  non-null values
    # seed_cell_number_ml    252  non-null values
    # signal                 252  non-null values
    # dtypes: float64(2), object(1)

# ---------------------------------------------------------------------------
    # COMPUTE REGRESSION
    ## 4. coeff = calibration.groupby('cell_line').ols(xcol='seed_cell_number_ml',
    ##                                                 ycol='signal')

    coeff = calibration.groupby(u'cell_line').apply(regress)
    del calibration

    #                coefficient    intercept
    # cell_line                              
    # AU-565            0.768691   259.587801
    # BT-20             0.715104  1003.095948
    # BT-474            0.665241  1454.570673
    # CAMA-1            0.710518  2016.311377
    # DU-4475           0.297694   865.542404
    # HCC-1187          0.540053   -12.907952
    # HCC-1395          0.491397   326.059323
    # HCC-1419          1.181097  3235.927030
    # HCC-1569          1.212983  2711.226292
    # HCC-1806          0.591247   594.609107
    # HCC-1937          1.199830  2056.426124
    # HCC-1954          0.714895  1535.265283
    # HCC-202           0.651251   320.896811
    # HCC-2218          1.489807  2118.558418
    # HCC-38            1.091150   841.510096
    # HCC-70            0.805700    77.731792
    # MCF10DCIS.COM     0.771817  1663.525971
    # MCF7              0.803097  1342.555076
    # MDA-MB-361        0.476176  1068.589890
    # SK-BR-3           0.770801   899.026876
    # ZR-75-1           1.270914  1851.751010

    coeff.reset_index(inplace=True)

    #         cell_line  coefficient    intercept
    # 0          AU-565     0.768691   259.587801
    # 1           BT-20     0.715104  1003.095948
    # 2          BT-474     0.665241  1454.570673
    # 3          CAMA-1     0.710518  2016.311377
    # 4         DU-4475     0.297694   865.542404
    # 5        HCC-1187     0.540053   -12.907952
    # 6        HCC-1395     0.491397   326.059323
    # 7        HCC-1419     1.181097  3235.927030
    # 8        HCC-1569     1.212983  2711.226292
    # 9        HCC-1806     0.591247   594.609107
    # 10       HCC-1937     1.199830  2056.426124
    # 11       HCC-1954     0.714895  1535.265283
    # 12        HCC-202     0.651251   320.896811
    # 13       HCC-2218     1.489807  2118.558418
    # 14         HCC-38     1.091150   841.510096
    # 15         HCC-70     0.805700    77.731792
    # 16  MCF10DCIS.COM     0.771817  1663.525971
    # 17           MCF7     0.803097  1342.555076
    # 18     MDA-MB-361     0.476176  1068.589890
    # 19        SK-BR-3     0.770801   899.026876
    # 20        ZR-75-1     1.270914  1851.751010

# ---------------------------------------------------------------------------

    # CLEANUP SEEDED DF
    ## 5. seeded = dataset.seeded
    ##    seeded.rename_columns(callback_or_dict, inplace=True)
    ##    seeded.drop_columns(callback_or_sequence, inplace=True)

    # In [115]: seeded
    # Out[115]: 
    # <class 'pandas.core.frame.DataFrame'>
    # Int64Index: 332 entries, 0 to 331
    # Data columns:
    # ReadDate                    332  non-null values
    # CellID                      332  non-null values
    # CellLine                    332  non-null values
    # Barcode                     332  non-null values
    # seeding density cells/ml    332  non-null values
    # dtypes: float64(2), object(3)

    seeded.rename(columns=normalize_label, inplace=True)
    # seeded.rename(columns={u'cell_line': u'cell_name'}, inplace=True)
    seeded = dropcols(seeded, u'read_date cell_id')

    ## 6. seeded.barcode.apply(fix_barcode, inplace=True)

    # fix malformed barcodes
    seeded.barcode = seeded.barcode.apply(fix_barcode)

    # remove the '_HMS' suffix from cell-line names
    hmssfx_re = re.compile(ur'_HMS$')
    seeded.cell_line = seeded.cell_line.apply(lambda s: hmssfx_re.sub(u'', s))
    del hmssfx_re

    # In [117]: seeded
    # Out[117]: 
    # <class 'pandas.core.frame.DataFrame'>
    # Int64Index: 332 entries, 0 to 331
    # Data columns:
    # cell_line                   332  non-null values
    # barcode                     332  non-null values
    # seeding_density_cells_ml    332  non-null values
    # dtypes: float64(1), object(2)

# ---------------------------------------------------------------------------

    # UPDATE SEEDED DF WITH INFO FROM CALIBRATION DF
    ## 7. seeded.join(coeff, on='cell_line', how='outer', inplace=True)

    seeded = pd.merge(seeded, coeff, on=u'cell_line', how='outer')
    del coeff

    # In [157]: seeded
    # Out[157]: 
    # <class 'pandas.core.frame.DataFrame'>
    # Int64Index: 332 entries, 0 to 331
    # Data columns:
    # cell_line                   332  non-null values
    # barcode                     332  non-null values
    # seeding_density_cells_ml    332  non-null values
    # coefficient                 318  non-null values
    # intercept                   318  non-null values
    # dtypes: float64(3), object(2)

    ## 8. seeded.estimated_seeding_signal = \
    ##         np.round(seeded.intercept +
    ##                  seeded.seeding_density_cells_ml * seeded.coefficient)

    seeded[u'estimated_seeding_signal'] = \
        np.round(seeded.intercept +
                 seeded.seeding_density_cells_ml * seeded.coefficient)

    # In [159]: seeded
    # Out[159]: 
    # <class 'pandas.core.frame.DataFrame'>
    # Int64Index: 332 entries, 0 to 331
    # Data columns:
    # cell_line                   332  non-null values
    # barcode                     332  non-null values
    # seeding_density_cells_ml    332  non-null values
    # coefficient                 318  non-null values
    # intercept                   318  non-null values
    # estimated_seeding_signal    318  non-null values
    # dtypes: float64(4), object(2)

    seeded = dropcols(seeded, [u'cell_line'])

    # In [161]: seeded
    # Out[161]: 
    # <class 'pandas.core.frame.DataFrame'>
    # Int64Index: 332 entries, 0 to 331
    # Data columns:
    # barcode                     332  non-null values
    # seeding_density_cells_ml    332  non-null values
    # coefficient                 318  non-null values
    # intercept                   318  non-null values
    # estimated_seeding_signal    318  non-null values
    # dtypes: float64(4), object(1)

# ---------------------------------------------------------------------------

    # CLEANUP PLATEDATA

    # In [162]: platedata
    # Out[162]: 
    # <class 'pandas.core.frame.DataFrame'>
    # Int64Index: 332 entries, 0 to 331
    # Data columns:
    # Barcode          332  non-null values
    # CellID           332  non-null values
    # Filename         332  non-null values
    # AssayID          332  non-null values
    # ReadDate         332  non-null values
    # ReadTime         332  non-null values
    # ProtocolID       332  non-null values
    # ProtocolName     332  non-null values
    # Rows             332  non-null values
    # Columns          332  non-null values
    # Wells            332  non-null values
    # ReaderSN         332  non-null values
    # ExportSW         332  non-null values
    # Notifications    1  non-null values
    # Modified         332  non-null values
    # Created          332  non-null values
    # QCScore          332  non-null values
    # PassFail         240  non-null values
    # Manual Flag      332  non-null values
    # dtypes: float64(8), object(11)

    platedata.rename(columns=normalize_label, inplace=True)

    # In [163]: platedata
    # Out[163]: 
    # <class 'pandas.core.frame.DataFrame'>
    # Int64Index: 332 entries, 0 to 331
    # Data columns:
    # barcode          332  non-null values
    # cell_id          332  non-null values
    # filename         332  non-null values
    # assay_id         332  non-null values
    # read_date        332  non-null values
    # read_time        332  non-null values
    # protocol_id      332  non-null values
    # protocol_name    332  non-null values
    # rows             332  non-null values
    # columns          332  non-null values
    # wells            332  non-null values
    # reader_sn        332  non-null values
    # export_sw        332  non-null values
    # notifications    1  non-null values
    # modified         332  non-null values
    # created          332  non-null values
    # qcscore          332  non-null values
    # pass_fail        240  non-null values
    # manual_flag      332  non-null values
    # dtypes: float64(8), object(11)

    # PANDAS BUG: the following fails silently (no 'time' column is created):
    # platedata.time = platedata.protocol_name.apply(lambda s: s[-4])

    platedata[u'time'] = platedata.protocol_name.apply(lambda s: s[-4])
    platedata.barcode = platedata.barcode.apply(fix_barcode)

    for c in u'qcscore pass_fail manual_flag'.split():
        platedata[c] = platedata[c].apply(maybe_to_int)

    ## 9. platedata = dataset.platedata
    ##    platedata.keep_columns(callback_or_sequence, inplace=True)

    platedata = keepcols(platedata,
                         u'barcode time qcscore pass_fail manual_flag')

    # In [165]: platedata
    # Out[165]: 
    # <class 'pandas.core.frame.DataFrame'>
    # Int64Index: 332 entries, 0 to 331
    # Data columns:
    # barcode        332  non-null values
    # qcscore        332  non-null values
    # pass_fail      240  non-null values
    # manual_flag    332  non-null values
    # time           332  non-null values
    # dtypes: float64(2), object(3)

# ---------------------------------------------------------------------------

    # CLEANUP WELLDATA

    # In [176]: welldata
    # Out[176]: 
    # <class 'pandas.core.frame.DataFrame'>
    # Int64Index: 127488 entries, 0 to 127487
    # Data columns:
    # Barcode         127488  non-null values
    # Cell ID         127488  non-null values
    # Cell Name       127488  non-null values
    # WellID          127488  non-null values
    # Row             127488  non-null values
    # Column          127488  non-null values
    # Sample_Code     127488  non-null values
    # CompoundNo      127488  non-null values
    # CompoundConc    127488  non-null values
    # Signal          127488  non-null values
    # Modified        127488  non-null values
    # Created         127488  non-null values
    #                 0  non-null values
    # None.1          0  non-null values
    # None.2          0  non-null values
    # None.3          0  non-null values
    # None.4          0  non-null values
    # None.5          1  non-null values
    # dtypes: float64(10), object(8)

    welldata.rename(columns=normalize_label, inplace=True)
    welldata.rename(columns=dict(cell_name=u'cell_line',
                                 compound_no=u'compound_number',
                                 compound_conc=u'compound_concentration'),
                    inplace=True)

    # In [182]: welldata
    # Out[182]: 
    # <class 'pandas.core.frame.DataFrame'>
    # Int64Index: 127488 entries, 0 to 127487
    # Data columns:
    # barcode                   127488  non-null values
    # cell_id                   127488  non-null values
    # cell_line                 127488  non-null values
    # well_id                   127488  non-null values
    # row                       127488  non-null values
    # column                    127488  non-null values
    # sample_code               127488  non-null values
    # compound_number           127488  non-null values
    # compound_concentration    127488  non-null values
    # signal                    127488  non-null values
    # modified                  127488  non-null values
    # created                   127488  non-null values
    # none_0                    0  non-null values
    # none_1                    0  non-null values
    # none_2                    0  non-null values
    # none_3                    0  non-null values
    # none_4                    0  non-null values
    # none_5                    1  non-null values
    # dtypes: float64(10), object(8)

    ## 10. welldata = dataset.welldata
    ##     ??? welldata.dropna(criterion_callback, how='all, inplace=True)

    welldata = dropna(welldata)

    # In [184]: welldata
    # Out[184]: 
    # <class 'pandas.core.frame.DataFrame'>
    # Int64Index: 127488 entries, 0 to 127487
    # Data columns:
    # barcode                   127488  non-null values
    # cell_id                   127488  non-null values
    # cell_line                 127488  non-null values
    # well_id                   127488  non-null values
    # row                       127488  non-null values
    # column                    127488  non-null values
    # sample_code               127488  non-null values
    # compound_number           127488  non-null values
    # compound_concentration    127488  non-null values
    # signal                    127488  non-null values
    # modified                  127488  non-null values
    # created                   127488  non-null values
    # dtypes: float64(5), object(7)

    welldata.barcode = welldata.barcode.apply(fix_barcode)

    for c in u'compound_number column'.split():
        welldata[c] = welldata[c].apply(maybe_to_int)

    sc2rc = dict(BDR=DISCARD, BL=BACKGROUND, CRL=CONTROL)
    welldata[u'rcat'] = \
        welldata.sample_code.apply(lambda sc: sc2rc.get(sc, DATA))
    del sc2rc

    welldata[u'compound_concentration_log10'] = \
        welldata.compound_concentration.apply(log10)

    welldata = dropcols(welldata,
                        u'cell_id well_id sample_code compound_concentration')

    # In [2]: welldata
    # Out[2]: 
    # <class 'pandas.core.frame.DataFrame'>
    # Int64Index: 127488 entries, 0 to 127487
    # Data columns:
    # barcode                         127488  non-null values
    # cell_line                       127488  non-null values
    # row                             127488  non-null values
    # column                          127488  non-null values
    # compound_number                 127488  non-null values
    # signal                          127488  non-null values
    # modified                        127488  non-null values
    # created                         127488  non-null values
    # rcat                            127488  non-null values
    # compound_concentration_log10    127488  non-null values
    # dtypes: float64(1), object(9)

# ---------------------------------------------------------------------------
    ## TBC
    # UPDATE WELLDATA DF WITH INFO FROM SEEDED AND PLATEDATA DFS
    welldata = pd.merge(welldata, seeded, on=u'barcode', how='left')
    del seeded

    # In [4]: welldata
    # Out[4]: 
    # <class 'pandas.core.frame.DataFrame'>
    # Int64Index: 127488 entries, 0 to 127487
    # Data columns:
    # barcode                         127488  non-null values
    # cell_line                       127488  non-null values
    # row                             127488  non-null values
    # column                          127488  non-null values
    # compound_number                 127488  non-null values
    # signal                          127488  non-null values
    # modified                        127488  non-null values
    # created                         127488  non-null values
    # rcat                            127488  non-null values
    # compound_concentration_log10    127488  non-null values
    # seeding_density_cells_ml        127488  non-null values
    # coefficient                     122112  non-null values
    # intercept                       122112  non-null values
    # estimated_seeding_signal        122112  non-null values
    # dtypes: float64(5), object(9)


    welldata = pd.merge(welldata, platedata, on=u'barcode', how='left')
    del platedata

    # In [7]: welldata
    # Out[7]: 
    # <class 'pandas.core.frame.DataFrame'>
    # Int64Index: 127488 entries, 0 to 127487
    # Data columns:
    # barcode                         127488  non-null values
    # cell_line                       127488  non-null values
    # row                             127488  non-null values
    # column                          127488  non-null values
    # compound_number                 127488  non-null values
    # signal                          127488  non-null values
    # modified                        127488  non-null values
    # created                         127488  non-null values
    # rcat                            127488  non-null values
    # compound_concentration_log10    127488  non-null values
    # seeding_density_cells_ml        127488  non-null values
    # coefficient                     122112  non-null values
    # intercept                       122112  non-null values
    # estimated_seeding_signal        122112  non-null values
    # qcscore                         127488  non-null values
    # pass_fail                       127488  non-null values
    # manual_flag                     127488  non-null values
    # time                            127488  non-null values
    # dtypes: float64(5), object(13)

# ---------------------------------------------------------------------------

    # ADD IDS TO WELLDATA DF
    welldata[u'replicate_group_id'] = welldata.apply(repgroup, axis=1)

    # In [9]: welldata
    # Out[9]: 
    # <class 'pandas.core.frame.DataFrame'>
    # Int64Index: 127488 entries, 0 to 127487
    # Data columns:
    # barcode                         127488  non-null values
    # cell_line                       127488  non-null values
    # row                             127488  non-null values
    # column                          127488  non-null values
    # compound_number                 127488  non-null values
    # signal                          127488  non-null values
    # modified                        127488  non-null values
    # created                         127488  non-null values
    # rcat                            127488  non-null values
    # compound_concentration_log10    127488  non-null values
    # seeding_density_cells_ml        127488  non-null values
    # coefficient                     122112  non-null values
    # intercept                       122112  non-null values
    # estimated_seeding_signal        122112  non-null values
    # qcscore                         127488  non-null values
    # pass_fail                       127488  non-null values
    # manual_flag                     127488  non-null values
    # time                            127488  non-null values
    # replicate_group_id              127488  non-null values
    # dtypes: float64(5), object(14)

    bggroup = groupid_updater(u'barcode', u'background_id', BACKGROUND)
    welldata[u'background_id'] = welldata.apply(bggroup, axis=1)
    del bggroup

    # In [11]: welldata
    # Out[11]: 
    # <class 'pandas.core.frame.DataFrame'>
    # Int64Index: 127488 entries, 0 to 127487
    # Data columns:
    # barcode                         127488  non-null values
    # cell_line                       127488  non-null values
    # row                             127488  non-null values
    # column                          127488  non-null values
    # compound_number                 127488  non-null values
    # signal                          127488  non-null values
    # modified                        127488  non-null values
    # created                         127488  non-null values
    # rcat                            127488  non-null values
    # compound_concentration_log10    127488  non-null values
    # seeding_density_cells_ml        127488  non-null values
    # coefficient                     122112  non-null values
    # intercept                       122112  non-null values
    # estimated_seeding_signal        122112  non-null values
    # qcscore                         127488  non-null values
    # pass_fail                       127488  non-null values
    # manual_flag                     127488  non-null values
    # time                            127488  non-null values
    # replicate_group_id              127488  non-null values
    # background_id                   127488  non-null values
    # dtypes: float64(5), object(15)

    ctrlgroup = groupid_updater(u'barcode', u'control_id', CONTROL)
    welldata[u'control_id'] = welldata.apply(ctrlgroup, axis=1)
    del ctrlgroup

    # In [13]: welldata
    # Out[13]: 
    # <class 'pandas.core.frame.DataFrame'>
    # Int64Index: 127488 entries, 0 to 127487
    # Data columns:
    # barcode                         127488  non-null values
    # cell_line                       127488  non-null values
    # row                             127488  non-null values
    # column                          127488  non-null values
    # compound_number                 127488  non-null values
    # signal                          127488  non-null values
    # modified                        127488  non-null values
    # created                         127488  non-null values
    # rcat                            127488  non-null values
    # compound_concentration_log10    127488  non-null values
    # seeding_density_cells_ml        127488  non-null values
    # coefficient                     122112  non-null values
    # intercept                       122112  non-null values
    # estimated_seeding_signal        122112  non-null values
    # qcscore                         127488  non-null values
    # pass_fail                       127488  non-null values
    # manual_flag                     127488  non-null values
    # time                            127488  non-null values
    # replicate_group_id              127488  non-null values
    # background_id                   127488  non-null values
    # control_id                      127488  non-null values
    # dtypes: float64(5), object(16)

# ------------------------------------------------------------

    # REORDER COLUMNS OF WELLDATA DF
    welldata = \
      welldata.reindex_axis(
        (u'rcat replicate_group_id background_id control_id '
         u'cell_line compound_number compound_concentration_log10 time '
         u'signal '
         u'barcode seeding_density_cells_ml intercept coefficient '
         u'estimated_seeding_signal row column modified created '
         u'qcscore pass_fail manual_flag'.split()),
        axis=1)

    # In [15]: welldata
    # Out[15]: 
    # <class 'pandas.core.frame.DataFrame'>
    # Int64Index: 127488 entries, 0 to 127487
    # Data columns:
    # rcat                            127488  non-null values
    # replicate_group_id              127488  non-null values
    # background_id                   127488  non-null values
    # control_id                      127488  non-null values
    # cell_line                       127488  non-null values
    # compound_number                 127488  non-null values
    # compound_concentration_log10    127488  non-null values
    # time                            127488  non-null values
    # signal                          127488  non-null values
    # barcode                         127488  non-null values
    # seeding_density_cells_ml        127488  non-null values
    # intercept                       122112  non-null values
    # coefficient                     122112  non-null values
    # estimated_seeding_signal        122112  non-null values
    # row                             127488  non-null values
    # column                          127488  non-null values
    # modified                        127488  non-null values
    # created                         127488  non-null values
    # qcscore                         127488  non-null values
    # pass_fail                       127488  non-null values
    # manual_flag                     127488  non-null values
    # dtypes: float64(5), object(16)


# ---------------------------------------------------------------------------

    # WRITE OUT RESULTS
    welldata.to_csv(tsv_path('test_dataset'), '\t',
                    index=False,
                    float_format='%.1f')
