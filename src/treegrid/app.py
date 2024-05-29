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
    # Output("output", "children"),
    Output("tree-data-example", "rowTransaction"),
    Input("tree-data-example", "cellRendererData"),
    State("tree-data-example", "rowData"),
    prevent_initial_call=True,
)
def row_update(n, row_data):
    """Callback for add button press"""
    app.logger.info(n)
    result = ""
    if n["colId"] == "add":
        new_id = max(item["id"] for item in row_data) + 1
        row_id = int(n["rowId"])
        path = next((row for row in row_data if row["id"] == row_id), "")[
            "path"
        ]
        path = path + "." + n["value"]
        result = {
            "add": [
                {"id": new_id, "path": path, "name": n["value"], "value": None}
            ]
        }
    if n["colId"] == "del":
        path = row_data[n["rowIndex"]]["path"]
        result = {
            "remove": [
                {"id": row.get("id")}
                for row in row_data
                if row["path"].startswith(path)
            ]
        }
        app.logger.info(path)
        app.logger.info(result)
    return result


if __name__ == "__main__":
    app.run(debug=True)
