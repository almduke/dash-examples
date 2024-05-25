import dash_ag_grid as dag
from dash import Dash, html, dcc, Input, Output, clientside_callback

app = Dash(__name__, suppress_callback_exceptions=True)


rowData = [
    {
        "id": 1,
        "path": "Alpha",
        "name": "Alpha",
        "value": 50,
    },
    {
        "id": 2,
        "path": "Alpha.One",
        "name": "One ",
        "value": 25,
    },
    {
        "id": 3,
        "path": "Alpha.Two",
        "name": "Two",
        "value": 25,
    },
    {
        "id": 4,
        "path": "Beta",
        "name": "Beta",
        "value": 50,
    },
    {
        "id": 5,
        "path": "Beta.Three",
        "name": "Three",
        "value": 25,
    },
    {
        "id": 6,
        "path": "Beta.Four",
        "name": "Four",
        "value": 25,
    },
]


columnDefs = [
    {"field": "name"},
    {"field": "value"},
]


grid = html.Div(
    [
        dag.AgGrid(
            id="tree-data-example",
            columnDefs=columnDefs,
            defaultColDef={
                "flex": 1,
            },
            dashGridOptions={
                "autoGroupColumnDef": {
                    "headerName": "Path",
                    "minWidth": 300,
                    "rowDrag": True,
                    "cellRendererParams": {
                        "suppressCount": True,
                    },
                },
                "groupDefaultExpanded": -1,
                "getDataPath": {"function": "getDataPath(params)"},
                "treeData": True,
                "animateRows": False,
                "onRowDragEnd": {"function": "onRowDragEnd(params)"},
                "suppressRowDrag": True,
            },
            rowData=rowData,
            enableEnterpriseModules=True,
            getRowId="params.data.id",
        ),
    ]
)


app.layout = html.Div(
    [
        dcc.Markdown("Example: Tree grid with drag and drop."),
        dcc.Checklist(
            [{"label": "Enable drag and drop", "value": "Y"}],
            id="enable_drag_and_drop",
        ),
        grid,
        html.Div(id="output", children=[]),
    ]
)


clientside_callback(
    """
        (n) => {
            if (n) {
                gridApi = dash_ag_grid.getApi("tree-data-example");

                if(n[0] === undefined) {
                    gridApi.setGridOption("suppressRowDrag", true);
                    gridApi.removeEventListener("rowDragEnd", onRowDragEnd);
                } else {
                    gridApi.setGridOption("suppressRowDrag", false);
                    gridApi.addEventListener("rowDragEnd", onRowDragEnd);
                }

                return window.dash_clientside.no_update;
            }
        }
    """,
    Output("tree-data-example", "id"),
    Input("enable_drag_and_drop", "value"),
    prevent_initial_call=True,
)

if __name__ == "__main__":
    app.run(debug=True)
