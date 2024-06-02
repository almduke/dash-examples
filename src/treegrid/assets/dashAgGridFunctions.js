var dagfuncs = (window.dashAgGridFunctions = window.dashAgGridFunctions || {});
var dagcomponentfuncs = (window.dashAgGridComponentFunctions =
  window.dashAgGridComponentFunctions || {});

dagfuncs.getDataPath = function (data) {
  return data.path.split(".");
};

function onRowDragEnd(e) {
  console.log(e);
  var newPath;
  const itemsToUpdate = [];

  if (e.overNode === undefined) {
    newPath = e.node.key;
  } else if (e.overNode.key === e.node.key) {
    return window.dash_clientside.no_update;
  } else if (e.node.allLeafChildren.includes(e.overNode)) {
    return window.dash_clientside.no_update;
  } else {
    newPath = e.overNode.data.path + "." + e.node.key;
  }

  const data = e.node.data;
  data.path = newPath;
  itemsToUpdate.push(data);

  e.node.allLeafChildren.forEach((node) => {
    if (node.data.id != data.id) {
      const child = node.data;
      child.path = newPath + "." + node.key;
      itemsToUpdate.push(child);
    }
  });
  const res = gridApi.applyTransaction({ update: itemsToUpdate });
}

dagcomponentfuncs.ButtonAdd = function (props) {
  const { setData, data } = props;

  function onClick(e) {
    e.persist();
    setData(e.target.value);
  }
  return React.createElement(
    "button",
    {
      onClick: onClick,
      className: props.className,
      value: data.path,
    },
    props.value,
  );
};

dagcomponentfuncs.ButtonDel = function (props) {
  const { setData, data } = props;

  function onClick(e) {
    e.persist();
    setData(e.target.value);
  }
  return React.createElement(
    "button",
    {
      onClick: onClick,
      className: props.className,
      value: data.path,
    },
    props.value,
  );
};
