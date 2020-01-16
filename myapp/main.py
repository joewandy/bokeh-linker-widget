from bokeh.models import Button
from bokeh.models import CustomJS
from bokeh.models.widgets import Div
from bokeh.plotting import curdoc
from bokeh.layouts import row, column, gridplot

from functions import get_data, update_alert, NA, create_links, get_table_info

### define data sources ###

# create some example data
mf_df, mf_ds, mf_dt = get_data('mf', 5)
spectra_df, spectra_ds, spectra_dt = get_data('spectra', 10)
bgc_df, bgc_ds, bgc_dt = get_data('bgc', 10)
gcf_df, gcf_ds, gcf_dt = get_data('gcf', 5)

# create some example links
# 0 is not used because it's for NA
link_indices = [(1, 1), (1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (5, 8), (5, 9), (5, 10)]
mf_spectra = create_links(mf_df, spectra_df, 'mf_pk', 'spectra_pk', link_indices)

link_indices = [(1, 1), (2, 2), (1, 3), (3, 4), (3, 5), (5, 7)]
spectra_bgc = create_links(spectra_df, bgc_df, 'spectra_pk', 'bgc_pk', link_indices)

link_indices = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 2), (6, 3), (7, 4), (8, 5), (9, 5), (10, 5)]
bgc_gcf = create_links(bgc_df, gcf_df, 'bgc_pk', 'gcf_pk', link_indices)

# combine the data and link informations into a table info
# this will be passed to the linker object when the Load button is clicked
table_info = get_table_info(mf_df, mf_spectra, spectra_df, spectra_bgc, bgc_df, bgc_gcf, gcf_df)
data_sources = {
    'mf_table': mf_ds,
    'spectra_table': spectra_ds,
    'bgc_table': bgc_ds,
    'gcf_table': gcf_ds
}

# custom JS callback codes to call the linker when a data table is clicked
code = """    
    // get linker object    
    const linker = window.shared['linker'];
    if (!linker) {
        alert('Please click Load Data first!');
        cb_obj.indices = [];
        return;
    }
    
    // set selections       
    const selected_indices = cb_obj.indices;
    console.log(table_name, selected_indices);
    linker.removeConstraints(table_name);
    for(let i = 0; i < selected_indices.length; i++) {
        const idx = selected_indices[i];
        linker.addConstraint(table_name, idx, data_sources[table_name]);        
    }
    
    // query the linker and update data sources with the query result
    linker.query();
    linker.updateDataSources(data_sources);    
"""
mf_ds.selected.js_on_change('indices', CustomJS(args={'table_name': 'mf_table', 'data_sources': data_sources}, code=code))
spectra_ds.selected.js_on_change('indices', CustomJS(args={'table_name': 'spectra_table', 'data_sources': data_sources}, code=code))
bgc_ds.selected.js_on_change('indices', CustomJS(args={'table_name': 'bgc_table', 'data_sources': data_sources}, code=code))
gcf_ds.selected.js_on_change('indices', CustomJS(args={'table_name': 'gcf_table', 'data_sources': data_sources}, code=code))

### define widgets and layouts ###

widgets = []

alert_div = Div(text="", name='alert_div')
widgets.append(alert_div)

load_button = Button(label='Load Data')
load_button.callback = CustomJS(args=dict(tableInfo=table_info), code="""
    // disable this button so we won't create the linker again
    cb_obj.disabled = true;
    
    // create a linker object and put it into window, so it can be used in other callbacks
    // window.shared defined in main.js
    const linker = new Linker(tableInfo);
    window.shared['linker'] = linker;
""")
widgets.append(load_button)

title_mol_fam = Div(text='<h3>Molecular Family</h3>')
title_spectra = Div(text='<h3>Spectra</h3>')
title_bgc = Div(text='<h3>Biosynthetic Gene Cluster</h3>')
title_gcf = Div(text='<h3>Gene Cluster Family</h3>')

info_mf_spectra = Div(text="""
<h3>MF - Spectra Links</h3>
<ul>
    <li>(1, 1), (1, 2), (1, 3)</li>
    <li>(2, 4), (2, 5)</li>
    <li>(3, 6)</li>
    <li>(4, 7)</li>
    <li>(5, 8), (5, 9), (5, 10)</li>
</ul>
""")

info_spectra_bgc = Div(text="""
<h3>Spectra - BGC Links</h3>
<ul>
    <li>(1, 1), (1, 3)</li>
    <li>(2, 2)</li>
    <li>(3, 4), (3, 5)</li>
    <li>(5, 7)</li>
</ul>
""")

info_bgc_gcf = Div(text="""
<h3>BGC - GCF Links</h3>
<ul>
    <li>(1, 1), (2, 1), (3, 1), (4, 1)</li>
    <li>(5, 2)</li>
    <li>(6, 3)</li>
    <li>(7, 4)</li>
    <li>(8, 5), (9, 5), (10, 5)</li>
</ul>
""")

grids = gridplot([
    [title_mol_fam, title_spectra, title_bgc, title_gcf],
    [mf_dt, spectra_dt, bgc_dt, gcf_dt],
    [info_mf_spectra, info_spectra_bgc, info_bgc_gcf, None]
])
widgets.append(grids)

for w in widgets:
    curdoc().add_root(w)

update_alert(alert_div, 'Initialised OK!', 'success')
