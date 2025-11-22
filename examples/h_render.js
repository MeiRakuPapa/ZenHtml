// Renders a dict_-compatible tree into DOM nodes.
export function HRender(tree) {
  const renderNode = ({ tag, props = {}, children = [] }) => {
    const el = document.createElement(tag);
    Object.entries(props).forEach(([key, value]) => {
      if (value === true) {
        el.setAttribute(key, "");
      } else {
        el.setAttribute(key, value);
      }
    });
    for (const child of children) {
      el.append(
        typeof child === "string" ? document.createTextNode(child) : renderNode(child)
      );
    }
    return el;
  };

  return renderNode(tree);
}
