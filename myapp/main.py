from bokeh.models import Button
from bokeh.models import CustomJS
from bokeh.models.widgets import Div
from bokeh.plotting import curdoc
from bokeh.layouts import row, column, gridplot

from functions import get_data, update_alert, NA, create_links, get_table_info

### define data sources ###

# create some example data
max_items = 20
spectra_df, spectra_ds, spectra_dt = get_data('spectra', max_items)
mf_df, mf_ds, mf_dt = get_data('mf', max_items)
bgc_df, bgc_ds, bgc_dt = get_data('bgc', max_items)
gcf_df, gcf_ds, gcf_dt = get_data('gcf', max_items)

# create some example links, 0 is not used because it's NA
indices = [(1, 1), (1, 2), (1, 3), (1, 4), (2, 2), (2, 3), (3, 3)]
spectra_mf = create_links(spectra_df, mf_df, 'spectra_pk', 'mf_pk', indices)
mf_bgc = create_links(mf_df, bgc_df, 'mf_pk', 'bgc_pk', indices)
bgc_gcf = create_links(bgc_df, gcf_df, 'bgc_pk', 'gcf_pk', indices)

# combine the data and link informations into a table info
table_info = get_table_info(spectra_df, spectra_mf, mf_df, mf_bgc, bgc_df, bgc_gcf, gcf_df)

spectra_ds.selected.js_on_change('indices', CustomJS(args=dict(spectra_ds=spectra_ds, mf_ds=mf_ds, bgc_ds=bgc_ds,
                                                               gcf_ds=gcf_ds), code="""
    console.log(window.shared);
    var spectra_indices = cb_obj.indices;
    var mf_data = [];
    var bgc_data = [];
    var gcf_data = [];

    for (var i = 0; i < spectra_indices.length; i++) {
        var idx = spectra_indices[i];
        mf_indices.push(idx+1);
        bgc_indices.push(idx+2);
        gcf_indices.push(idx+3);            
    }
    mf_ds.selected.indices = mf_indices;
    bgc_ds.selected.indices = bgc_indices;
    gcf_ds.selected.indices = gcf_indices;

    // example to change data
    // var d1 = s1.data;
    // var d2 = s2.data;
    // for (var i = 0; i < inds.length; i++) {
    //    d2['x'].push(d1['x'][inds[i]]+100)
    //    d2['y'].push(d1['y'][inds[i]]+100)
    // }        

    mf_ds.change.emit();
    bgc_ds.change.emit();
    gcf_ds.change.emit();
"""))

### define widgets and layouts ###

widgets = []

alert_div = Div(text="", name='alert_div')
widgets.append(alert_div)

load_button = Button(label='Load Data')
load_button.callback = CustomJS(args=dict(tableInfo=table_info), code="""
    // create a linker object and put it into window, so it can be used in other callbacks
    // window.shared defined in main.js
    const linker = new Linker(tableInfo);
    window.shared['linker'] = linker;
""")
widgets.append(load_button)

title_spectra = Div(text='<h3>Spectra</h3>')
title_mol_fam = Div(text='<h3>Molecular Family</h3>')
title_bgc = Div(text='<h3>Biosynthetic Gene Cluster</h3>')
title_gcf = Div(text='<h3>Gene Cluster Family</h3>')

grids = gridplot([
    [title_spectra, title_mol_fam, title_bgc, title_gcf],
    [spectra_dt, mf_dt, bgc_dt, gcf_dt]
])
widgets.append(grids)

for w in widgets:
    curdoc().add_root(w)

update_alert(alert_div, 'Initialised OK!', 'success')
