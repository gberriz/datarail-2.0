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

    def groupid_updater(key, col, rcat):
        memo=dict()
        def groupid(v=None, _reset=False):
            if _reset: return memo.clear()
            rc = v[u'rcat']
            return (memo.setdefault(v[key], unicode(len(memo)))
                    if (rc == DATA or rc == rcat) else v[col])

        return groupid

    def keep(df, labels, axis=0, level=None):
        drop = list(set(df.columns).difference(set(labels.split()
                                                   if hasattr(labels, 'split')
                                                   else labels)))
        return df.drop(drop, axis=axis, level=level)

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
        ls = pd.ols(x=sdf[xcol][2:], y=sdf[ycol][2:])
        ret = ls.beta
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
    datapath = get_datapath()
    print u'reading data from %s...\t' % datapath,; sys.stdout.flush()
    workbook = pd.ExcelFile(str(datapath))
    del datapath

    welldatamapped = workbook.parse(u'WellDataMapped')

    platedata = workbook.parse(u'PlateData')
    calibration = workbook.parse(u'RefSeedSignal', header=1, skiprows=[0],
                                 skip_footer=7)
    seeded = workbook.parse(u'SeededNumbers')
    # del workbook

    print u'done'

# ---------------------------------------------------------------------------

    # CLEANUP CALIBRATION DF
    calibration.rename(columns={calibration.columns[0]:
                                    normalize_label(calibration.columns[0])},
                       inplace=True)
    fixre=re.compile(ur'^MCFDCIS\.COM$')
    calibration.rename(columns=lambda l: fixre.sub(u'MCF10DCIS.COM', l),
                       inplace=True)
    del fixre

# ---------------------------------------------------------------------------

    # RESTRUCTURE CALIBRATION DF
    calibration.set_index(calibration.columns[0], inplace=True)
    calibration = pd.DataFrame(calibration.stack()
                               .swaplevel(0, 1)
                               .sortlevel(), columns=[u'signal'])
    calibration.index.names[0] = u'cell_name'

# ---------------------------------------------------------------------------

    # CLEANUP SEEDED DF
    seeded.rename(columns=normalize_label, inplace=True)
    seeded.rename(columns={u'cell_line': u'cell_name'}, inplace=True)
    seeded = dropcols(seeded, u'read_date cell_id')
    seeded.barcode = seeded.barcode.apply(fix_barcode)

    hmssfx_re = re.compile(ur'_HMS$')
    seeded.cell_name = seeded.cell_name.apply(lambda s: hmssfx_re.sub(u'', s))
    del hmssfx_re

# ---------------------------------------------------------------------------

    # UPDATE SEEDED DF WITH INFO FROM CALIBRATION DF
    coeff = (calibration.reset_index().groupby(u'cell_name').apply(regress)
             .reset_index())
    seeded = pd.merge(seeded, coeff, on=u'cell_name', how='outer')
    del coeff
    del calibration

    seeded[u'estimated_seeding_signal'] = \
        np.round(seeded.intercept +
                 seeded.seeding_density_cells_ml * seeded.coefficient)

    seeded = dropcols(seeded, [u'cell_name'])

# ---------------------------------------------------------------------------

    # CLEANUP PLATEDATA
    platedata.rename(columns=normalize_label, inplace=True)

    # PANDAS BUG: the following fails silently (no 'time' column is created):
    # platedata.time = platedata.protocol_name.apply(lambda s: s[-4])

    platedata[u'time'] = platedata.protocol_name.apply(lambda s: s[-4])
    platedata.barcode = platedata.barcode.apply(fix_barcode)

    platedata = keep(platedata,
                     u'barcode time qcscore pass_fail manual_flag',
                     axis=1)

    for c in u'qcscore pass_fail manual_flag'.split():
        platedata[c] = platedata[c].apply(maybe_to_int)

# ---------------------------------------------------------------------------

    # CLEANUP WELLDATAMAPPED
    welldatamapped.rename(columns=normalize_label, inplace=True)

    data0 = dropna(welldatamapped)
    data0.rename(columns=dict(cell_name=u'cell_line',
                              compound_no=u'compound_number',
                              compound_conc=u'compound_concentration'),
                 inplace=True)

    sc2rc = dict(BDR=DISCARD, BL=BACKGROUND, CRL=CONTROL)
    data0[u'rcat'] = data0.sample_code.apply(lambda sc: sc2rc.get(sc, DATA))

    data0[u'compound_concentration_log10'] = \
        data0.compound_concentration.apply(log10)

    for c in u'compound_number column'.split():
        data0[c] = data0[c].apply(maybe_to_int)

    for cn in u'replicate_group_id control_id background_id'.split():
        data0[cn] = data0.apply(lambda x: u'', axis=1)


    data0 = dropcols(data0, (u'cell_id well_id sample_code '
                             u'compound_concentration'))

    data0.barcode = data0.barcode.apply(fix_barcode)

# ---------------------------------------------------------------------------

    # UPDATE DATA0 DF WITH INFO FROM SEEDED AND PLATEDATA DFS
    data0 = pd.merge(data0, seeded, on=u'barcode', how='left')
    del seeded

    data0 = pd.merge(data0, platedata, on=u'barcode', how='left')
    del platedata

# ---------------------------------------------------------------------------

    # REORDER COLUMNS OF DATA0 DF
    data0 = \
      data0.reindex_axis(
        (u'rcat replicate_group_id background_id control_id '
         u'cell_line compound_number compound_concentration_log10 time '
         u'signal '
         u'barcode seeding_density_cells_ml coefficient intercept '
         u'estimated_seeding_signal row column modified created '
         u'qcscore pass_fail manual_flag'.split()),
        axis=1)

# ---------------------------------------------------------------------------

    # ADD IDS TO DATA0 DF
    data0[u'replicate_group_id'] = data0.apply(repgroup, axis=1)

    bggroup = groupid_updater(u'barcode', u'background_id', BACKGROUND)
    data0[u'background_id'] = data0.apply(bggroup, axis=1)

    ctrlgroup = groupid_updater(u'barcode', u'control_id', CONTROL)
    data0[u'control_id'] = data0.apply(ctrlgroup, axis=1)

# ------------------------------------------------------------

    # WRITE OUT RESULTS
    data0.to_csv(tsv_path('test_dataset'), '\t', index=False, float_format='%.1f')
