var dagfuncs = window.dashAgGridFunctions = window.dashAgGridFunctions || {};

dagfuncs.getDataPath = function (data) {
    return data.path.split('.');
}

document.addEventListener("DOMContentLoaded", function () {
    console.log("DOMContentLoaded");
    //gridApi = dash_ag_grid.getApi("tree-data-example");
    //var rowCount = gridApi.getDisplayedRowCount();
    //console.log(gridApi);
});


function onRowDragEnd(e) {
    console.log(e);
    var newPath;
    const itemsToUpdate = [];

    if(e.overNode === undefined) {
        newPath = e.node.key;
    } else if(e.overNode.key === e.node.key) {
        return window.dash_clientside.no_update;
    } else if(e.node.allLeafChildren.includes(e.overNode)) {
        return window.dash_clientside.no_update;
    } else {
        newPath = e.overNode.data.path + "." + e.node.key;
    }

    const data = e.node.data;
    data.path = newPath;
    itemsToUpdate.push(data);

    e.node.allLeafChildren.forEach((node) => {
        if(node.data.id != data.id) {
            const child = node.data;
            child.path = newPath + "." + node.key;
            itemsToUpdate.push(child);
        }
    });
    const res = gridApi.applyTransaction({ update: itemsToUpdate });
}
