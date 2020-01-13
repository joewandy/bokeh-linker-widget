import numpy as np
import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn

NA = '-'


def get_data(label, max_items):
    items = ['%s_%d' % (label, i) for i in list(range(max_items))]
    x1 = np.random.randint(low=1, high=100, size=max_items).tolist()
    x2 = np.random.randint(low=1, high=100, size=max_items).tolist()
    x3 = np.random.randint(low=1, high=100, size=max_items).tolist()

    items.insert(0, NA)
    x1.insert(0, NA)
    x2.insert(0, NA)
    x3.insert(0, NA)

    colname = '%s_pk' % label
    data = {
        colname: items,
        'x1': x1,
        'x2': x2,
        'x3': x3
    }
    columns = [
        TableColumn(field=colname, title='ID'),
        TableColumn(field='x1', title='x1'),
        TableColumn(field='x2', title='x2'),
        TableColumn(field='x3', title='x3'),
    ]
    df = pd.DataFrame(data)
    ds = ColumnDataSource(df)
    dt = DataTable(source=ds, columns=columns, width=300, height=300)
    return df, ds, dt


def create_links(df1, df2, key1, key2, indices):
    links = []

    # link everything on df1 to NA
    for idx, row in df1.iterrows():
        val1 = row[key1]
        val2 = NA
        link = {key1: val1, key2: val2}
        links.append(link)

    # link everything on df2 to NA
    for idx, row in df2.iterrows():
        val1 = NA
        val2 = row[key2]
        link = {key1: val1, key2: val2}
        links.append(link)

    # link entries in df1 and df2 to each other according to their indices
    for idx1, idx2 in indices:
        val1 = df1.loc[idx1][key1]
        val2 = df2.loc[idx2][key2]
        link = {key1: val1, key2: val2}
        links.append(link)
    return links


def get_table_info(spectra_df, spectra_mf, mf_df, mf_bgc, bgc_df, bgc_gcf, gcf_df):
    tables_info = [
        {
            'table_name': 'spectra_table',
            'table_data': spectra_df.to_dict('records'),
            'options': {
                'visible': True,
                'pk': 'spectra_pk'
            },
            'relationship': {'with': 'spectra_mf', 'using': 'spectra_pk'}
        },
        {
            'tableName': 'spectra_mf',
            'tableData': spectra_mf,
            'options': {
                'visible': False
            },
            'relationship': {'with': 'mf_table', 'using': 'mf_pk'}
        },
        {
            'table_name': 'mf_table',
            'table_data': mf_df.to_dict('records'),
            'options': {
                'visible': True,
                'pk': 'mf_pk'
            },
            'relationship': {'with': 'mf_bgc', 'using': 'mf_pk'}
        },
        {
            'tableName': 'mf_bgc',
            'tableData': mf_bgc,
            'options': {
                'visible': False
            },
            'relationship': {'with': 'bgc_table', 'using': 'bgc_pk'}
        },
        {
            'table_name': 'bgc_table',
            'table_data': bgc_df.to_dict('records'),
            'options': {
                'visible': True,
                'pk': 'bgc_pk'
            },
            'relationship': {'with': 'bgc_gcf', 'using': 'bgc_pk'}
        },
        {
            'tableName': 'bgc_gcf',
            'tableData': bgc_gcf,
            'options': {
                'visible': False
            },
            'relationship': {'with': 'gcf_table', 'using': 'bgc_pk'}
        },
        {
            'table_name': 'gcf_table',
            'table_data': gcf_df.to_dict('records'),
            'options': {
                'visible': True,
                'pk': 'gcf_pk'
            }
        },

    ]
    return tables_info


def update_alert(alert_div, msg, alert_class='primary'):
    alert_div.text = '<div class="alert alert-{}" role="alert">{}</div>'.format(alert_class, msg)
