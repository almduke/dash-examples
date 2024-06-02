""" App """

import dash_ag_grid as dag
from dash import (
    Dash,
    html,
    dcc,
    Input,
    Output,
    State,
    callback,
    clientside_callback,
    ctx,
)

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
    {
        "field": "add",
        "cellRenderer": "ButtonAdd",
        "cellRendererParams": {"className": "button_plus"},
        "suppressMenu": True,
        "sortable": False,
        "minWidth": 75,
        "maxWidth": 75,
        "hide": True,
    },
    {
        "field": "del",
        "cellRenderer": "ButtonDel",
        "cellRendererParams": {"className": "button_minus"},
        "suppressMenu": True,
        "sortable": False,
        "minWidth": 75,
        "maxWidth": 75,
        "hide": True,
    },
    {"field": "name"},
    {"field": "value"},
    {"field": "id"},
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
            [{"label": "Enable grid editing", "value": "Y"}],
            id="enable_drag_and_drop",
        ),
        grid,
        html.Div(id="output"),
        html.Dialog(
            id="new-node-dialog",
            children=[
                html.Div(
                    dcc.Input(id="new-node-parent", type="hidden", value="")
                ),
                html.Div(dcc.Input(id="new-node-name", type="text", value="")),
                html.Button("Close", id="btn-close-dialog"),
            ],
        ),
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
                    gridApi.setColumnsVisible(["add","del"], false);
                } else {
                    gridApi.setGridOption("suppressRowDrag", false);
                    gridApi.addEventListener("rowDragEnd", onRowDragEnd);
                    gridApi.setColumnsVisible(["add","del"], true);
                }

                return window.dash_clientside.no_update;
            }
        }
    """,
    Output("tree-data-example", "id"),
    Input("enable_drag_and_drop", "value"),
    prevent_initial_call=True,
)


@callback(
    Output("tree-data-example", "rowTransaction"),
    Output("new-node-dialog", "open", allow_duplicate=True),
    Output("new-node-parent", "value"),
    Input("btn-close-dialog", "n_clicks"),
    Input("tree-data-example", "cellRendererData"),
    State("new-node-parent", "value"),
    State("new-node-name", "value"),
    State("tree-data-example", "rowData"),
    prevent_initial_call=True,
)
def row_update(btn_close, grid_button, parent_path, new_node_name, row_data):
    """Callback for add button press"""
    transaction = None
    trigger = ctx.triggered_id

    if trigger == "tree-data-example" and grid_button["colId"] == "add":
        return transaction, True, grid_button["value"]

    if trigger == "tree-data-example" and grid_button["colId"] == "del":
        transaction = {
            "remove": [
                {"id": row.get("id")}
                for row in row_data
                if row["path"].startswith(grid_button["value"])
            ]
        }

    if trigger == "btn-close-dialog" and btn_close > 0:
        new_id = max(item["id"] for item in row_data) + 1
        path = parent_path + "." + new_node_name
        transaction = {
            "add": [
                {
                    "id": new_id,
                    "path": path,
                    "name": new_node_name,
                    "value": None,
                }
            ]
        }

    return transaction, False, ""


if __name__ == "__main__":
    app.run(debug=True)
