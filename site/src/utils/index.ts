import React from 'react';

const isComponent = (child: React.ReactNode, component: string) => {
  return React.isValidElement(child) && (child as React.ReactElement).props['mdxType'] === component;
}

export {
  isComponent
}